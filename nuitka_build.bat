python -m nuitka ^
    --standalone ^
    --lto=no ^
    --output-dir=build ^
    --company-name="ACGN-Alliance" ^
    --product-name="BlueArchive-Starter-Develop-Tools" ^
    --windows-icon-from-ico=bas.ico ^
    --file-version="0.0.1" ^
    --product-version="0.0.1" ^
    --windows-file-description="Develop Tools for BAS" ^
    --copyright="Copyright @ACGN-Alliance. All right reserved." ^
    --remove-output ^
    --windows-disable-console ^
    --msvc=latest ^
    --clang ^
    --jobs=4 ^
    --enable-plugin=pyside6 ^
    --include-data-file=scrcpy/scrcpy-server.jar=scrcpy/scrcpy-server.jar ^
    entry.py