pyinstaller.exe pyinstaller_pack_f.spec
copy .\dist\RT-Flash.exe ..\bin
rd /q /s .\build
rd /q /s .\dist