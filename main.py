import random
import subprocess
import time
from datetime import datetime, timedelta
from config import logging

logger = logging.getLogger(__name__)

adb_commands = [
    "-s {device} shell sendevent /dev/input/event4 3 53 15079",
    "-s {device} shell sendevent /dev/input/event4 3 54 19612",
    "-s {device} shell sendevent /dev/input/event4 0 2 0",
    "-s {device} shell sendevent /dev/input/event4 0 0 0",
    "-s {device} shell sendevent /dev/input/event4 0 2 0",
    "-s {device} shell sendevent /dev/input/event4 0 0 0",
]


def adb(command: str, capture_output: bool = True):
    return subprocess.run(f"adb {command}", capture_output=capture_output)


def get_devices_with_resolutions() -> list[list[str]] | list:
    """
    Find all devices with their resolutions.
    :return: list of lists of devices with resolutions.
    """
    result = adb("devices").stdout.decode("utf-8").split()
    devices = [[el] for el in result if el not in ("List", "of", "devices", "attached", "device")]
    if not devices:
        logger.error("No devices found")
        return []
    for i in range(len(devices)):
        resolution = adb(f"-s {devices[i][0]} shell wm size").stdout.decode("utf-8").split()[-1].split("x")
        devices[i].extend([int(resolution[0]), int(resolution[1])])
    return devices


def start() -> None:
    """
    The entry poing of app
    """
    devices_with_resolutions = get_devices_with_resolutions()
    if not devices_with_resolutions:
        return
    logger.info(f"Devices' list: {devices_with_resolutions}")
    start_time = datetime.now()
    while True:
        for device_with_resolutions in devices_with_resolutions:
            x, y = (random.randint(device_with_resolutions[1] // 2.4, device_with_resolutions[1] // 1.44),
                    random.randint(device_with_resolutions[2] // 1.4, device_with_resolutions[2] // 1.34))
            subprocess.Popen(["adb", "-s", device_with_resolutions[0], "shell", "input", "tap", str(x), str(y)])
            time.sleep(0.05)
        if datetime.now() - start_time >= timedelta(minutes=2, seconds=10):
            time.sleep(670)


if __name__ == "__main__":
    start()
