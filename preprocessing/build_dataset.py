import os

from preprocessing.window_labeler import WindowLabeler

from collector.config import (
    RAW_DATA_DIR,
    METADATA_DIR,
)


def main():

    labeler = WindowLabeler()

    raw_files = sorted(os.listdir(RAW_DATA_DIR))

    for raw_file in raw_files:

        if not raw_file.endswith(".csv"):
            continue

        raw_path = os.path.join(
            RAW_DATA_DIR,
            raw_file
        )

        event_name = raw_file.replace(
            ".csv",
            "_events.csv"
        )

        event_path = os.path.join(
            METADATA_DIR,
            event_name
        )

        if not os.path.exists(event_path):

            print(f"Missing metadata: {event_name}")
            continue

        print(f"\nProcessing {raw_file}")

        labeler.process(
            raw_path,
            event_path
        )

    print("\nDataset rebuild complete.")


if __name__ == "__main__":

    main()