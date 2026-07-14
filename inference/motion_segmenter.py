"""
motion_segmenter.py

Real-time motion segmentation for a two-wrist (Left/Right) boxing sensor
stream.

Responsibility of this module
------------------------------
MotionSegmenter watches a continuous stream of BLE packets and cuts out
the sub-sequences ("segments") that correspond to individual punches.
It does NOT classify, normalize to a fixed length, or predict anything.
It hands back a variable-length, raw feature window plus metadata that
downstream stages (feature engineering / Random Forest predictor) can
consume.

High-level algorithm
---------------------
1. While idle, continuously estimate the "resting" (background) motion
   level using a rolling window of recent motion scores.
2. Derive an adaptive trigger threshold from that baseline
   (mean + N * std).
3. When the incoming motion score exceeds the trigger threshold, start
   recording a segment, seeding it with a short pre-trigger buffer so
   the very start of the punch (before it crossed the threshold) is not
   lost.
4. While recording, track the peak motion sample (magnitude, packet,
   and index within the segment) and use a *dynamic* end-threshold
   (a fraction of the observed peak, floored by the baseline threshold)
   to decide when the motion has actually died down.
5. End the segment once motion has stayed below the end-threshold for
   `quiet_time_ms`, or once a hard `max_segment_packets` cap is hit.
6. Discard segments that are too short to be a real punch (noise).
7. After a valid segment, enforce a cooldown window so the trailing
   vibration/settling of one punch cannot be mistaken for a second one.
"""

from collections import deque
import statistics

import numpy as np

from utils.motion import (
    left_motion_score,
    right_motion_score,
    combined_motion_score,
)


class MotionSegmenter:
    """
    Streaming segmenter that converts a raw BLE packet stream into
    discrete punch segments.

    Usage
    -----
    segmenter = MotionSegmenter()
    for packet in packet_stream:
        result = segmenter.process(packet)
        if result is not None:
            # result["window"] -> np.ndarray of shape (n_packets, 12)
            handle_punch(result)
    """

    # Hand labels returned in the result dict.
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(
        self,
        baseline_window=50,
        trigger_sigma=3.0,
        quiet_time_ms=150,
        pre_trigger_packets=10,
        max_segment_packets=80,
        min_segment_packets=5,
        cooldown_ms=200,
        end_threshold_ratio=0.20,
        min_baseline_samples=10,
        fallback_threshold=3.0,
    ):
        """
        Parameters
        ----------
        baseline_window : int
            Number of recent idle motion scores kept to estimate the
            resting baseline (mean/std).
        trigger_sigma : float
            Number of standard deviations above the baseline mean that
            a motion score must exceed to trigger recording.
        quiet_time_ms : int
            How long motion must stay below the end-threshold before a
            segment is considered finished.
        pre_trigger_packets : int
            Number of packets kept *before* the trigger so the start of
            the punch isn't clipped.
        max_segment_packets : int
            Hard safety cap on segment length, in case motion never
            drops back down.
        min_segment_packets : int
            Segments shorter than this are treated as noise and
            discarded (no result is returned for them).
        cooldown_ms : int
            After a valid segment ends, incoming packets are ignored
            for this many milliseconds to prevent double-triggering on
            the same punch's settling motion.
        end_threshold_ratio : float
            Fraction of the segment's peak motion used as the dynamic
            end-threshold (floored by the baseline threshold).
        min_baseline_samples : int
            Minimum number of baseline samples required before trusting
            the computed baseline threshold; below this, a fixed
            fallback threshold is used instead.
        fallback_threshold : float
            Threshold used while the baseline has not yet accumulated
            `min_baseline_samples` readings.
        """

        # -----------------------------
        # Configuration
        # -----------------------------
        self.trigger_sigma = trigger_sigma
        self.quiet_time_ms = quiet_time_ms
        self.max_segment_packets = max_segment_packets
        self.min_segment_packets = min_segment_packets
        self.cooldown_ms = cooldown_ms
        self.end_threshold_ratio = end_threshold_ratio
        self.min_baseline_samples = min_baseline_samples
        self.fallback_threshold = fallback_threshold

        # -----------------------------
        # Idle baseline estimation
        # -----------------------------
        self.baseline_scores = deque(maxlen=baseline_window)

        # -----------------------------
        # Pre-trigger buffer
        # -----------------------------
        self.pre_buffer = deque(maxlen=pre_trigger_packets)

        # -----------------------------
        # Recording / segment state
        # -----------------------------
        self.recording = False
        self.segment = []
        self.motion_start_ts = None
        self.last_active_ts = None

        # -----------------------------
        # Peak tracking (within current segment)
        # -----------------------------
        self.peak_motion = 0.0
        self.peak_packet = None
        self.peak_index = None

        # -----------------------------
        # Cooldown state
        # -----------------------------
        # Timestamp (ms) until which incoming packets are ignored.
        # None means "no active cooldown".
        self.cooldown_until_ts = None

        print("[MotionSegmenter] Ready")

    # =====================================================
    # Public API
    # =====================================================

    def process(self, packet):
        """
        Feed a single incoming packet into the segmenter.

        Returns
        -------
        dict or None
            A result dict (see module docstring / finish_segment) if a
            valid punch segment just completed on this call, otherwise
            None.
        """

        ts = packet["ts"]
        motion = combined_motion_score(packet)

        # ------------------------------------------------
        # Cooldown: swallow packets right after a punch so
        # its settling vibration isn't misread as a new one.
        # ------------------------------------------------
        if not self.recording and self._in_cooldown(ts):
            return None

        baseline_threshold = self._current_baseline_threshold()

        # ------------------------------------------------
        # Idle state: update baseline/pre-buffer and watch
        # for a trigger.
        # ------------------------------------------------
        if not self.recording:
            self.baseline_scores.append(motion)
            self.pre_buffer.append(packet)

            if motion > baseline_threshold:
                self._start_recording(packet, motion, ts)

            return None

        # ------------------------------------------------
        # Recording state: accumulate the segment and track
        # its peak.
        # ------------------------------------------------
        self.segment.append(packet)
        self._update_peak(packet, motion)

        end_threshold = self._compute_end_threshold(baseline_threshold)

        if motion > end_threshold:
            self.last_active_ts = ts

        # Hard cap: never let a segment grow unbounded.
        if len(self.segment) >= self.max_segment_packets:
            return self._finish_segment(ts)

        # Motion has been quiet long enough -> segment is done.
        quiet_duration_ms = ts - self.last_active_ts
        if quiet_duration_ms >= self.quiet_time_ms:
            return self._finish_segment(ts)

        return None

    def packet_to_vector(self, packet):
        """
        Flatten a single packet into the fixed 12-value feature order
        used throughout the pipeline:

        [L_ax, L_ay, L_az, L_gx, L_gy, L_gz,
         R_ax, R_ay, R_az, R_gx, R_gy, R_gz]
        """

        left = packet["L"]
        right = packet["R"]

        return [
            left["ax"], left["ay"], left["az"],
            left["gx"], left["gy"], left["gz"],
            right["ax"], right["ay"], right["az"],
            right["gx"], right["gy"], right["gz"],
        ]

    # =====================================================
    # Baseline / threshold helpers
    # =====================================================

    def _current_baseline_threshold(self):
        """
        Adaptive idle-motion threshold:
            baseline_mean + trigger_sigma * baseline_std

        Falls back to a fixed threshold until enough baseline samples
        have been collected to make the statistics meaningful.
        """

        if len(self.baseline_scores) < self.min_baseline_samples:
            return self.fallback_threshold

        mean = statistics.mean(self.baseline_scores)
        std = statistics.pstdev(self.baseline_scores)

        return mean + self.trigger_sigma * std

    def _compute_end_threshold(self, baseline_threshold):
        """
        Dynamic end-of-motion threshold. Using a fraction of the
        segment's own peak (rather than the fixed start threshold)
        means a hard punch has to fully die down before the segment
        ends, while a soft punch ends sooner - without ever dropping
        below the baseline noise floor.
        """

        return max(baseline_threshold, self.end_threshold_ratio * self.peak_motion)

    def _in_cooldown(self, ts):
        """True if `ts` still falls within the post-punch cooldown window."""

        return self.cooldown_until_ts is not None and ts < self.cooldown_until_ts

    # =====================================================
    # Segment lifecycle
    # =====================================================

    def _start_recording(self, packet, motion, ts):
        """Begin a new segment, seeded with the pre-trigger buffer."""

        self.recording = True

        # Copy (not reference) the pre-trigger packets so later mutation
        # of pre_buffer can't retroactively affect this segment.
        self.segment = list(self.pre_buffer)
        self.segment.append(packet)

        self.motion_start_ts = ts
        self.last_active_ts = ts

        self.peak_motion = motion
        self.peak_packet = packet
        self.peak_index = len(self.segment) - 1

        print("\n==============================")
        print("Motion Started")
        print("==============================")

    def _update_peak(self, packet, motion):
        """Update the running peak-motion sample for the active segment."""

        if motion > self.peak_motion:
            self.peak_motion = motion
            self.peak_packet = packet
            self.peak_index = len(self.segment) - 1

    def _finish_segment(self, ts):
        """
        Close out the current segment.

        Short segments (below `min_segment_packets`) are treated as
        noise and dropped silently - no cooldown is applied for them,
        since they were never a real punch. Valid segments trigger the
        cooldown window and are returned to the caller.
        """

        packet_count = len(self.segment)

        print("\n==============================")
        print("Motion Finished")
        print("==============================")
        print(f"Packets     : {packet_count}")
        print(f"Peak Motion : {self.peak_motion:.2f}")

        result = None

        if packet_count >= self.min_segment_packets:
            window = np.array(
                [self.packet_to_vector(p) for p in self.segment],
                dtype=float,
            )

            trigger_hand = self._determine_trigger_hand(self.peak_packet)

            result = {
                "window": window,
                "peak_motion": self.peak_motion,
                "peak_index": self.peak_index,
                "trigger_hand": trigger_hand,
                "duration_packets": packet_count,
            }

            # Only genuine punches start a cooldown period.
            self.cooldown_until_ts = ts + self.cooldown_ms
        else:
            print("[MotionSegmenter] Segment rejected (too short)")

        self._reset_after_segment()

        return result

    def _reset_after_segment(self):
        """Clear per-segment state so the segmenter is ready to idle again."""

        self.recording = False
        self.segment = []
        self.motion_start_ts = None
        self.last_active_ts = None

        self.peak_motion = 0.0
        self.peak_packet = None
        self.peak_index = None

    # =====================================================
    # Trigger-hand classification
    # =====================================================

    def _determine_trigger_hand(self, packet):
        """
        Decide which hand initiated the punch by comparing per-hand
        motion scores on the peak packet of the segment.
        """

        left_score = left_motion_score(packet)
        right_score = right_motion_score(packet)

        return self.LEFT if left_score >= right_score else self.RIGHT