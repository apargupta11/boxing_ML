import os
import joblib
import numpy as np

from collector.config import MODEL_DIR
from preprocessing.feature_engineering import extract_features


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
    # Predict One Motion Segment
    # ====================================================

    def predict(self, segment):

        """
        Parameters
        ----------
        segment : np.ndarray

        Shape:
            (window_size, 12)

        Returns
        -------
        prediction : int

            0 = No Punch
            1 = Left Punch
            2 = Right Punch
        """

        # -------------------------------
        # Feature Engineering
        # -------------------------------

        windows = np.array([segment])

        features, _ = extract_features(
            windows
        )

        # -------------------------------
        # Predict
        # -------------------------------

        prediction = self.model.predict(
            features
        )[0]

        probability = self.model.predict_proba(
            features
        )[0]

        return prediction, probability

    # ====================================================
    # Pretty Prediction
    # ====================================================

    def predict_name(self, segment):

        prediction, probability = self.predict(
            segment
        )

        label_map = {

            0: "NO_PUNCH",

            1: "LEFT_PUNCH",

            2: "RIGHT_PUNCH"

        }
        # if prediction==0:
        #     return None
        

        return (

            label_map[prediction],

            probability

        )