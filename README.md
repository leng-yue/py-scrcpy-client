# py android viewer

This package allows you to get video stream from android device.

Stream frames already converted to numpy array using [PyAV](https://github.com/mikeboers/PyAV)

Also this package allows you to send touch events to devices.


### How it works
I am using [scrcpy](https://github.com/Genymobile/scrcpy) server and connect to two sockets, video and control sockets.
Video stream has almost no delay because i am not using separate process of `ffmpeg` and use direct bindings to `ffmpeg` to decode video.

### Requirements 
[PyAV](http://docs.mikeboers.com/pyav/develop/overview/installation.html)

[ffmpeg](http://ffmpeg.org/)



### Examples
```python
import cv2
from viewer import AndroidViewer

# This will deploy and run server on android device connected to USB
android = AndroidViewer()

while True:
    frames = android.get_next_frames()
    if frames is None:
        continue
    
    for frame in frames:
        cv2.imshow('game', frame)
        cv2.waitKey(1)
```

Send swipe event:
```python
    android = AndroidViewer()
    android.swipe(start_x, start_y, end_x, end_y)   
```

# Doc
https://github.com/Genymobile/scrcpy/blob/v1.12.1/server/src/main/java/com/genymobile/scrcpy/ControlMessageReader.java