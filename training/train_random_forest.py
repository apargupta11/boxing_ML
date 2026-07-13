import os
import numpy as np
import pandas as pd

from collector.config import (
    MASTER_DATA_DIR,
    WINDOW_BEFORE,
    WINDOW_AFTER,
    WINDOW_STRIDE,
)

from training.utils import get_window
from preprocessing.feature_engineering import extract_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
import joblib

from collector.config import MODEL_DIR
from training.model_manager import save_best_model


# ====================================================
# Sensor Columns
# ====================================================

SENSOR_COLUMNS = [

    "L_ax",
    "L_ay",
    "L_az",

    "L_gx",
    "L_gy",
    "L_gz",

    "R_ax",
    "R_ay",
    "R_az",

    "R_gx",
    "R_gy",
    "R_gz",
]


# ====================================================
# Load Dataset
# ====================================================

def load_dataset(master_dataset_path=None):

    if master_dataset_path is None:

        master_dataset_path = os.path.join(
            MASTER_DATA_DIR,
            "master_dataset.csv"
        )

    print("\n===================================")
    print("LOADING MASTER DATASET")
    print("===================================\n")

    df = pd.read_csv(master_dataset_path)

    print(f"[INFO] Dataset Loaded")
    print(f"[INFO] Rows : {len(df)}")
    print(f"[INFO] Columns : {len(df.columns)}")

    return df


# ====================================================
# Create Sliding Windows
# ====================================================

def create_windows(df):

    print("\n===================================")
    print("CREATING SLIDING WINDOWS")
    print("===================================\n")

    windows = []
    labels = []

    for center in range(
        WINDOW_BEFORE,
        len(df) - WINDOW_AFTER,
        WINDOW_STRIDE
    ):

        window = get_window(
            df=df,
            center_idx=center,
            before=WINDOW_BEFORE,
            after=WINDOW_AFTER,
            sensor_columns=SENSOR_COLUMNS
        )

        label = int(df.iloc[center]["activity_label"])

        windows.append(window)
        labels.append(label)

    windows = np.array(windows)
    labels = np.array(labels)

    print(f"[INFO] Windows Created : {len(windows)}")

    return windows, labels


# ====================================================
# Print Dataset Statistics
# ====================================================

def print_statistics(windows, labels):

    print("\n===================================")
    print("WINDOW DATASET SUMMARY")
    print("===================================\n")

    print("Window Dataset Shape :", windows.shape)
    print("One Window Shape     :", windows[0].shape)
    print("Labels Shape         :", labels.shape)

    unique, counts = np.unique(
        labels,
        return_counts=True
    )

    print("\nLabel Distribution")

    for label, count in zip(unique, counts):

        print(f"Label {label} : {count}")

    print("\nExample Label :", labels[0])

    print("\n===================================")
    print("WINDOW CREATION COMPLETE")
    print("===================================\n")


# ====================================================
# Random Forest Training Pipeline
# ====================================================

def train_random_forest(master_dataset_path=None):

    print("\n===================================")
    print("RANDOM FOREST TRAINING")
    print("===================================\n")

    # ----------------------------------
    # Step 1 : Load Dataset
    # ----------------------------------

    df = load_dataset(master_dataset_path)

    # ----------------------------------
    # Step 2 : Create Sliding Windows
    # ----------------------------------

    windows, labels = create_windows(df)

    print_statistics(
        windows,
        labels
    )

    # ----------------------------------
    # Step 3 : Feature Engineering
    # ----------------------------------

    features, feature_names = extract_features(windows)

    # ----------------------------------
    # Step 4 : Train/Test Split
    # ----------------------------------

    print("\n===================================")
    print("TRAIN / TEST SPLIT")
    print("===================================\n")

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.20,
        random_state=42,
        stratify=labels
    )

    print(f"Training Samples : {len(X_train)}")
    print(f"Testing Samples  : {len(X_test)}")

    # ----------------------------------
    # Step 5 : Train Random Forest
    # ----------------------------------

    print("\n===================================")
    print("TRAINING RANDOM FOREST")
    print("===================================\n")

    model = RandomForestClassifier(
        n_estimators=1000,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Model training complete.")

    # ----------------------------------
    # Step 6 : Evaluate Model
    # ----------------------------------

    print("\n===================================")
    print("MODEL EVALUATION")
    print("===================================\n")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Accuracy : {accuracy*100:.2f}%")

    print("\nClassification Report\n")
    
    report = classification_report(

    y_test,

    predictions,

    output_dict=True

)

    print(

    classification_report(

        y_test,

        predictions

    )

)

    print("Confusion Matrix\n")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    # ----------------------------------
    # Step 7 : Feature Importance
    # ----------------------------------

    print("\n===================================")
    print("TOP 20 IMPORTANT FEATURES")
    print("===================================\n")

    importance = sorted(
        zip(
            feature_names,
            model.feature_importances_
        ),
        key=lambda x: x[1],
        reverse=True
    )

    for name, score in importance[:20]:
        print(f"{name:20s} {score:.5f}")

    # ----------------------------------
    # Step 8 : Save Model
    # ----------------------------------

    print("\n===================================")
    print("SAVING MODEL")
    print("===================================\n")

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model_path = os.path.join(
        MODEL_DIR,
        "random_forest.pkl"
    )

    joblib.dump(
        model,
        model_path
    )
    
    save_best_model(
    model_path=model_path,
    accuracy=accuracy,
    report=report,
    model_dir=MODEL_DIR
)
    

    print(f"Model saved to : {model_path}")

    print("\n===================================")
    print("TRAINING COMPLETE")
    print("===================================\n")

    return model_path   


# ====================================================
# Standalone Testing
# ====================================================

def main():

    train_random_forest()


if __name__ == "__main__":

    main()