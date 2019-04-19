#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
        'subMenu_language':                   ['Language',                              u"语言"],
        'mItem_english':                      ['English',                               u"英文"],
        'mItem_chinese':                      ['Chinese',                               u"简体中文"],
        'menu_tools':                         ['Tools',                                 u"工具"],
        'subMenu_usbDetection':               ['USB Detection',                         u"USB识别模式"],
        'mItem_usbDetectionAuto':             ['Auto',                                  u"动态"],
        'mItem_usbDetectionStatic':           ['Static',                                u"静态"],
        'menu_window':                        ['Window',                                u"界面"],
        'menu_help':                          ['Help',                                  u"帮助"],
        'mItem_homePage':                     ['Home Page',                             u"软件主页"],
        'mItem_aboutAuthor':                  ['About Author',                          u"关于作者"],
        'mItem_revisionHistory':              ['Revision History',                      u"版本历史"],

        'panel_setup':                        ['Setup',                                 u"设置"],
        'sText_mcuDevice':                    ['RT Device:',                            u"RT型号："],
        'sText_serialPort':                   ['Serial Port:',                          u"串行接口："],
        'radioBtn_uart':                      ['UART',                                  u"串口"],
        'radioBtn_usbhid':                    ['USB-HID',                               u"HID设备"],
        'sText_comPort':                      ['COM Port:',                             u"端口号："],
        'sText_baudrate':                     ['Baudrate:',                             u"波特率："],
        'sText_vid':                          ['Vendor ID:',                            u"厂商识别号："],
        'sText_pid':                          ['Product ID:',                           u"产品识别号："],

        'panel_download':                     ['Download',                              u"下载"],
        'sText_appPath':                      ['Application Image File (.sb):',         u"源应用程序文件(.sb)："],
        'button_allInOneAction_black':        ['Start',                                 u"开始"],
        'button_allInOneAction_yellow':       ['Disconnected',                          u"断开"],
        'button_allInOneAction_green':        ['Ready',                                 u"就绪"],
        'button_allInOneAction_blue':         ['Success',                               u"成功"],
        'button_allInOneAction_red':          ['Failure',                               u"失败"],

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
kRevision_1_0_1_en =  "【v1.0.1】 \n" + \
                      "  Bug: \n" + \
                      "     1. Cannot download large image file (eg 6.8MB) in some case \n\n"
kRevision_1_0_1_zh = u"【v1.0.1】 \n" + \
                     u"  缺陷: \n" + \
                     u"     1. 当输入的源image文件非常大时(比如6.8MB)，下载可能会超时失败 \n\n"

kMsgLanguageContentDict = {
        'homePage_title':                     ['Home Page',                             u"项目主页"],
        'homePage_info':                      ['https://github.com/JayHeng/RT-Flash.git \n',                                       u"https://github.com/JayHeng/RT-Flash.git \n"],
        'aboutAuthor_title':                  ['About Author',                          u"关于作者"],
        'aboutAuthor_author':                 [u"Author:  痞子衡 \n",                   u"作者：痞子衡 \n"],
        'aboutAuthor_email1':                 ['Email:     jie.heng@nxp.com \n',        u"邮箱：jie.heng@nxp.com \n"],
        'aboutAuthor_email2':                 ['Email:     hengjie1989@foxmail.com \n', u"邮箱：hengjie1989@foxmail.com \n"],
        'aboutAuthor_blog':                   [u"Blog:      痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n",                   u"博客：痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"],
        'revisionHistory_title':              ['Revision History',                      u"版本历史"],
        'revisionHistory_v1_0_0':             [kRevision_1_0_0_en,                      kRevision_1_0_0_zh],
        'revisionHistory_v1_0_1':             [kRevision_1_0_1_en,                      kRevision_1_0_1_zh],

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

        'downloadError_notValidImage':        ['Please select one application image file (.sb )!',
                                              u"请先选择一个.sb文件！"],
        'downloadError_failToDownload':       ['Failed to download application image file (.sb )!',
                                              u"未能成功下载.sb文件！"],
        'downloadInfo_success':               ['Application image file (.sb ) has been downloaded successfully!',
                                              u".sb文件已被成功下载！"],
}