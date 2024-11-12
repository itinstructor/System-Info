cd c:\temp

python -m nuitka ^
    --mingw64 ^
    --lto=no ^
    --onefile ^
    --enable-plugin=tk-inter ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=airplay.ico ^
    system_info_gui_theme.py
pause