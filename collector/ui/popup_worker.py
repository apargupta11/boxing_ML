import queue
import threading

from collector.ui.label_popup import LabelPopup


class PopupWorker:

    def __init__(self, event_writer):

        self.queue = queue.Queue()

        self.popup = LabelPopup()

        self.event_writer = event_writer

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

    def add_event(self, event):

        self.queue.put(event)

    def run(self):

        while True:

            event = self.queue.get()

            label = self.popup.ask(event)

            self.event_writer.write_event(

                event_id=event["event_id"],
                start_row=event["start_row"],
                end_row=event["start_row"],

                hand=event["hand"],

                label=label

            )

            self.queue.task_done()