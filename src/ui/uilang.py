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

        'sText_mcuDevice':                    ['i.MX RT Device:',                       u"i.MX RT型号："],
        'sText_usbPort':                      ['Download Port:',                        u"下载端口："],
        'sText_appPath':                      ['Application Image File(.sb):',          u"源应用程序镜像文件(.sb)："],
        'button_allInOneAction':              ['All-In-One Action',                     u"一键下载"],

}

kRevision_1_0_0_en =  "【v1.0.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT1021, i.MXRT1051/1052, i.MXRT1061/1062, i.MXRT1064 SIP \n" + \
                      "     2. Support USB-HID serial downloader mode \n" + \
                      "     3. Support for loading .sb image file into boot device \n\n"
kRevision_1_0_0_zh = u"【v1.0.0】 \n" + \
                     u"  特性: \n" + \
                     u"     1. 支持i.MXRT全系列MCU，包含i.MXRT1021、i.MXRT1051/1052、i.MXRT1061/1062、i.MXRT1064 SIP \n" + \
                     u"     2. 支持USB-HID串行下载方式（USB设备自动识别） \n" + \
                     u"     3. 支持下载.sb格式的image文件进主动启动设备 \n\n"

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

        'connectError_failToJumpToFl':        ['Failed to jump to Flashloader, Reset board and try again!',
                                              u"MCU已进入ROM SDP模式，但未能跳转Flashloader，请复位板子再试！"],
        'connectError_notValidSignedFl':      ['Signed flashloader(ivt_flashloader_signed.bin) is not found!',
                                              u"没有找到签名的Flashloader文件(ivt_flashloader_signed.bin)！"],
        'connectError_doubleCheckBmod':       ['Put MCU in SDP mode (BMOD[1:0] pins = 2\'b01), Reset board and try again!',
                                              u"将BMOD[1:0]引脚状态设置为2\'b01，然后复位板子再试！"],
        'connectError_failToPingFl':          ['Failed to ping Flashloader, Reset board and try again!',
                                              u"MCU未能与Flashloader建立连接，请复位板子再试！"],
        'connectInfo_readyForDownload':       ['Connected, Ready for downloading!',
                                              u"已连接，可以进行下载操作！"],

        'downloadError_notValidImage':        ['Please select one application image file (.sb )!',
                                              u"请先选择一个.sb文件！"],
        'downloadError_failToDownload':       ['Failded to download application image file (.sb )!',
                                              u"未能成功下载.sb文件！"],
        'downloadInfo_success':               ['Application image file (.sb ) has been downloaded successfully!',
                                              u".sb文件已被成功下载！"],
}