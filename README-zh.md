# NXP MCU Boot Flasher

[![GitHub release](https://img.shields.io/github/release/JayHeng/NXP-MCUBootFlasher.svg)](https://github.com/JayHeng/NXP-MCUBootFlasher/releases/latest) [![GitHub commits](https://img.shields.io/github/commits-since/JayHeng/NXP-MCUBootFlasher/v2.0.0.svg)](https://github.com/JayHeng/NXP-MCUBootFlasher/compare/v2.0.0...master) ![GitHub All Releases](https://img.shields.io/github/downloads/JayHeng/NXP-MCUBootFlasher/total.svg) [![GitHub license](https://img.shields.io/github/license/JayHeng/NXP-MCUBootFlasher.svg)](https://github.com/JayHeng/NXP-MCUBootFlasher/blob/master/LICENSE)

[English](./README.md) | 中文

```text
对于MCUBootUtility，MCUBootFlasher（NXP-MCUBootFlasher）工具，有任何使用上的问题，可以在《痞子衡嵌入式》博客下留言，也可以扫码加入QQ交流群。  
```

<img src="http://henjay724.com/image/cnblogs/MCUBootUtility_qq.png" style="zoom:100%" />

### 1 软件概览
#### 1.1 介绍
　　NXP-MCUBootFlasher是一个专为基于NXP i.MX RT系列芯片的产品量产而设计的工具，其功能与官方MfgTool2工具类似，但是解决了MfgTool2工具在实际量产使用中的一些痛点：  

> * 使用MfgTool2仅能在xml中指定.sb文件，无法直接在GUI里选择.sb文件；  
> * 使用MfgTool2仅能选择USB端口，无法使用UART端口；  
> * 使用MfgTool2的USB端口下载时，有时无法识别某些端口连接，必须要加Hub方可识别;  
> * 使用MfgTool2批量下载时，最多只能支持4块板卡;  

　　借助于NXP-MCUBootFlasher，你可以轻松实现批量生产。NXP-MCUBootFlasher主要功能如下：  

> * 支持i.MXRT全系列MCU，包含i.MXRT1015、i.MXRT1021、i.MXRT1051/1052、i.MXRT1061/1062、i.MXRT1064 SIP  
> * 支持UART和USB-HID两种串行下载方式（COM端口/USB设备自动识别）  
> * 支持下载.sb格式的image文件进启动设备  
> * 支持批量下载多个.sb格式的image文件(同一文件夹下)  
> * 支持批量下载多个板卡(板卡数量不限)

#### 1.2 下载
　　NXP-MCUBootFlasher完全基于Python语言开发，并且源代码全部开源，其具体开发环境为Python 2.7.15 (32bit)、wxPython 4.0.3、pySerial 3.4、pywinusb 0.4.2、PyInstaller 3.3.1（或更高）。  

> * 源代码: https://github.com/JayHeng/NXP-MCUBootFlasher  
> * 用户手册：https://www.cnblogs.com/henjay724/p/10776084.html
> * 问题反馈：https://www.cnblogs.com/henjay724/p/10776095.html

　　NXP-MCUBootFlasher在发布时借助PyInstaller将所有的Python依赖全部打包进一个可执行文件（\NXP-MCUBootFlasher\bin\NXP-MCUBootFlasher.exe），因此如果不是对NXP-MCUBootFlasher的二次开发，你不需要安装任何Python软件及相关库。  

> Note1: 源代码包里的NXP-MCUBootFlasher.exe是在Windows 10 x64环境下打包的，也仅在该环境下测试过，如果因系统原因无法直接使用，你需要先安装 [Python2.7.15 x86版本](https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi) （安装完成后确认\Python27\\, \Python27\Scripts\\目录被添加到系统环境变量Path里），然后在\NXP-MCUBootFlasher\env\目录下点击do_setup_by_pip.bat安装开发NXP-MCUBootFlasher所依赖的Python库，最后点击do_pack_by_pyinstaller.bat重新生成NXP-MCUBootFlasher.exe可执行文件。  

> Note2: 必须使用Python2 x86版本去打包NXP-MCUBootFlasher，因为NXP-MCUBootFlasher使用了pywinusb库，该库在Python2 x64版本下无法用PyInstaller打包，pywinusb作者没有计划修复该问题。  

#### 1.3 安装
　　NXP-MCUBootFlasher是一个是纯绿色免安装的工具，下载了源代码包之后，直接双击\NXP-MCUBootFlasher\bin\NXP-MCUBootFlasher.exe即可使用。使用NXP-MCUBootFlasher没有任何软件依赖，不需要额外安装任何软件。  
　　在NXP-MCUBootFlasher.exe图形界面显示之前，会首先弹出一个控制台窗口，该控制台会伴随着NXP-MCUBootFlasher.exe图形界面一起工作，很多图形界面的操作都会在控制台窗口看到对应的底层命令执行，保留控制台主要是为了便于定位NXP-MCUBootFlasher.exe的问题，目前NXP-MCUBootFlasher尚处于早期阶段，等后期软件成熟会考虑移除控制台。  

#### 1.4 目录

　　NXP-MCUBootFlasher软件目录组织如下：  
```text
\NXP-MCUBootFlasher
                \apps                 --放置NXP官方评估板示例.sb格式image文件
                \bin                  --放置NXP-MCUBootFlasher可执行文件
                \env                  --放置用于安装NXP-MCUBootFlasher开发环境以及打包脚本
                \gui                  --放置开发NXP-MCUBootFlasher UI构建工程文件
                \img                  --放置NXP-MCUBootFlasher使用过程中需加载的图片
                \src                  --放置开发NXP-MCUBootFlasher的所有Python源代码文件
                \tools                --放置NXP-MCUBootFlasher使用过程中需调用的外部程序
                      \blhost             --与Flashloader通信的上位机命令行工具
                      \sdphost            --与ROM通信的上位机命令行工具
```

#### 1.5 界面
　　下图为NXP-MCUBootFlasher工具的主界面，界面主要由四部分组成，各部分功能如下：  

![NXP-MCUBootFlasher_mainWin](http://henjay724.com/image/cnblogs/NXP-MCUBootFlasher_v2.0.0.PNG)

> * 【Menu Bar】：功能菜单栏，提供软件通用设置。  
> * 【Setup Window】：设置栏，提供MCU Device选项、串行接口选项。  
> * 【Download Window】：下载主界面，提供对目标设备做一键下载操作。  
> * 【Status Bar】：状态栏，显示软件运行状态信息。  

### 2 准备工作
　　在使用NXP-MCUBootFlasher工具前主要有两个准备工作：一、准备好i.MXRT硬件板以及串行下载连接线（USB/UART）；二、准备好用于下载进Flash的.sb格式源文件。  
　　关于串行下载线连接，需要查看i.MXRT参考手册System Boot章节，确保连接的UART/USB引脚是BootROM指定的。  
　　关于.sb格式源文件准备，可借助NXP-MCUBootUtility工具（v1.2.0版本及以上），NXP-MCUBootUtility能够识别五种常见格式(elf/axf/srec/hex/bin)的源image，并且能够将源image文件转换成.sb格式文件。  
　　如果只是为了快速验证NXP-MCUBootFlasher工具，在NXP-MCUBootFlasher\apps文件夹下默认存放了全系列恩智浦官方i.MXRT评估板的led_blinky应用的.sb格式文件。  

### 3 软件使用
#### 3.1 设置目标芯片
　　在使用NXP-MCUBootFlasher时首先需要配置目标设备，目标设备即MCU Device。以NXP官方开发板EVK-MIMXRT1060为例，该开发板主芯片为i.MXRT1062DVL6A，所以【RT Device】应设为i.MXRT106x。  

![NXP-MCUBootFlasher_setMcuDevice](http://henjay724.com/image/cnblogs/rtFlash_v1_1_0_setMcuDevice_rt1060.PNG)

#### 3.2 设置下载端口
　　设置好目标设备之后，下一步便是连接目标设备，以USB-HID接口连接为例，给EVK-MIMXRT1060板子供电，并用USB Cable将PC与J9口连接起来，如果一切正常，应该可以在设备管理器找到vid,pid为0x1fc9,0x0135的HID-compliant vendor-defined device设备被枚举。如果没有发现该HID设备，请仔细检查板子SW7拨码开关是否将Boot Mode设为2'b01即Serial Downloader模式。  

![NXP-MCUBootUtility_usbhidDetected_e](http://henjay724.com/image/cnblogs/nxpSecBoot_usbhidDetected_e.png)

　　确认HID设备存在之后，选中USB-HID即可。  

![NXP-MCUBootFlasher_setPort_usb_e](http://henjay724.com/image/cnblogs/rtFlash_v1_1_0_setPort_usb_e.png)

#### 3.3 点击一键下载
　　选中要下载的.sb文件，直接点击【Start】按钮便可将.sb文件下载进启动设备。如果成功下载，【Successful Boards】里数值会变成1，此外状态栏里会显示"Application image file (.sb) has been downloaded successfully!"。  

![NXP-MCUBootFlasher_SingleBoardSingleSb_e](http://henjay724.com/image/cnblogs/rtFlash_v1_1_0_SingleBoardSingleSb_downloadSuccess_e.png)

#### 3.4 批量下载
##### 3.4.1 批量多文件
　　如果你想一次性下载多个.sb文件，你需要将这些文件放置于同一个文件夹，然后在工具里第二个【Browse】下选中这个文件夹（注意必须保证第一个【Browse】按钮里的路径是空），然后直接点击【Start】按钮便可。  

![NXP-MCUBootFlasher_SingleBoardMultipleSb_e](http://henjay724.com/image/cnblogs/rtFlash_v1_1_0_SingleBoardMultipleSb_downloadSuccess_e.png)

##### 3.4.2 批量多板卡
　　如果你想一次性下载程序进多个板卡，你需要在板卡设置栏【Connected】填入实际连接板卡数（填入数值后必须按键盘上的Enter键来确定），以USB接口为例，此时你会看到【Detected】里会显示实际识别板卡数，最终下载以实际识别板卡数为准。然后直接点击【Start】按钮便可。  

![NXP-MCUBootFlasher_MultipleBoardSingleSb_e](http://henjay724.com/image/cnblogs/rtFlash_v1_1_0_MultipleBoardMultipleSb_downloadSuccess_e.png)

　　如果选择的是UART接口，你必须在【RT Port Index】里逐一选中每个Port进行具体设置，并保证右侧状态均为"Already Set"。  

![NXP-MCUBootFlasher_setPort_multipleUart_e](http://henjay724.com/image/cnblogs/rtFlash_v1_1_0_setPort_multipleUart_e.png)

#### 3.5 在HAB Closed情况下
　　当芯片HAB状态处于Closed的情况下，此时需要将你生成的含签名的flashloader文件放置于NXP-MCUBootFlasher指定目录下（此处以RT106x为例），并且文件必须命名为ivt_flashloader_signed.bin。  

![NXP-MCUBootFlasher_signedFlashloader_e](http://henjay724.com/image/cnblogs/rtFlash_v1_0_0_signedFlashloader.PNG)

　　除此以外，还需确保bltargetconfig.py文件里的两个变量与你的含签名flashloader文件相匹配。  

![NXP-MCUBootFlasher_signedFlashloader_address_e](http://henjay724.com/image/cnblogs/rtFlash_v1_0_0_signedFlashloader_address_e.png)
