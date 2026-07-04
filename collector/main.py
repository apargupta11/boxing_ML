import asyncio

from collector.ble.scanner import scan
from collector.ble.client import BoxingBLEClient

from collector.recorder.csv_writer import CSVWriter
from collector.recorder.event_writer import EventWriter
from collector.recorder.punch_detector import PunchDetector
from collector.recorder.event_manager import EventManager

from collector.ui.popup_worker import PopupWorker
from preprocessing.pipeline import process


# ------------------------
# Initialize components
# ------------------------

csv_writer = CSVWriter()
event_writer = EventWriter()

detector = PunchDetector()
event_manager = EventManager()

popup_worker = PopupWorker(event_writer)


# ------------------------
# BLE Callback
# ------------------------

def on_packet(packet):

    # Save every packet
    row = csv_writer.write(packet)

    # Detect punches
    punches = detector.detect(packet)

    # Create events
    for punch in punches:

        event = event_manager.create_event(
            hand=punch["hand"],
            row=row
        )

        print(f"Queued Event #{event['event_id']} ({event['hand']})")

        # Send event to popup thread
        popup_worker.add_event(event)


# ------------------------
# Main
# ------------------------

async def main():

    device = await scan()

    if device is None:
        print("Device not found.")
        return

    print(f"Found device: {device.name} ({device.address})")

    client = BoxingBLEClient(device)

    await client.run(on_packet)


# ------------------------
# Entry Point
# ------------------------

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nStopping collector...")

    finally:

        csv_writer.close()
        event_writer.close()

        process(
            csv_writer.path,
            event_writer.path
        )

        print("Collector Finished")