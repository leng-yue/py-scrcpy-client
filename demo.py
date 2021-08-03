import cv2
import scrcpy

client = scrcpy.Client(adb_path="adb/adb.exe", max_width=800, max_fps=60)


def mouse_click(event, x, y, flags, param):
    # Bind left button
    if event == cv2.EVENT_LBUTTONDOWN:
        client.event.touch(x, y, scrcpy.ACTION_DOWN)
        mouse_down = True
    if event == cv2.EVENT_LBUTTONUP:
        client.event.touch(x, y, scrcpy.ACTION_UP)
        mouse_down = False
    if event == cv2.EVENT_MOUSEMOVE:
        client.event.touch(x, y, scrcpy.ACTION_MOVE)

    # Bind right button to home
    if event == cv2.EVENT_RBUTTONDOWN:
        client.event.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
    if event == cv2.EVENT_RBUTTONUP:
        client.event.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)


cv2.namedWindow("game")
cv2.setMouseCallback('game', mouse_click)


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


def listener(frame):
    if frame is not None:
        cv2.imshow('game', frame)
    code = map_code(cv2.waitKey(10))
    if code != -1:
        client.event.keycode(code, scrcpy.ACTION_DOWN)
        client.event.keycode(code, scrcpy.ACTION_UP)


client.add_listener(listener)
client.listen()
