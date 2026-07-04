import csv
import os
from datetime import datetime


class CSVWriter:

    def __init__(self, save_dir="data/raw"):

        os.makedirs(save_dir, exist_ok=True)

        filename = datetime.now().strftime("session_%Y%m%d_%H%M%S.csv")

        self.path = os.path.join(save_dir, filename)

        self.file = open(self.path, "w", newline="")

        self.writer = csv.writer(self.file)

        self.row_number = 0

        self.writer.writerow([
            "timestamp",

            "L_ax", "L_ay", "L_az",
            "L_gx", "L_gy", "L_gz",

            "R_ax", "R_ay", "R_az",
            "R_gx", "R_gy", "R_gz",

            "L_punch_cnt",
            "R_punch_cnt",

            "label"
        ])

        print(f"\nSaving to:\n{self.path}\n")

    def write(self, packet, label="UNKNOWN"):

        try:

            left = packet["L"]
            right = packet["R"]

            self.writer.writerow([

                packet["ts"],

                left["ax"],
                left["ay"],
                left["az"],

                left["gx"],
                left["gy"],
                left["gz"],

                right["ax"],
                right["ay"],
                right["az"],

                right["gx"],
                right["gy"],
                right["gz"],

                left["punch_cnt"],
                right["punch_cnt"],

                label
            ])

            self.file.flush()

            self.row_number += 1

            return self.row_number

        except Exception as e:

            print("\n========== BAD PACKET ==========")
            print(packet)
            print("Exception:", type(e).__name__, e)

            if "L" in packet:
                print("Left Keys:", packet["L"].keys())

            if "R" in packet:
                print("Right Keys:", packet["R"].keys())

            print("================================\n")

            return -1

    def close(self):

        self.file.close()