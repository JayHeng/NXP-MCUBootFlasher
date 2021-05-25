#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys
import os

kLanguageIndex_English = 0x0
kLanguageIndex_Chinese = 0x1

kMenuPosition_File     = 0x0
kMenuPosition_Edit     = 0x1
kMenuPosition_View     = 0x2
kMenuPosition_Tools    = 0x3
kMenuPosition_Window   = 0x4
kMenuPosition_Help     = 0x5

kPanelIndex_Download   = 0x0

kMainLanguageContentDict = {
        'menu_file':                          ['File',                                  u"文件"],
        'mItem_exit':                         ['Exit',                                  u"退出"],
        'menu_edit':                          ['Edit',                                  u"编辑"],
        'menu_view':                          ['View',                                  u"查看"],
        'menu_tools':                         ['Tools',                                 u"工具"],
        'subMenu_usbDetection':               ['USB Detection',                         u"USB识别模式"],
        'mItem_usbDetectionDynamic':          ['Dynamic',                               u"动态"],
        'mItem_usbDetectionStatic':           ['Static',                                u"静态"],
        'menu_window':                        ['Window',                                u"界面"],
        'menu_help':                          ['Help',                                  u"帮助"],
        'mItem_homePage':                     ['Home Page',                             u"软件主页"],
        'mItem_aboutAuthor':                  ['About Author',                          u"关于作者"],
        'mItem_revisionHistory':              ['Revision History',                      u"版本历史"],

        'panel_setup':                        ['Setup',                                 u"设置"],
        'sText_mcuDevice':                    ['MCU Device:',                           u"MCU型号:"],
        'sText_mcuBoard':                     ['MCU Boards (Unlimited):',               u"MCU板卡数(不限量):"],
        'sText_connectedBoards':              ['Connected:',                            u"总连接数:"],
        'sText_detectedBoards':               ['Detected:',                             u"已识别数:"],
        'sText_serialPortIndex':              ['MCU Port Idx:',                         u"MCU接口编号:"],
        'radioBtn_uart':                      ['UART',                                  u"串口"],
        'radioBtn_usbhid':                    ['USB-HID',                               u"HID设备"],
        'sText_comPort':                      ['COM Port:',                             u"端口号:"],
        'sText_baudrate':                     ['Baudrate:',                             u"波特率:"],
        'sText_vid':                          ['Vendor ID:',                            u"厂商识别号:"],
        'sText_pid':                          ['Product ID:',                           u"产品识别号:"],

        'panel_download':                     ['Download',                              u"下载"],
        'sText_appPath':                      ['Application Image File (.sb) / Folder:',u"源应用程序文件(.sb)/文件夹:"],
        'button_allInOneAction_black':        ['Start',                                 u"开始"],
        'button_allInOneAction_yellow':       ['Disconnected',                          u"断开"],
        'button_allInOneAction_green':        ['Downloading...',                        u"下载中..."],
        'button_allInOneAction_blue':         ['Success',                               u"成功"],
        'button_allInOneAction_red':          ['Failure',                               u"失败"],
        'sText_successfulBoards':             ['Successful Boards:',                    u"下载成功板卡:"],
        'sText_failedBoards':                 ['Failed Boards:',                        u"下载失败板卡:"],
        'button_slot':                        ['slot',                                  u"插槽"],

}

kRevision_1_0_0_en =  "【v1.0.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT1015, i.MXRT1021, i.MXRT1051/1052, i.MXRT1061/1062, i.MXRT1064 SIP \n" + \
                      "     2. Support both UART and USB-HID serial downloader modes \n" + \
                      "     3. Support for loading .sb image file into boot device \n\n"
kRevision_1_0_0_zh = u"【v1.0.0】 \n" + \
                     u"  特性: \n" + \
                     u"     1. 支持i.MXRT全系列MCU，包含i.MXRT1015、i.MXRT1021、i.MXRT1051/1052、i.MXRT1061/1062、i.MXRT1064 SIP \n" + \
                     u"     2. 支持UART和USB-HID两种串行下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     3. 支持下载.sb格式的image文件进启动设备 \n\n"
kRevision_2_0_0_en =  "【v2.0.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support batch downloading for multiple image files in one folder \n" + \
                      "     2. Support batch downloading for unlimited boards \n" + \
                      "  Improvement: \n" + \
                      "     1. The text of language option in menu bar should be static and easy understanding \n" + \
                      "  Bug: \n" + \
                      "     1. Cannot download large image file (eg 6.8MB) in some case \n\n"
kRevision_2_0_0_zh = u"【v2.0.0】 \n" + \
                     u"  特性: \n" + \
                     u"     1. 支持批量下载多个.sb格式的image文件(来自同一文件夹) \n" + \
                     u"     2. 支持批量下载多个板卡(板卡数量不限) \n" + \
                     u"  改进: \n" + \
                     u"     1. 菜单栏里的语言选项标签应该是静态且易于理解的(中英双语同时显示) \n" + \
                     u"  缺陷: \n" + \
                     u"     1. 当输入的源image文件非常大时(比如6.8MB)，下载可能会超时失败 \n\n"
kRevision_3_0_0_en =  "【v3.0.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT1011, i.MXRT1024 SIP, i.MXRT117x \n" + \
                      "     2. Support i.MXRT5xx/6xx, Kinetis, LPC5500 Series \n" + \
                      "     3. Can download image automatically via USB when new board is connected \n" + \
                      "  Improvement: \n" + \
                      "     1. Can download image into 8 boards via USB at the same time \n" + \
                      "  Bug: \n" + \
                      "     1. Fix USB download issue when static detection mode is set \n\n"
kRevision_3_0_0_zh = u"【v3.0.0】 \n" + \
                     u"  特性: \n" + \
                     u"     1. 支持i.MXRT1011、i.MXRT1024 SIP、i.MXRT117x \n" + \
                     u"     2. 支持i.MXRT5xx/6xx，Kinetis, LPC5500系列 \n" + \
                     u"     3. 动态检测模式下，板卡连接上时自动下载.sb文件(仅适用USB口) \n" + \
                     u"  改进: \n" + \
                     u"     1. 动态检测模式下，支持最多8块板卡通过USB同时下载.sb文件（异步进行） \n" + \
                     u"  缺陷: \n" + \
                     u"     1. 修复静态检测模式下板卡无法通过USB口正常下载的问题 \n\n"
kRevision_3_1_0_en =  "【v3.1.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT116x \n" + \
                      "  Improvement: \n" + \
                      "     1. Can show pass/total info for each slot \n" + \
                      "     2. Can generate log file to record each slot programming status \n\n"
kRevision_3_1_0_zh = u"【v3.1.0】 \n" + \
                     u"  特性: \n" + \
                     u"     1. 支持i.MXRT116x \n" + \
                     u"  改进: \n" + \
                     u"     1. 可以在插槽控件上显示下载统计信息 \n" + \
                     u"     2. 可以将插槽下载失败的情况记录下来 \n\n"

kMsgLanguageContentDict = {
        'homePage_title':                     ['Home Page',                             u"项目主页"],
        'homePage_info':                      ['https://github.com/JayHeng/NXP-MCUBootFlasher.git \n',                             u"https://github.com/JayHeng/NXP-MCUBootFlasher.git \n"],
        'aboutAuthor_title':                  ['About Author',                          u"关于作者"],
        'aboutAuthor_author':                 [u"Author:  痞子衡 \n",                   u"作者：痞子衡 \n"],
        'aboutAuthor_email1':                 ['Email:     jie.heng@nxp.com \n',        u"邮箱：jie.heng@nxp.com \n"],
        'aboutAuthor_email2':                 ['Email:     hengjie1989@foxmail.com \n', u"邮箱：hengjie1989@foxmail.com \n"],
        'aboutAuthor_blog':                   [u"Blog:      痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n",                   u"博客：痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"],
        'revisionHistory_title':              ['Revision History',                      u"版本历史"],
        'revisionHistory_v1_0_0':             [kRevision_1_0_0_en,                      kRevision_1_0_0_zh],
        'revisionHistory_v2_0_0':             [kRevision_2_0_0_en,                      kRevision_2_0_0_zh],
        'revisionHistory_v3_0_0':             [kRevision_3_0_0_en,                      kRevision_3_0_0_zh],
        'revisionHistory_v3_1_0':             [kRevision_3_1_0_en,                      kRevision_3_1_0_zh],

        'connectError_failToJumpToFl':        ['Failed to jump to Flashloader, Reset board and try again!',
                                              u"MCU已进入ROM SDP模式，但未能跳转Flashloader，请复位板子再试！"],
        'connectError_notValidSignedFl':      ['Signed flashloader(ivt_flashloader_signed.bin) is not found!',
                                              u"没有找到签名的Flashloader文件(ivt_flashloader_signed.bin)！"],
        'connectError_doubleCheckBmod':       ['Put MCU in SDP mode (BMOD[1:0] = 2\'b01), Reset board and try again!',
                                              u"将BMOD[1:0]引脚状态设置为2\'b01，然后复位板子再试！"],
        'connectError_failToPingFl':          ['Failed to ping Flashloader, Reset board and try again!',
                                              u"MCU未能与Flashloader建立连接，请复位板子再试！"],
        'connectError_checkUsbCable':         ['Disconnected, Check USB Cable then reset board and try again!',
                                              u"未连接，检查USB线后复位板子再试！"],
        'connectInfo_readyForDownload':       ['Connected, Ready for downloading!',
                                              u"已连接，可以进行下载操作！"],

        'downloadError_notValidImage':        ['Please select one application image file (.sb ) or folder containing .sb file!',
                                              u"请先选择一个.sb文件或文件夹！"],
        'downloadError_clearImageFileFirst':  ['Please clear application image file path first then set folder path!',
                                              u"请先清除.sb文件路径，然后再设.sb文件夹路径！"],
        'downloadError_notValidImageFolder':  ['Please select one folder containing application image file (.sb )!',
                                              u"请选择一个包含.sb文件的文件夹！"],
        'downloadError_failToDownload':       ['Failed to download application image file (.sb )!',
                                              u"未能成功下载.sb文件！"],
        'downloadInfo_success':               ['Application image file (.sb ) has been downloaded successfully!',
                                              u".sb文件已被成功下载！"],

        'portInfo_alreadySet':                ['Already Set',
                                              u"已设置"],
        'portInfo_notSet':                    ['Not Set',
                                              u"未设置"],

        'connectError_doubleCheckIsp':        ['Put MCU in ISP modes (ISP[2:0] pins = 3\'bx10 (USB/UART)), Reset board and try again!',
                                              u"将ISP[2:0]引脚设为3\'bx10 (USB/UART)，然后复位板子再试！"],
        'connectError_doubleCheckFopt':       ['Put MCU in ROM boot mode (FOPT = 0x3D, assert BOOTCFG0(NMI)), Reset board and try again!',
                                              u"将FOPT(FCF区域0x40d)设为0x3D以及按住BOOTCFG0，然后复位板子再试！"],
        'connectError_doubleCheckIspBoot':    ['Put MCU in ISP boot mode (ISP0 pin = LOW), Reset board and try again!',
                                              u"将ISP0引脚设为低，然后复位板子再试！"],

        'usbDymaticModeInfo':                 ['Slot Green - \'Downloading...\';  Slot Blue - \'Success\';  Slot Red - \'Failure\';',
                                              u"插槽显示绿色 - \'下载中...\';  插槽显示蓝色 - 成功;  插槽显示红色 - 失败；"],
}