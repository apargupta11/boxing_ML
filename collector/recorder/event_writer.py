import csv
import os
from datetime import datetime


class EventWriter:

    def __init__(self, save_dir="data/metadata"):

        os.makedirs(save_dir, exist_ok=True)

        filename = datetime.now().strftime(
            "session_%Y%m%d_%H%M%S_events.csv"
        )

        self.path = os.path.join(save_dir, filename)

        self.file = open(self.path, "w", newline="")

        self.writer = csv.writer(self.file)

        self.writer.writerow([
            "event_id",
            "start_row",
            "end_row",
            "hand",
            "label"
        ])

        print(f"Event file: {self.path}")

    def write_event(
        self,
        event_id,
        start_row,
        end_row,
        hand,
        label
    ):

        self.writer.writerow([
            event_id,
            start_row,
            end_row,
            hand,
            label
        ])

        self.file.flush()

    def close(self):

        self.file.close()