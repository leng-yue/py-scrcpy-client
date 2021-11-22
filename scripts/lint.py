import subprocess

source_dirs = "scrcpy tests scripts scrcpy_ui"
subprocess.check_call(f"isort {source_dirs}", shell=True)
subprocess.check_call(f"black {source_dirs}", shell=True)
