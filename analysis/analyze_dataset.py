import pandas as pd


def analyze(training_path):

    print("\n===================================")
    print("DATASET ANALYSIS")
    print("===================================\n")

    df = pd.read_csv(training_path)

    # ----------------------------------
    # Dataset Information
    # ----------------------------------

    print("Dataset Information")
    print("-------------------")

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    # ----------------------------------
    # Column Names
    # ----------------------------------

    print("\nColumn Names")
    print("-------------------")

    for col in df.columns:
        print(f"- {col}")

    # ----------------------------------
    # Missing Values
    # ----------------------------------

    print("\nMissing Values")
    print("-------------------")

    print(df.isnull().sum())

    # ----------------------------------
    # Activity Distribution
    # ----------------------------------

    print("\nActivity Label Distribution")
    print("---------------------------")

    print(df["activity_label"].value_counts())

    # ----------------------------------
    # Sensor Statistics
    # ----------------------------------

    sensor_columns = [
        "L_ax", "L_ay", "L_az",
        "L_gx", "L_gy", "L_gz",
        "R_ax", "R_ay", "R_az",
        "R_gx", "R_gy", "R_gz"
    ]

    print("\nSensor Statistics")
    print("---------------------------")

    print(df[sensor_columns].describe())

    print("\n===================================")
    print("DATASET ANALYSIS COMPLETE")
    print("===================================\n")