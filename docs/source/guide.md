# Guide

In this article, you will learn to use this project in 10 minutes.

## ADB connection
Since this project depends on [adbutils](https://github.com/openatx/adbutils), 
user don't have to download adb manually on windows and macos.  
However, **linux users still need to install adb manually**. 
- Debian user can use `apt install adb` to install ADB.

```python
import scrcpy
# If you already know the device serial
client = scrcpy.Client(device="DEVICE SERIAL")
# You can also pass an ADBClient instance to it
from adbutils import adb
adb.connect("127.0.0.1:5555")
client = scrcpy.Client(device=adb.devices()[0])
```

For more information, you should go to [adbutils's webpage](https://github.com/openatx/adbutils).

## Bind events
This project's core follow event sender and receiver structure.
This means you can add multiple listener to the same stream.

```python
import cv2

def on_frame(self):
    # If you set non-blocking (default) in constructor, the frame event receiver 
    # may receive None to avoid blocking event.
    if frame is not None:
        # frame is an bgr numpy ndarray (cv2' default format)
        cv2.imshow("viz", frame)
    cv2.waitKey(10)

client.add_listener(scrcpy.EVENT_FRAME, on_frame)
```

[Optional] You can also add a listener to listen the `init` event.
```python
def on_init(self):
    # Print device name
    print(self.client.device_name)
client.add_listener(scrcpy.EVENT_INIT, on_init)
```

Then, you can start the client
```python
client.start()
```
[Optional] you can start the client with `threaded=True`, then the frame loop will be executed in a new thread, 
and the main thread won't be blocked.
```python
client.start(threaded=True)
```

## Send actions
You can find all actions in the `API:scrcpy.control` submodule.  

The core will create a control instance to itself automatically.  
For example, you can send a touch event by
```python
# Mousedown
client.control.touch(100, 200, scrcpy.ACTION_DOWN)
# Mouseup
client.control.touch(100, 200, scrcpy.ACTION_UP)
```

## Get device information
```python
# Resolution
client.resolution
# Screenshot / Last frame
client.last_frame
# Device Name
client.device_name
```

## Reduce CPU usage
You can use `max_width`, `bitrate`, and `max_fps` parameter to limit the bitrate of the video stream.  
After reducing the bitrate of video stream, the H264 decoder can save much CPU resources.  
This is very helpful when you don't need a 10 ms level experience. (You probably only need 5 fps in most automation).  
