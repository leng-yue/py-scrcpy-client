import cv2
import scrcpy

client = scrcpy.Client(adb_path="adb/adb.exe", max_width=800)


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


# Mapping numbers, english chars, delete
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


if __name__ == "__main__":
    client.add_listener(scrcpy.EVENT_INIT, on_init)
    client.add_listener(scrcpy.EVENT_FRAME, on_frame)
    client.start()
