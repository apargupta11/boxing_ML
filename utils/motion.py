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

    Supports:
        1. Training CSV row (list)
        2. BLE packet (dict)
    """

    # -----------------------------------
    # CSV Row
    # -----------------------------------

    if isinstance(row, list):

        ax = float(row[1])
        ay = float(row[2])
        az = float(row[3])

        gx = float(row[4])
        gy = float(row[5])
        gz = float(row[6])

    # -----------------------------------
    # BLE Packet
    # -----------------------------------

    else:

        L = row["L"]

        ax = float(L["ax"])
        ay = float(L["ay"])
        az = float(L["az"])

        gx = float(L["gx"])
        gy = float(L["gy"])
        gz = float(L["gz"])

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

    Supports:
        1. Training CSV row (list)
        2. BLE packet (dict)
    """

    # -----------------------------------
    # CSV Row
    # -----------------------------------

    if isinstance(row, list):

        ax = float(row[7])
        ay = float(row[8])
        az = float(row[9])

        gx = float(row[10])
        gy = float(row[11])
        gz = float(row[12])

    # -----------------------------------
    # BLE Packet
    # -----------------------------------

    else:

        R = row["R"]

        ax = float(R["ax"])
        ay = float(R["ay"])
        az = float(R["az"])

        gx = float(R["gx"])
        gy = float(R["gy"])
        gz = float(R["gz"])

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

    Uses whichever glove currently has
    the larger amount of motion.
    """

    left = left_motion_score(row)

    right = right_motion_score(row)

    return max(
        left,
        right
    )