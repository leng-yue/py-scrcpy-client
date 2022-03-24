# Minimal makefile for Sphinx documentation
.PHONY: help

# Put it first so that "make" without argument is like "make help".
help: # 获取命令行示例
	@grep ":" Makefile | grep -v "Makefile"

run: # 运行
	pip install .
	py-muti-scrcpy
ui: # 编译.ui 到 .py
	cd scrcpy_ui && pyside6-uic single.ui -o ui_single.py
	cd scrcpy_ui && pyside6-uic mainwindow.ui -o ui_main.py
	cd scrcpy_ui && pyside6-uic screen.ui -o ui_screen.py
