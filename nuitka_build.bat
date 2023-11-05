python -m nuitka ^
    --standalone ^
    --lto=no ^
    --output-dir=build ^
    --company-name="ACGN-Alliance" ^
    --product-name="BlueArchive-Starter-Develop-Tools" ^
    --windows-icon-from-ico=bas.ico ^
    --disable-plugin=multiprocessing ^
    --file-version="0.0.1" ^
    --product-version="0.0.1" ^
    --windows-file-description="Develop Tools for BAS" ^
    --copyright="Copyright @ACGN-Alliance. All right reserved." ^
    --remove-output ^
    --msvc=latest ^
    --clang ^
    --windows-disable-console ^
    --jobs=4 ^
    entry.py