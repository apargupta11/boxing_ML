from merge_events import merge

merge(

    raw_file="data/raw/session.csv",

    events_file="data/metadata/session_events.csv",

    output_file="data/processed/merged.csv"

)