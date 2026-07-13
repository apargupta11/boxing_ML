from inference.buffer import RollingBuffer
from preprocessing.motion_segmenter import MotionSegmenter


class MotionDetector:

    def __init__(self, max_buffer_size=300):

        self.buffer = RollingBuffer(
            max_samples=max_buffer_size
        )

        self.segmenter = MotionSegmenter()

    # ====================================================
    # Process One Incoming Packet
    # ====================================================

    def process(self, packet):

        """
        Parameters
        ----------
        packet : dict
            One incoming BLE IMU packet.

        Returns
        -------
        None
            No motion completed yet.

        OR

        list[dict]
            Completed motion segment.
        """

        # ------------------------------------
        # Store packet
        # ------------------------------------

        self.buffer.add(packet)

        # ------------------------------------
        # Ask MotionSegmenter
        # ------------------------------------

        segment = self.segmenter.process(
            self.buffer.get_all()
        )

        return segment

    # ====================================================
    # Reset Detector
    # ====================================================

    def reset(self):

        self.buffer.clear()

        self.segmenter.reset()