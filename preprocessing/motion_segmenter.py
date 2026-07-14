import math


def acceleration_magnitude(ax, ay, az):

    return math.sqrt(
        ax * ax +
        ay * ay +
        az * az
    )


def gyroscope_magnitude(gx, gy, gz):

    return math.sqrt(
        gx * gx +
        gy * gy +
        gz * gz
    )


def motion_score(row, hand):
    """
    Returns combined motion score.

    row -> CSV row
    hand -> LEFT / RIGHT
    """

    if hand == "LEFT":

        ax = float(row[1])
        ay = float(row[2])
        az = float(row[3])

        gx = float(row[4])
        gy = float(row[5])
        gz = float(row[6])

    else:

        ax = float(row[7])
        ay = float(row[8])
        az = float(row[9])

        gx = float(row[10])
        gy = float(row[11])
        gz = float(row[12])

    acc = acceleration_magnitude(
        ax,
        ay,
        az
    )

    gyro = gyroscope_magnitude(
        gx,
        gy,
        gz
    )

    # Gyroscope contributes less
    return acc + 0.5 * gyro


# =====================================================
# Find Peak
# =====================================================

def find_peak(
        rows,
        trigger,
        hand,
        search_radius=20
):

    """
    Searches around ESP32 trigger
    and finds actual punch peak.
    """

    left = max(
        0,
        trigger - search_radius
    )

    right = min(
        len(rows) - 1,
        trigger + search_radius
    )

    best_score = -1
    best_index = trigger

    for i in range(left, right + 1):

        score = motion_score(
            rows[i],
            hand
        )

        if score > best_score:

            best_score = score
            best_index = i

    return best_index


# =====================================================
# Estimate Threshold
# =====================================================

# =====================================================
# Estimate Threshold
# =====================================================

# =====================================================
# Estimate Threshold
# =====================================================

def estimate_threshold(
        rows,
        peak,
        hand
):
    """
    Dynamic threshold based on:

    1. Background noise
    2. Punch intensity

    threshold = max(
        baseline + 3*std,
        20% of punch peak
    )
    """

    # ------------------------------------------
    # Baseline Region
    # ------------------------------------------

    start = max(
        0,
        peak - 50
    )

    baseline_scores = []

    for i in range(start, peak):

        baseline_scores.append(
            motion_score(
                rows[i],
                hand
            )
        )

    # Safety

    if len(baseline_scores) == 0:

        return 3.0

    # ------------------------------------------
    # Baseline Mean
    # ------------------------------------------

    baseline_mean = sum(
        baseline_scores
    ) / len(baseline_scores)

    # ------------------------------------------
    # Standard Deviation
    # ------------------------------------------

    variance = sum(

        (x - baseline_mean) ** 2

        for x in baseline_scores

    ) / len(baseline_scores)

    baseline_std = math.sqrt(
        variance
    )

    # ------------------------------------------
    # Baseline Threshold
    # ------------------------------------------

    baseline_threshold = (

        baseline_mean +

        3 * baseline_std

    )

    # ------------------------------------------
    # Peak Threshold
    # ------------------------------------------

    peak_value = motion_score(
        rows[peak],
        hand
    )

    peak_threshold = 0.20 * peak_value

    # ------------------------------------------
    # Final Threshold
    # ------------------------------------------

    threshold = max(
        baseline_threshold,
        peak_threshold
    )

    print("\n--------------------------------")
    print("Dynamic Threshold Estimation")
    print("--------------------------------")
    print(f"Baseline Mean      : {baseline_mean:.2f}")
    print(f"Baseline Std       : {baseline_std:.2f}")
    print(f"Peak Motion Score  : {peak_value:.2f}")
    print(f"Noise Threshold    : {baseline_threshold:.2f}")
    print(f"Peak Threshold     : {peak_threshold:.2f}")
    print(f"Final Threshold    : {threshold:.2f}")

    return threshold
# =====================================================
# Walk Backward
# =====================================================

def find_start(
        rows,
        peak,
        hand,
        threshold,
        quiet_samples=5
):

    quiet = 0

    for i in range(
            peak,
            0,
            -1
    ):

        score = motion_score(
            rows[i],
            hand
        )

        if score < threshold:

            quiet += 1

            if quiet >= quiet_samples:

                return i

        else:

            quiet = 0

    return 0


# =====================================================
# Walk Forward
# =====================================================

def find_end(
        rows,
        peak,
        hand,
        threshold,
        quiet_samples=5
):

    quiet = 0

    for i in range(
            peak,
            len(rows)
    ):

        score = motion_score(
            rows[i],
            hand
        )

        if score < threshold:

            quiet += 1

            if quiet >= quiet_samples:

                return i

        else:

            quiet = 0

    return len(rows) - 1


# =====================================================
# Segment Punch
# =====================================================

def segment_punch(
        rows,
        trigger,
        hand
):

    peak = find_peak(
        rows,
        trigger,
        hand
    )

    threshold = estimate_threshold(
        rows,
        peak,
        hand
    )

    start = find_start(
        rows,
        peak,
        hand,
        threshold
    )

    end = find_end(
        rows,
        peak,
        hand,
        threshold
    )

    return start, end