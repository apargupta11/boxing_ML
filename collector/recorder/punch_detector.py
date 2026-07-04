class PunchDetector:

    def __init__(self):

        self.last_left = 0
        self.last_right = 0

    def detect(self, packet):

        events = []

        left = packet["L"]["punch_cnt"]
        right = packet["R"]["punch_cnt"]

        if left > self.last_left:

            self.last_left = left

            events.append({
                "hand": "LEFT",
                "count": left
            })

        if right > self.last_right:

            self.last_right = right

            events.append({
                "hand": "RIGHT",
                "count": right
            })

        return events