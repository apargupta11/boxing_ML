from preprocessing.merger import merge


def process(raw_path, event_path):

    print("\n========== PREPROCESSING ==========\n")

    merged_path = merge(
        raw_path,
        event_path
    )

    print("\n========== DONE ==========\n")

    return merged_path