# RT Flash

[![GitHub release](https://img.shields.io/github/release/JayHeng/RT-Flash.svg)](https://github.com/JayHeng/RT-Flash/releases/latest) [![GitHub commits](https://img.shields.io/github/commits-since/JayHeng/RT-Flash/v1.0.0.svg)](https://github.com/JayHeng/RT-Flash/compare/v1.0.0...master) [![GitHub license](https://img.shields.io/github/license/JayHeng/RT-Flash.svg)](https://github.com/JayHeng/RT-Flash/blob/master/LICENSE)

English | [中文](./README-zh.md)

### 1 Overview
#### 1.1 Introduction
　　RT-Flash is a GUI tool specially designed for i.MX RT production. Its feature is similar to MfgTool2, but it solves below limitaions of MfgTool2:  

> * The .sb file can only be specified in xml file;  
> * USB port is the only choice to download .sb file;  
> * Sometimes USB Hub connection is not appliable;  

　　With RT-Flash, you can easily get started with NXP MCU secure boot. The main features of RT-Flash include：  

> * Support i.MXRT1015, i.MXRT1021, i.MXRT1051/1052, i.MXRT1061/1062, i.MXRT1064 SIP  
> * Support both UART and USB-HID serial downloader modes  
> * Support for loading .sb image file into boot device  

#### 1.2 Download
　　RT-Flash is developed in Python, and it is open source. The development environment is Python 2.7.15 (32bit), wxPython 4.0.3, pySerial 3.4, pywinusb 0.4.2, PyInstaller 3.3.1 (or higher).  

> * Source code: https://github.com/JayHeng/RT-Flash  

　　RT-Flash is packaged by PyInstaller, all Python dependencies have been packaged into an executable file (\RT-Flash\bin\RT-Flash.exe), so if you do not want to develop RT-Flash for new feature, there is no need to install any Python software or related libraries.  

> Note1: The RT-Flash.exe in the source code package is packaged in the Windows 10 x64 environment and has only been tested in this environment. If it cannot be used directly for system environment reasons, you need to install [Python2.7.15 x86 version ](https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi)(Confirm that the directory "\Python27\" and "\Python27\Scripts\" are in the system environment variable path after the installation is completed), then click on "do_setup_by_pip.bat" in the "\RT-Flash\env\" directory to install the Python library on which RT-Flash depends. Finally, click "do_pack_by_pyinstaller.bat" to regenerate the RT-Flash.exe.  

> Note2: You must use Python2 x86 version, because RT-Flash uses the pywinusb library, which cannot be packaged by PyInstaller in Python2 x64 version. The pywinusb author has no plan to fix the problem.  

#### 1.3 Installation
　　RT-Flash is a pure green free installation tool. After downloading the source code package, double-click "\RT-Flash\bin\RT-Flash.exe" to use it. No additional software is required.  
　　Before the RT-Flash.exe graphical interface is displayed, a console window will pop up first. The console will work along with the RT-Flash.exe graphical interface. The console is mainly for the purpose of showing error information of RT-Flash.exe. At present, RT-Flash is still in development stage, and the console will be removed when the RT-Flash is fully validated.

#### 1.4 Contents
　　The RT-Flash software directory is organized as follows:  
```text
\RT-Flash
                \apps                 --Place example source image files
                \bin                  --Place RT-Flash.exe file
                \env                  --Place scripts to install the RT-Flash development environment and to do package
                \gui                  --Place RT-Flash development UI build project file
                \img                  --Place the image to be loaded during the use of RT-Flash
                \src                  --Place all Python source code files for developing RT-Flash
                \tools                --Place all external programs to be called during the use of RT-Flash
                      \blhost             -- Host command line tool to communicate with Flashloader
                      \sdphost            -- Host command line tool to communicate with ROM
```
#### 1.5 Interface
　　The following figure shows the main interface of the RT-Flash tool. The interface consists of five parts. The functions of each part are as follows:  

![RT-Flash_mainWin_e](http://henjay724.com/image/cnblogs/rtFlash_v1_0_0_mainWin_e.png)

> * [Menu Bar]: Functional menu bar, providing general software settings.  
> * [Target Setup]: Target device setting bar, providing MCU Device options.  
> * [Port Setup]: In the serial interface setting field, select the interface for connecting to the MCU Device.  
> * [Boot Action]: Boot main interface, providing all-in-one operation.  
> * [Status Bar]: Status bar, showing runtime infomation  

### 2 Preparation
　　There are two main preparations before using the RT-Flash tool: 1. Prepare the i.MXRT hardware board and the serial download cable (USB/UART). 2. Prepare the .sb image file for downloading into Flash.  
　　For serial download line connections, you need to check the System Boot chapter of the i.MXRT Reference Manual to ensure that the connected UART/USB pins are specified by the BootROM.  
　　Regarding the .sb image file preparation, the NXP-MCUBootUtility tool (v1.2.0 or higher) can recognize the images of the five common formats (elf/axf/srec/hex/bin) and convert the image into .sb file.  
　　If you just want to quickly verify the RT-Flash tool, all the led_blinky application .sb image files of NXP's official i.MXRT evaluation boards are stored by default in the RT-Flash\apps folder.  

### 3 Basic Usage
#### 3.1 Setting target chip
　　When using RT-Flash, you need to configure the target device. The target device includes MCU Device. Taking the NXP official development board EVK-MIMXRT1060 as an example, the main chip of the development board is i.MXRT1062DVL6A, so [RT Device] should be set to i.MXRT106x.  

![RT-Flash_setMcuDevice_e](http://henjay724.com/image/cnblogs/rtFlash_v1_0_0_setMcuDevice_e.png)

#### 3.2 Setting download port
　　After setting up the target device, the next step is to connect the target device. Taking the USB-HID interface as an example, supply power to the EVK-MIMXRT1060 board, and connect the PC to the J9 port with USB Cable. If everything is going well, you can find new HID device (vid=0x1fc9, pid=0x0135) named HID-compliant vendor-defined device is enumerated. If the HID device is not found, please check the board SW7 DIP switch to set Boot Mode to 2'b01(Serial Downloader mode).  

![NXP-MCUBootUtility_usbhidDetected_e](http://henjay724.com/image/cnblogs/nxpSecBoot_usbhidDetected_e.png)

　　After confirming the existence of the HID device, select USB-HID in [Port Setup].  

![RT-Flash_setPort_e](http://henjay724.com/image/cnblogs/rtFlash_v1_0_0_setPort_e.png)

#### 3.3 Clicking All-In-One Action
　　At first, you should select your .sb file, then just click [All-In-One Action] button, if the .sb file has been downloaded successfully, the background color of [All-In-One Action] button will turn blue.  

![RT-Flash_downloadSb_e](http://henjay724.com/image/cnblogs/rtFlash_v1_0_0_downloadSb_e.png)

