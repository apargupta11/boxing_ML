import numpy as np


FEATURE_NAMES = [

    "mean",
    "std",
    "min",
    "max",
    "range",
    "rms",
    "energy",
]


SENSOR_COLUMNS = [

    "L_ax",
    "L_ay",
    "L_az",

    "L_gx",
    "L_gy",
    "L_gz",

    "R_ax",
    "R_ay",
    "R_az",

    "R_gx",
    "R_gy",
    "R_gz",

    # Resultant Signals
    "L_acc_mag",
    "L_gyro_mag",
    "R_acc_mag",
    "R_gyro_mag",
]


def extract_features(windows):

    """
    Input
    -----
    windows : (N, WINDOW_SIZE, 12)

    Output
    ------
    Feature Matrix : (N,112)
    """

    print("\n===================================")
    print("FEATURE ENGINEERING")
    print("===================================\n")

    feature_vectors = []

    feature_names = []

    # -----------------------------------
    # Create Feature Names
    # -----------------------------------

    for sensor in SENSOR_COLUMNS:

        for feature in FEATURE_NAMES:

            feature_names.append(
                f"{sensor}_{feature}"
            )

    # -----------------------------------
    # Feature Extraction
    # -----------------------------------

    for window in windows:

        # Original Signals
        signals = []

        for i in range(window.shape[1]):

            signals.append(window[:, i])

        # -----------------------------------
        # Left Acceleration Magnitude
        # -----------------------------------

        L_acc_mag = np.sqrt(

            window[:, 0] ** 2 +
            window[:, 1] ** 2 +
            window[:, 2] ** 2

        )

        # -----------------------------------
        # Left Gyroscope Magnitude
        # -----------------------------------

        L_gyro_mag = np.sqrt(

            window[:, 3] ** 2 +
            window[:, 4] ** 2 +
            window[:, 5] ** 2

        )

        # -----------------------------------
        # Right Acceleration Magnitude
        # -----------------------------------

        R_acc_mag = np.sqrt(

            window[:, 6] ** 2 +
            window[:, 7] ** 2 +
            window[:, 8] ** 2

        )

        # -----------------------------------
        # Right Gyroscope Magnitude
        # -----------------------------------

        R_gyro_mag = np.sqrt(

            window[:, 9] ** 2 +
            window[:, 10] ** 2 +
            window[:, 11] ** 2

        )

        signals.extend([

            L_acc_mag,
            L_gyro_mag,
            R_acc_mag,
            R_gyro_mag

        ])

        # -----------------------------------
        # Extract Statistical Features
        # -----------------------------------

        features = []

        for signal in signals:

            features.extend([

                np.mean(signal),

                np.std(signal),

                np.min(signal),

                np.max(signal),

                np.max(signal) - np.min(signal),

                np.sqrt(np.mean(signal ** 2)),

                np.sum(signal ** 2),

            ])

        feature_vectors.append(features)

    feature_vectors = np.array(feature_vectors)

    print(f"[INFO] Samples  : {feature_vectors.shape[0]}")
    print(f"[INFO] Features : {feature_vectors.shape[1]}")

    return feature_vectors, feature_names