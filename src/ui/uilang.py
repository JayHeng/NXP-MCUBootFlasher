#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

kMenuPosition_Help     = 0x0

kRevision_1_0_0_en =  "【v1.0.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT1021, i.MXRT1051/1052, i.MXRT1061/1062, i.MXRT1064 SIP \n" + \
                      "     2. Support USB-HID serial downloader mode \n" + \
                      "     3. Support for loading .sb image file into boot device \n\n"

kMsgLanguageContentDict = {
        'homePage_title':                     ['Home Page'],
        'homePage_info':                      ['https://github.com/JayHeng/RT-Flash.git \n'],
        'aboutAuthor_title':                  ['About Author'],
        'aboutAuthor_author':                 [u"Author:  痞子衡 \n"],
        'aboutAuthor_email1':                 ['Email:     jie.heng@nxp.com \n'],
        'aboutAuthor_email2':                 ['Email:     hengjie1989@foxmail.com \n'],
        'aboutAuthor_blog':                   [u"Blog:      痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"],
        'revisionHistory_title':              ['Revision History'],
        'revisionHistory_v1_0_0':             [kRevision_1_0_0_en],

        'connectError_failToJumpToFl':        ['Failed to jump to Flashloader, Reset board and try again!'],
        'connectError_notValidSignedFl':      ['Signed flashloader(ivt_flashloader_signed.bin) is not found!'],
        'connectError_doubleCheckBmod':       ['Put MCU in SDP mode (BMOD[1:0] pins = 2\'b01), Reset board and try again!'],
        'connectError_failToPingFl':          ['Failed to ping Flashloader, Reset board and try again!'],
        'connectInfo_readyForDownload':       ['Connected, Ready for downloading!'],

        'downloadError_notValidImage':        ['Please select one application image file (.sb )!'],
        'downloadError_failToDownload':       ['Failded to download application image file (.sb )!'],
        'downloadInfo_success':               ['Application image file (.sb ) has been downloaded successfully!'],
}