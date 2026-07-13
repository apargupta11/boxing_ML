import json
import os
import shutil


def save_best_model(
    model_path,
    accuracy,
    report,
    model_dir
):

    metrics_path = os.path.join(
        model_dir,
        "metrics.json"
    )

    best_model_path = os.path.join(
        model_dir,
        "best_model.pkl"
    )

    # -----------------------------
    # First model
    # -----------------------------

    if not os.path.exists(metrics_path):

        shutil.copy(
            model_path,
            best_model_path
        )

        metrics = {

            "accuracy": accuracy,

            "macro_f1":
                report["macro avg"]["f1-score"],

            "weighted_f1":
                report["weighted avg"]["f1-score"]

        }

        with open(metrics_path, "w") as f:

            json.dump(
                metrics,
                f,
                indent=4
            )

        print("\nNo previous model found.")
        print("Saved as BEST MODEL.")

        return True

    # -----------------------------
    # Compare
    # -----------------------------

    with open(metrics_path) as f:

        old_metrics = json.load(f)

    old_score = old_metrics["macro_f1"]

    new_score = report[
        "macro avg"
    ]["f1-score"]

    print("\n==============================")
    print("MODEL COMPARISON")
    print("==============================")

    print(f"Old Macro F1 : {old_score:.4f}")
    print(f"New Macro F1 : {new_score:.4f}")

    if new_score > old_score:

        shutil.copy(
            model_path,
            best_model_path
        )

        metrics = {

            "accuracy": accuracy,

            "macro_f1":
                report["macro avg"]["f1-score"],

            "weighted_f1":
                report["weighted avg"]["f1-score"]

        }

        with open(metrics_path, "w") as f:

            json.dump(
                metrics,
                f,
                indent=4
            )

        print("\nNew model is BETTER.")
        print("Best model updated.")

        return True

    print("\nOld model is still BETTER.")
    print("Keeping previous model.")

    return False