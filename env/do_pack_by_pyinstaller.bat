pyinstaller.exe pyinstaller_pack_f.spec
copy .\dist\NXP-MCUBootFlasher.exe ..\bin
rd /q /s .\build
rd /q /s .\dist