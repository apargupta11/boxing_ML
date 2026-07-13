import os

import pandas as pd

from collector.config import (
    TRAINING_DIR,
    MASTER_DATA_DIR,
)


def build_master_dataset():

    print("\n===================================")
    print("BUILDING MASTER DATASET")
    print("===================================\n")

    os.makedirs(MASTER_DATA_DIR, exist_ok=True)

    dataframes = []

    files = sorted(os.listdir(TRAINING_DIR))

    for file in files:

        if not file.endswith(".csv"):
            continue

        path = os.path.join(
            TRAINING_DIR,
            file
        )

        print(f"Reading {file}")

        df = pd.read_csv(path)

        # Future:
        # df["session"] = file

        dataframes.append(df)

    if len(dataframes) == 0:

        raise Exception("No training files found.")

    master = pd.concat(
        dataframes,
        ignore_index=True
    )

    output_path = os.path.join(
        MASTER_DATA_DIR,
        "master_dataset.csv"
    )

    master.to_csv(
        output_path,
        index=False
    )

    print("\n===================================")
    print("MASTER DATASET CREATED")
    print(f"Rows : {len(master)}")
    print(f"Saved : {output_path}")
    print("===================================\n")

    return output_path


if __name__ == "__main__":
    build_master_dataset()