import asyncio

from collector.ble.scanner import scan
from collector.ble.client import BoxingBLEClient

from inference.realtime_classifier import (
    RealtimeClassifier,
)


classifier = RealtimeClassifier()


def on_packet(packet):

    prediction = classifier.process(packet)

    if prediction is None:
        return

    print()

    print("=" * 40)

    print(f"Punch       : {prediction['label']}")

    print(f"Confidence  : {prediction['confidence']:.2%}")

    print(f"Peak Motion : {prediction['peak_motion']:.2f}")

    print("=" * 40)


async def main():

    device = await scan()

    if device is None:

        print("Device not found.")

        return

    print(f"Connected to {device.name}")

    client = BoxingBLEClient(device)

    await client.run(on_packet)


if __name__ == "__main__":

    asyncio.run(main())