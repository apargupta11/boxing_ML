class EventManager:

    def __init__(self):

        self.next_event_id = 1
        self.active_events = []

    def create_event(self, hand, row):

        event = {
            "event_id": self.next_event_id,
            "hand": hand,
            "start_row": row,
            "end_row": None,
            "label": "UNKNOWN"
        }

        self.next_event_id += 1

        self.active_events.append(event)

        return event

    def close_event(self, event_id, end_row):

        for event in self.active_events:

            if event["event_id"] == event_id:

                event["end_row"] = end_row

                self.active_events.remove(event)

                return event

        return None

    def get_active_events(self):

        return self.active_events