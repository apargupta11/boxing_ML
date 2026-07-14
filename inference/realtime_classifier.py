from inference.motion_segmenter import MotionSegmenter
from inference.predictor import Predictor


class RealtimeClassifier:

    def __init__(self):

        print("\n===================================")
        print("REALTIME CLASSIFIER")
        print("===================================\n")

        self.segmenter = MotionSegmenter()

        self.predictor = Predictor()

    # ==================================================
    # Process One BLE Packet
    # ==================================================

    def process(self, packet):

        """
        Parameters
        ----------
        packet : dict

        Returns
        -------
        prediction dictionary or None
        """

        # -----------------------------------
        # Segment Motion
        # -----------------------------------

        segment = self.segmenter.process(
            packet
        )

        if segment is None:

            return None

        # -----------------------------------
        # Predict Punch
        # -----------------------------------

        prediction = self.predictor.predict(
            segment
        )

        self.print_prediction(
            prediction
        )

        return prediction

    # ==================================================
    # Print Prediction
    # ==================================================

    def print_prediction(
        self,
        prediction
    ):

        print("\n===================================")
        print("PUNCH DETECTED")
        print("===================================")

        print(f"Prediction      : {prediction['label']}")

        print(f"Confidence      : {prediction['confidence']:.2%}")

        print(f"Peak Motion     : {prediction['peak_motion']:.2f}")

        print(f"Duration        : {prediction['duration_packets']} packets")

        print(f"Trigger Hand    : {prediction['trigger_hand']}")

        print("===================================\n")