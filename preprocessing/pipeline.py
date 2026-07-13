from preprocessing.window_labeler import WindowLabeler
from analysis.analyze_dataset import analyze
from training.dataset_builder import build_master_dataset
from training.train_random_forest import train_random_forest

def process(raw_path, event_path):

    print("\n===================================")
    print("STARTING PREPROCESSING")
    print("===================================\n")

    # ----------------------------------
    # Step 1: Window Labeling
    # ----------------------------------

    labeler = WindowLabeler()

    training_path = labeler.process(
        raw_path,
        event_path
    )

    # ----------------------------------
    # Step 2: Dataset Analysis
    # ----------------------------------

    training_path = labeler.process(raw_path, event_path)

    analyze(training_path)

    master_dataset_path = build_master_dataset()

    model_path = train_random_forest(master_dataset_path)
 

    return master_dataset_path