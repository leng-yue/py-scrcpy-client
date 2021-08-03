# Python Scrcpy Client

![pypi package](https://img.shields.io/pypi/v/scrcpy-client)
![build](https://img.shields.io/github/workflow/status/leng-yue/py-scrcpy-client/CI)
![build](https://img.shields.io/github/license/leng-yue/py-scrcpy-client)

This package allows you to view and control android device in realtime. 

## How to use
To begin with, you need to install this package via pip:
```shell
pip install scrcpy-client
```
Then, you can start `demo.py`:
```shell
python demo.py
```
Note: You need to install adb by yourself.

## Contribution & Development
Please check scrcpy server 1.12.1 source code: [Link](https://github.com/Genymobile/scrcpy/blob/v1.12.1/server/src/main/java/com/genymobile/scrcpy/ControlMessageReader.java)

## TODO:
- [x] Support all KeyCodes
- [ ] Update scrcpy to 1.19
- [ ] Add control unit test

## Reference
- [py-android-viewer](https://github.com/razumeiko/py-android-viewer)
- [scrcpy](https://github.com/Genymobile/scrcpy)
