import math


# ====================================================
# Acceleration Magnitude
# ====================================================

def acceleration_magnitude(ax, ay, az):

    return math.sqrt(
        ax * ax +
        ay * ay +
        az * az
    )


# ====================================================
# Gyroscope Magnitude
# ====================================================

def gyroscope_magnitude(gx, gy, gz):

    return math.sqrt(
        gx * gx +
        gy * gy +
        gz * gz
    )


# ====================================================
# Left Motion Score
# ====================================================

def left_motion_score(row):
    """
    Computes motion score for LEFT glove.

    row can be:
        - CSV row (list)
        - Packet (dict)
    """

    # CSV Row
    if isinstance(row, list):

        ax = float(row[1])
        ay = float(row[2])
        az = float(row[3])

        gx = float(row[4])
        gy = float(row[5])
        gz = float(row[6])

    # Dictionary Packet
    else:

        ax = float(row["L_ax"])
        ay = float(row["L_ay"])
        az = float(row["L_az"])

        gx = float(row["L_gx"])
        gy = float(row["L_gy"])
        gz = float(row["L_gz"])

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

    return acc + 0.5 * gyro


# ====================================================
# Right Motion Score
# ====================================================

def right_motion_score(row):

    """
    Computes motion score for RIGHT glove.
    """

    if isinstance(row, list):

        ax = float(row[7])
        ay = float(row[8])
        az = float(row[9])

        gx = float(row[10])
        gy = float(row[11])
        gz = float(row[12])

    else:

        ax = float(row["R_ax"])
        ay = float(row["R_ay"])
        az = float(row["R_az"])

        gx = float(row["R_gx"])
        gy = float(row["R_gy"])
        gz = float(row["R_gz"])

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

    return acc + 0.5 * gyro


# ====================================================
# Combined Motion Score
# ====================================================

def combined_motion_score(row):

    """
    Motion detector score.

    Uses the larger motion from either glove.
    """

    left = left_motion_score(row)

    right = right_motion_score(row)

    return max(
        left,
        right
    )