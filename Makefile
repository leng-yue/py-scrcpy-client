# Minimal makefile for Sphinx documentation
.PHONY: help

# Put it first so that "make" without argument is like "make help".
help: # 获取命令行示例
	@grep ":" Makefile | grep -v "Makefile"

code_check:
	isort --check --diff scrcpy tests scripts scrcpy_ui workers
	black --check --diff scrcpy tests scripts scrcpy_ui workers
	flake8 --ignore W503,E203,E501,E731,F403,F401 scrcpy tests scripts scrcpy_ui --exclude scrcpy_ui/ui_main.py,scrcpy_ui/ui_single.py,scrcpy_ui/ui_screen.py,scrcpy_ui/ui_config_edit.py

format:
	isort scrcpy tests scripts scrcpy_ui workers
	black scrcpy tests scripts scrcpy_ui workers
	flake8 --ignore W503,E203,E501,E731,F403,F401 scrcpy tests scripts scrcpy_ui --exclude scrcpy_ui/ui_main.py,scrcpy_ui/ui_single.py,scrcpy_ui/ui_screen.py,scrcpy_ui/ui_config_edit.py

run: # 运行
	pip install .
	py-muti-scrcpy

ui: # 编译.ui 到 .py
	cd scrcpy_ui && pyside6-uic single.ui -o ui_single.py
	cd scrcpy_ui && pyside6-uic mainwindow.ui -o ui_main.py
	cd scrcpy_ui && pyside6-uic screen.ui -o ui_screen.py
	cd scrcpy_ui && pyside6-uic config_edit.ui -o ui_config_edit.py
