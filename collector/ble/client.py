import asyncio
from bleak import BleakClient
from collector.config import CHARACTERISTIC_UUID
from collector.ble.parser import parse


class BoxingBLEClient:

    def __init__(self, device):
        self.device = device

    async def run(self, on_packet):

        async with BleakClient(self.device) as client:

            print("Connected!")

            def handler(sender, data):
                packet = parse(data)
                if packet:
                    on_packet(packet)

            await client.start_notify(
                CHARACTERISTIC_UUID,
                handler
            )

            try:
                while True:
                    await asyncio.sleep(1)

            finally:
                print("Stopping notifications...")
                await client.stop_notify(CHARACTERISTIC_UUID)
                print("Disconnecting...")