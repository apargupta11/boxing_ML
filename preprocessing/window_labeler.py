import csv
import os

from collector.config import (
    LABEL_MAP,
    TRAINING_DIR,
    WINDOW_BEFORE,
    WINDOW_AFTER,
)

from preprocessing.motion_segmenter import (
    segment_punch
)


class WindowLabeler:

    def __init__(self):

        self.before = WINDOW_BEFORE
        self.after = WINDOW_AFTER

    def process(
        self,
        raw_path,
        event_path,
        output_dir=TRAINING_DIR
    ):

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        output_path = os.path.join(
            output_dir,
            os.path.basename(raw_path)
        )

        # ----------------------------------
        # Read Raw CSV
        # ----------------------------------

        with open(raw_path, "r", newline="") as f:

            reader = csv.reader(f)

            header = next(reader)

            rows = list(reader)

        # ----------------------------------
        # Default labels
        # ----------------------------------

        labels = [

            LABEL_MAP["NONE"]

            for _ in rows

        ]

        # ----------------------------------
        # Read Event CSV
        # ----------------------------------

        with open(event_path, "r", newline="") as f:

            reader = csv.DictReader(f)

            for event in reader:

                trigger = int(event["start_row"]) - 1

                hand = event["hand"].strip().upper()

                label = LABEL_MAP.get(
                    hand,
                    LABEL_MAP["NONE"]
                )

                # ----------------------------------
                # Segment Punch
                # ----------------------------------

                try:

                    start, end = segment_punch(

                        rows=rows,

                        trigger=trigger,

                        hand=hand

                    )

                except Exception:

                    # ----------------------------------
                    # Fallback to old fixed window
                    # ----------------------------------

                    start = max(
                        0,
                        trigger - self.before
                    )

                    end = min(
                        len(rows) - 1,
                        trigger + self.after
                    )

                # ----------------------------------
                # Apply Label
                # ----------------------------------

                for i in range(
                    start,
                    end + 1
                ):

                    labels[i] = label

        # ----------------------------------
        # Save Training CSV
        # ----------------------------------

        with open(
            output_path,
            "w",
            newline=""
        ) as f:

            writer = csv.writer(f)

            writer.writerow(

                header + [
                    "activity_label"
                ]

            )

            for row, label in zip(
                rows,
                labels
            ):

                writer.writerow(
                    row + [label]
                )

        print("\n======================================")
        print("Training dataset created successfully!")

        print(f"Saved to : {output_path}")

        print("======================================\n")

        return output_path