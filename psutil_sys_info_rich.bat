cd c:\temp

python -m nuitka ^
    --onefile ^
    --windows-icon-from-ico=airplay.ico ^
    --mingw64 ^
    --lto=no ^
    psutil_sys_info_rich.py
pause

