cd c:\temp

python -m nuitka ^
    --onefile ^
    --enable-plugin=tk-inter ^
    --mingw64 ^
    --lto=no ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=airplay.ico ^
    system_info_gui.py
pause