from typing import Optional

import click
import cv2
from adbutils import adb

import scrcpy

client: Optional[scrcpy.Client] = None


def mouse_click(event, x, y, flags, param):
    # Bind left button
    if event == cv2.EVENT_LBUTTONDOWN:
        client.control.touch(x, y, scrcpy.ACTION_DOWN)
    if event == cv2.EVENT_LBUTTONUP:
        client.control.touch(x, y, scrcpy.ACTION_UP)
    if event == cv2.EVENT_MOUSEMOVE:
        client.control.touch(x, y, scrcpy.ACTION_MOVE)

    # Bind right button to home
    if event == cv2.EVENT_RBUTTONDOWN:
        client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
    if event == cv2.EVENT_RBUTTONUP:
        client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)


# Mapping numbers, english chars, some other operations
def map_code(code):
    if code == -1:
        return -1
    if 48 <= code <= 57:
        return code - 48 + 7
    if 65 <= code <= 90:
        return code - 65 + 29
    if 97 <= code <= 122:
        return code - 97 + 29
    if code == 8:
        return 67
    if code == 32:
        return 62
    if code == 13:
        return 66
    if code == 91:
        client.control.text("test string")
    if code == 93:
        client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)
    return -1


def on_init():
    cv2.namedWindow("ui")
    cv2.setMouseCallback("ui", mouse_click)
    cv2.setWindowTitle("ui", client.device_name)


def on_frame(frame):
    if frame is not None:
        cv2.imshow("ui", frame)
    code = map_code(cv2.waitKey(10))

    if code != -1:
        client.control.keycode(code, scrcpy.ACTION_DOWN)
        client.control.keycode(code, scrcpy.ACTION_UP)


@click.command(help="A simple scrcpy client")
@click.option(
    "--max_width",
    default=800,
    show_default=True,
    help="Set max width of the window",
)
@click.option(
    "--device",
    help="Select device manually (device serial required)",
)
def main(max_width: int, device: Optional[str]):
    global client

    if device:
        device = adb.device(serial=device)
    elif len(adb.device_list()) > 1:
        devices = adb.device_list()
        print(
            "More than one device founded, please choice an android device to connect:"
        )
        for index, i in enumerate(devices):
            print(f"[{index}] {i.serial}")
        device = devices[int(input("Please type a number here:"))]

    # Setup client
    client = scrcpy.Client(max_width=max_width, device=device)
    client.add_listener(scrcpy.EVENT_INIT, on_init)
    client.add_listener(scrcpy.EVENT_FRAME, on_frame)
    client.start()


if __name__ == "__main__":
    main()
