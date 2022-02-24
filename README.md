# Python Scrcpy Client

（本项目客隆自：[https://github.com/leng-yue/py-scrcpy-client](https://github.com/leng-yue/py-scrcpy-client)）

这个包允许你**使用Python**实时查看和控制安卓设备。

众所周知 Scrcpy([https://github.com/Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)) 是一个很强大的安卓设备控制开源程序，

无需Root，延迟低，效果强，控制效果好。

但是，原程序控制端是用c语言写的，编译也麻烦，二次开发不容易；

本项目使用python语言重新编写控制端，这样就很方便的使用python对手机进行操控了。

## 使用方法：

[(翻译自 https://leng-yue.github.io/py-scrcpy-client/guide.html)](https://leng-yue.github.io/py-scrcpy-client/guide.html) 修改了部分小错误

在本文中，您将在 10 分钟内学会使用该项目。

### 0. 安装

首先，您需要通过 pip 安装此软件包：

```bash
pip install scrcpy-client[ui]
```

然后，您可以启动 py-scrcpy 来查看演示：

* 注意：不想看demo ui的可以忽略[ui]

### 1. 连接手机¶


```python
import scrcpy
# If you already know the device serial
client = scrcpy.Client(device="DEVICE SERIAL")
# You can also pass an ADBClient instance to it
from adbutils import adb
adb.connect("127.0.0.1:5555")
client = scrcpy.Client(device=adb.devices()[0])
```

> 由于本项目依赖于 adbutils，所以用户无需在 windows 和 macOS 上手动下载 adb。

> **不过linux用户还是需要手动安装adb。**
> * Debian 用户可以使用 apt install adb 来安装 ADB。
> 获取更多信息，请访问 [adbutils&#39;s webpage](https://github.com/openatx/adbutils).

### 2. 绑定事件

该项目的核心遵循事件发送者和接收者结构。这意味着您可以将多个侦听器添加到同一流中。

```python
import cv2

def on_frame(frame):
    # If you set non-blocking (default) in constructor, the frame event receiver 
    # may receive None to avoid blocking event.
    if frame is not None:
        # frame is an bgr numpy ndarray (cv2' default format)
        cv2.imshow("viz", frame)
    cv2.waitKey(10)

client.add_listener(scrcpy.EVENT_FRAME, on_frame)
```

[可选] 你也可以添加一个监听器来监听 init 事件。

```python
def on_init():
    # Print device name
    print(client.device_name)
client.add_listener(scrcpy.EVENT_INIT, on_init)
```

然后就可以启动客户端了

```
client.start()
```

【可选】你可以用thread=True来启动客户端，那么frame loop会在一个新的线程中执行，主线程不会被阻塞。

```
client.start(threaded=True)
```

### 3. 发送动作

您可以在 [API:scrcpy.control 子模块](https://leng-yue.github.io/py-scrcpy-client/scrcpy.html#module-scrcpy.control) 中找到所有操作。
核心会自动为自己创建一个控制实例。
例如，您可以通过以下方式发送触摸事件

```
# Mousedown
client.control.touch(100, 200, scrcpy.ACTION_DOWN)
# Mouseup
client.control.touch(100, 200, scrcpy.ACTION_UP)
```

### 4. 获取设备信息

```
# Resolution
client.resolution
# Screenshot / Last frame
client.last_frame
# Device Name
client.device_name
```

### 5. 减少 CPU 使用率

您可以使用 max_width、bitrate 和 max_fps 参数来限制视频流的比特率。
在降低视频码流码率后，H264解码器可以节省大量的CPU资源。
当您不需要 10 毫秒级别的体验时，这非常有用。 （在大多数自动化中，您可能只需要 5 fps）。

## 原文档：

<p>
    <a href="https://pypi.org/project/scrcpy-client/" target="_blank">
        <img src="https://img.shields.io/pypi/v/scrcpy-client" />
    </a>
    <a href="https://github.com/leng-yue/py-scrcpy-client/actions/workflows/ci.yml" target="_blank">
        <img src="https://img.shields.io/github/workflow/status/leng-yue/py-scrcpy-client/CI" />
    </a>
    <a href="https://app.codecov.io/gh/leng-yue/py-scrcpy-client" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/leng-yue/py-scrcpy-client" />
    </a>
    <img src="https://img.shields.io/github/license/leng-yue/py-scrcpy-client" />
    <a href="https://github.com/Genymobile/scrcpy/tree/v1.20" target="_blank">
        <img src="https://img.shields.io/badge/scrcpy-v1.20-violet" />
    </a>
</p>

This package allows you to view and control android device in realtime.

![demo gif](https://raw.githubusercontent.com/leng-yue/py-scrcpy-client/main/demo.gif)

Note: This gif is compressed and experience lower quality than actual.

## How to use

To begin with, you need to install this package via pip:

```shell
pip install scrcpy-client[ui]
```

Then, you can start `py-scrcpy` to view the demo:

Note: you can ignore `[ui]` if you don't want to view the demo ui

## Document

Here is the document GitHub page: [Documentation](https://leng-yue.github.io/py-scrcpy-client/)
Also, you can check `scrcpy_ui/main.py` for a full functional demo.

## Contribution & Development

Already implemented all functions in scrcpy server 1.20.
Please check scrcpy server 1.20 source code: [Link](https://github.com/Genymobile/scrcpy/tree/v1.20/server)

## Reference & Appreciation

- Core: [scrcpy](https://github.com/Genymobile/scrcpy)
- Idea: [py-android-viewer](https://github.com/razumeiko/py-android-viewer)
- CI: [index.py](https://github.com/index-py/index.py)
