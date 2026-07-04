import csv
import os


def extract_windows(
    raw_path,
    event_path,
    output_dir="data/processed/windows",
    before=20,
    after=20,
):

    os.makedirs(output_dir, exist_ok=True)

    # ----------------------------
    # Load raw csv
    # ----------------------------

    with open(raw_path, "r", newline="") as f:

        reader = csv.reader(f)

        header = next(reader)

        raw_rows = list(reader)

    # ----------------------------
    # Load events
    # ----------------------------

    with open(event_path, "r", newline="") as f:

        events = list(csv.DictReader(f))

    # ----------------------------
    # Extract each window
    # ----------------------------

    for event in events:

        trigger = int(event["start_row"])

        start = max(1, trigger - before)
        end = min(len(raw_rows), trigger + after)

        filename = f"event_{event['event_id']}.csv"

        output_path = os.path.join(output_dir, filename)

        with open(output_path, "w", newline="") as out:

            writer = csv.writer(out)

            writer.writerow(header)

            for row in raw_rows[start - 1:end]:

                writer.writerow(row)

        print(
            f"Created {filename} "
            f"({start} -> {end})"
        )