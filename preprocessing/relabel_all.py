import os

from collector.config import (
    RAW_DATA_DIR,
    METADATA_DIR,
    TRAINING_DIR,
)

from preprocessing.window_labeler import WindowLabeler


def relabel_all():

    print("\n===================================")
    print("RELABELING ALL SESSIONS")
    print("===================================\n")

    os.makedirs(TRAINING_DIR, exist_ok=True)

    labeler = WindowLabeler()

    raw_files = sorted(os.listdir(RAW_DATA_DIR))

    processed = 0
    skipped = 0

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

            print(f"[SKIP] {event_name} not found")

            skipped += 1

            continue

        print(f"Processing : {raw_file}")

        labeler.process(
            raw_path=raw_path,
            event_path=event_path,
            output_dir=TRAINING_DIR
        )

        processed += 1

    print("\n===================================")
    print("RELABELING COMPLETE")
    print("===================================")
    print(f"Processed : {processed}")
    print(f"Skipped   : {skipped}")
    print("===================================\n")

   

def main():

    relabel_all()


if __name__ == "__main__":

    main()