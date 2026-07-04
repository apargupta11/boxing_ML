import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "ESP32_RIGHT_RELAY"
CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


def notification_handler(sender, data):
    try:
        print(data.decode())
    except Exception:
        print(data)


async def main():

    devices = await BleakScanner.discover(timeout=5)

    device = next((d for d in devices if d.name == DEVICE_NAME), None)

    if device is None:
        print("Device not found")
        return

    async with BleakClient(device) as client:

        print("Connected!")

        await client.start_notify(
            CHAR_UUID,
            notification_handler
        )

        print("\nReceiving data...\n")
     

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())