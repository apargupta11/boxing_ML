import csv
import os

from collector.config import (
    LABEL_MAP,
    TRAINING_DIR,
)

from preprocessing.motion_segmenter import (
    segment_punch,
)


class WindowLabeler:

    # ====================================================
    # Create Training Dataset
    # ====================================================

    def process(
        self,
        raw_path,
        event_path,
        output_dir=TRAINING_DIR,
    ):

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

        output_path = os.path.join(
            output_dir,
            os.path.basename(raw_path),
        )

        # ----------------------------------
        # Read Raw CSV
        # ----------------------------------

        with open(raw_path, "r", newline="") as f:

            reader = csv.reader(f)

            header = next(reader)

            rows = list(reader)

        # ----------------------------------
        # Initialize Labels
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

                trigger = int(
                    event["start_row"]
                ) - 1

                hand = event[
                    "hand"
                ].strip().upper()

                label = LABEL_MAP.get(

                    hand,

                    LABEL_MAP["NONE"]

                )

                # ----------------------------------
                # Dynamic Motion Segmentation
                # ----------------------------------

                start, end = segment_punch(

                    rows=rows,

                    trigger=trigger,

                    hand=hand,

                )

                # ----------------------------------
                # Safety
                # ----------------------------------

                start = max(
                    0,
                    start,
                )

                end = min(
                    len(rows) - 1,
                    end,
                )

                # ----------------------------------
                # Apply Labels
                # ----------------------------------

                for i in range(
                    start,
                    end + 1,
                ):

                    labels[i] = label

        # ----------------------------------
        # Save Training CSV
        # ----------------------------------

        with open(
            output_path,
            "w",
            newline="",
        ) as f:

            writer = csv.writer(f)

            writer.writerow(

                header + [

                    "activity_label"

                ]

            )

            for row, label in zip(
                rows,
                labels,
            ):

                writer.writerow(
                    row + [label]
                )

        print("\n======================================")
        print("TRAINING DATASET CREATED")
        print("======================================")
        print(f"Rows  : {len(rows)}")
        print(f"Saved : {output_path}")
        print("======================================\n")

        return output_path