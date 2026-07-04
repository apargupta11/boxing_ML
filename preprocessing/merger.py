import csv
import os


def merge(raw_path, event_path, output_dir="data/processed"):

    os.makedirs(output_dir, exist_ok=True)

    # Output filename
    raw_name = os.path.basename(raw_path)
    output_path = os.path.join(output_dir, raw_name)

    # ----------------------------
    # Load events
    # ----------------------------

    events = []

    with open(event_path, "r", newline="") as f:

        reader = csv.DictReader(f)

        for row in reader:

            events.append({
                "event_id": int(row["event_id"]),
                "start_row": int(row["start_row"]),
                "end_row": int(row["end_row"]),
                "hand": row["hand"],
                "label": row["label"]
            })

    # ----------------------------
    # Merge
    # ----------------------------

    with open(raw_path, "r", newline="") as raw_file, \
         open(output_path, "w", newline="") as out_file:

        reader = csv.reader(raw_file)
        writer = csv.writer(out_file)

        # Read header
        header = next(reader)

        header.extend([
            "event_id",
            "hand",
            "label"
        ])

        writer.writerow(header)

        # Row numbers start after header
        for row_number, row in enumerate(reader, start=1):

            event_id = -1
            hand = ""
            label = "UNKNOWN"

            for event in events:

                if event["start_row"] <= row_number <= event["end_row"]:

                    event_id = event["event_id"]
                    hand = event["hand"]
                    label = event["label"]

                    break

            row.extend([
                event_id,
                hand,
                label
            ])

            writer.writerow(row)

    print("Merged dataset created:")
    print(output_path)

    return output_path