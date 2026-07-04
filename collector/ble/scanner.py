from bleak import BleakScanner
from collector.config import DEVICE_NAME


async def scan():
    devices = await BleakScanner.discover(timeout=5)
    return next((d for d in devices if d.name == DEVICE_NAME), None)