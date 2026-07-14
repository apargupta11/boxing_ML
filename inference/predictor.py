import os
import joblib
import numpy as np

from collector.config import MODEL_DIR
from preprocessing.feature_engineering import extract_features


LABEL_MAP = {
    0: "NO_PUNCH",
    1: "LEFT_PUNCH",
    2: "RIGHT_PUNCH",
}


class Predictor:

    def __init__(self):

        model_path = os.path.join(
            MODEL_DIR,
            "best_model.pkl"
        )

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        print("\n===================================")
        print("LOADING MODEL")
        print("===================================\n")

        self.model = joblib.load(model_path)

        print(f"Loaded : {model_path}")

    # ====================================================
    # Predict
    # ====================================================

    def predict(self, segment):
        """
        Parameters
        ----------
        segment : dict

        {
            "window": ndarray,
            "peak_motion": ...,
            "peak_index": ...,
            "trigger_hand": ...,
            "duration_packets": ...
        }

        Returns
        -------
        dict
        """

        # -------------------------------
        # Extract window
        # -------------------------------

        window = segment["window"]

        windows = np.expand_dims(
            window,
            axis=0
        )

        # -------------------------------
        # Feature Engineering
        # -------------------------------

        features, _ = extract_features(
            windows
        )

        # -------------------------------
        # Prediction
        # -------------------------------

        prediction = self.model.predict(
            features
        )[0]

        probability = self.model.predict_proba(
            features
        )[0]

        confidence = float(np.max(probability))

        return {

            "class": int(prediction),

            "label": LABEL_MAP[prediction],

            "confidence": confidence,

            "probabilities": probability,

            "peak_motion": segment["peak_motion"],

            "peak_index": segment["peak_index"],

            "trigger_hand": segment["trigger_hand"],

            "duration_packets": segment["duration_packets"]

        }

    # ====================================================
    # Pretty Prediction
    # ====================================================

    def predict_name(self, segment):

        result = self.predict(segment)

        return (

            result["label"],

            result["confidence"]

        )