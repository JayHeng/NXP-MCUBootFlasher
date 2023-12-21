--
　　RT产品落满地，客户工厂生产急;  
　　痞子衡出新神器，从此量产不费力！  

　　恩智浦半导体2017年10月正式发布了业内首款跨界处理器—i.MX RT系列，超强的性能、超高的性价比使得i.MX RT系列火遍大江南北，一度成为基于MCU的产品主控首选，尤其是那些对于性能有较高要求的产品，客户工程师更是苦盼i.MX RT久矣。经过一年多的评估与研发期，目前基于i.MX RT的产品已全面开花，客户工厂正在火热生产中，然而不少客户在实际量产中遇到了恩智浦官方i.MX RT量产工具MfgTool2使用上的一些小问题，痞子衡经过与客户沟通与工厂实地考察，了解了客户在MfgTool2实际量产使用中的限制，决定为客户排除这些限制，提升客户满意度，于是闭关一周潜心码代码，如今已顺利出关，并为大家带来了一款全新的量产工具RT-Flash。  

### 一、MfgTool2工具现状
　　恩智浦官方i.MX RT量产工具名为MfgTool2，其包含在Flashloader包里。以i.MXRT105x为例，可以在恩智浦官网i.MXRT105x产品主页的TOOLS & SOFTWARE下面找到该Flashloader包，当前Flashloader包版本为v1.1：  

![RT-Flash_RT1050Flashloader_webpage](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/rtFlash_Intro_RT1050Flashloader_webpage.PNG)

　　下载好Flashloader包后，打开\Flashloader_RT1050_1.1\Tools\mfgtools-rel\MfgTool2.exe便可看到该量产工具界面，界面非常简单明了，毕竟是量产工具嘛，要适合产线工人操作，理应越简单越好。  

![RT-Flash_MfgTool2_GUI](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/rtFlash_Intro_MfgTool2_GUI.PNG)

　　不过MfgTool2工具经过客户的实际量产使用反馈，隐含如下四个主要限制，且听痞子衡一一解析：  

#### 限制一：sb文件仅能在xml文件中指定
　　如果你用过MfgTool2工具，你也肯定知道有一种特殊的文件格式，即.sb文件格式，这个文件格式是专为i.MX RT产品量产而定制的专用格式，.sb文件中除了包含基本的Application数据外，还包含了Boot Device配置信息，以及Flash操作命令，此外还可能有efuse烧写命令，可以说.sb文件包含了i.MX RT产品量产所需要的所有操作。  

　　MfgTool2工具就是用来专门解析和下载.sb格式文件的，客户只需要提供.sb文件，其他量产工作全部交给MfgTool2就行了。但是要烧写的.sb文件是如何在MfgTool2工具里指定的呢？MfgTool2工具主界面并未看到有选择.sb文件的控件，好吧，该是痞子衡解密的时候了，其实秘密藏在\Flashloader_RT1050_1.1\Tools\mfgtools-rel\Profiles\MXRT105X\OS Firmware\ucl2.xml文件里，使用任何一个文本编辑器打开这个xml文件，找到"MXRT105x-DevBoot"（默认模式，由\Flashloader_RT1050_1.1\Tools\mfgtools-rel\cfg.ini文件指定）对应的LIST，你会发现.sb文件路径\Profiles\MXRT105X\OS Firmware\boot_image.sb。  

![RT-Flash_sb_file_path](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/rtFlash_Intro_sb_file_path_in_xml.png)

　　这种.sb文件指定方法在实际工厂量产中会有一些不便，研发工程师生成好.sb文件，往往在命名的时候会加入版本信息予以区别，比如boot_image_v1.0.sb。这个.sb文件发给工厂量产时，产线工人拿到这个.sb文件后，需要将其放在确定路径下（比如\Profiles\MXRT105X\OS Firmware\），并且修改xml文件里的.sb文件路径内容，保证路径名及.sb文件名与量产现场电脑里存储.sb文件情况相一致。这无疑增加了工人操作复杂度。  

#### 限制二：仅能使用USB接口下载，无法使用UART
　　MfgTool2工具仅支持USB接口去下载.sb文件，因此客户工程师在设计产品时为了量产需要必须要引出USB接口。如果客户产品设计里本来就有USB接口设计，那没有问题；但如果客户产品设计里本不需要USB接口，此时仅仅是为了量产而引出USB接口，这对于客户产品设计来说有点浪费成本。  

　　如果量产工具能够支持UART接口去下载.sb文件，那么客户仅需引出两根UART引脚即可，这种情况客户工程师一般是能够接受的。  

#### 限制三：有时候无法识别USB连接，必须加Hub方可识别
　　MfgTool2工具支持USB接口去下载.sb文件，当客户板卡连上PC时，会有新的HID-compliant设备枚举出来（在设备管理器里查看）。  

![RT-Flash_usb_hid_device](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/rtFlash_Intro_usb_hid_in_device_manager.png)

　　MfgTool2工具能够自动识别该USB设备的连接，从工具界面上可看到左上角状态由"Unassigned"变为了连接上的USB设备的位置信息（Hub 6 -- Port 3），此时表明MfgTool2已经找到板卡，可以开始下载操作了。  

![RT-Flash_usb_hid_detected](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/rtFlash_Intro_usb_hid_detected.PNG)

　　但有的时候，在某些客户工厂的电脑上，当连接上板卡后，虽然可以在设备管理器上看到HID-compliant设备已正常枚举，但是MfgTool2工具没能正确识别到，工具右上角状态仍为"Unassigned"，这时候客户可能需要加一级Hub或者更换一台电脑重新再试。这在一定程度上增加了量产工作量，影响量产效率。  

#### 限制四：批量生产最多仅能支持4块板卡
　　MfgTool2工具支持多板卡批量下载。在\Flashloader_RT1050_1.1\Tools\mfgtools-rel\UICfg.ini文件里将PortMgrDlg的值由1改为4，重新打开MfgTool2工具，便会看到如下全新界面：  

![RT-Flash_MfgTool2_GUI4](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/rtFlash_Intro_MfgTool2_GUI4.PNG)

　　如果此时电脑上同时连接4块板卡，只需一次点击，MfgTool2便会将.sb文件内容按序下载进4块板卡，这就是所谓的批量下载。既然能批量下载，那当然支持的板卡同时连接数越多越好，但是MfgTool2最大只能支持4块板卡，不免让客户觉得意犹未尽。  

### 二、全新量产神器RT-Flash
　　上一节讲完了MfgTool2量产使用中的一些限制，现在该是新量产工具RT-Flash登场的时候了，让我们先来看一些RT-Flash的主界面。与MfgTool2一样，RT-Flash界面也是足够简单，并没有太多花哨的东西，便于产线工人操作，更重要的是MfgTool2使用上的四大限制在RT-Flash上统统不存在。有木有很惊喜？再告诉你一个好消息，你可以联合NXP-MCUBootUtility工具（v1.3.0及以上）与RT-Flash工具一起使用，前者可生成.sb文件，后者专门解析下载.sb文件，可谓珠联璧合。  

![RT-Flash_mainWin](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/RT-Flash_v2.0.0.PNG)

　　RT-Flash是一个专为基于NXP i.MX RT系列芯片的产品量产而设计的工具，其功能与官方MfgTool2工具类似，但是解决了MfgTool2工具在实际量产使用中的一些限制。借助于RT-Flash，你可以轻松实现批量生产。RT-Flash主要功能如下：  

> * 支持i.MXRT全系列MCU，包含i.MXRT1015、i.MXRT1021、i.MXRT1051/1052、i.MXRT1061/1062、i.MXRT1064 SIP  
> * 支持UART和USB-HID两种串行下载方式（COM端口/USB设备自动识别）  
> * 支持下载.sb格式的image文件进启动设备  
> * 支持批量下载多个.sb格式的image文件(同一文件夹下)  
> * 支持批量下载多个板卡(板卡数量不限)

　　这么好用的工具去哪里下载？其实RT-Flash是一个基于Python的开源项目，其项目地址为 https://github.com/JayHeng/RT-Flash， 核心代码只有3000多行，虽然当前版本（v2.0.0）功能已经非常完备，你还是可以在此基础上再添加自己想要的功能。如此神器，还不快快去下载试用？  
