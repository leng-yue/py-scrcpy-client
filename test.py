import cv2
import time
from viewer import AndroidViewer

# This will deploy and run server on android device connected to USB
android = AndroidViewer(adb_path="adb/adb.exe", max_width=800, max_fps=60)
last_move = 0
mouse_down = False


def mouse_click(event, x, y, flags, param):
    global last_move, mouse_down
    if event == cv2.EVENT_LBUTTONDOWN:
        android.send_event(x, y, android.ACTION_DOWN)
        mouse_down = True
    if event == cv2.EVENT_LBUTTONUP:
        android.send_event(x, y, android.ACTION_UP)
        mouse_down = False
    if event == cv2.EVENT_MOUSEMOVE and mouse_down:
        if time.time_ns() - last_move < 1e8:
            return
        last_move = time.time_ns()
        android.send_event(x, y, android.ACTION_MOVE)
    if event == cv2.EVENT_RBUTTONDOWN:
        android.send_key_event(3, android.ACTION_DOWN)
    if event == cv2.EVENT_RBUTTONUP:
        android.send_key_event(3, android.ACTION_UP)


cv2.namedWindow("game")
cv2.setMouseCallback('game', mouse_click)


def listener(frame):
    if frame is not None:
        cv2.imshow('game', frame)
    cv2.waitKey(1)


android.add_listener(listener)
android.listen()
