#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import math
import pywinusb.hid
import uidef
import uilang
sys.path.append(os.path.abspath(".."))
from win import flashWin
from run import rundef

kRetryDetectTimes = 5

s_isGaugeWorking = False
s_curGauge = 0
s_maxGauge = 0
s_gaugeIntervalSec = 1

class flashUi(flashWin.flashWin):

    def __init__(self, parent):
        flashWin.flashWin.__init__(self, parent)
        self.m_bitmap_nxp.SetBitmap(wx.Bitmap( u"../img/logo_nxp.png", wx.BITMAP_TYPE_ANY ))

        self.exeBinRoot = os.getcwd()
        self.exeTopRoot = os.path.dirname(self.exeBinRoot)
        exeMainFile = os.path.join(self.exeTopRoot, 'src', 'main.py')
        if not os.path.isfile(exeMainFile):
            self.exeTopRoot = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self._initStatusBar()
        self.updateConnectStatus()
        self.languageIndex = 0
        self._initLanguage()
        self.setLanguage()
        self.isAutoUsbDetection = None
        self._initUsbDetection()
        self.setUsbDetection()
        self.mcuDevice = None
        self.setTargetSetupValue()
        self.usbhidVid = None
        self.usbhidPid = None
        self.isUsbhidConnected = False
        self.usbhidToConnect = [None] * 2
        self._initPortSetupValue()
        self.sbAppPath = None

    def _initStatusBar( self ):
        self.m_statusBar.SetFieldsCount(2)
        self.m_statusBar.SetStatusWidths([150, 350])
        self.setHabStatus(u"N/A")
        self.setInfoStatus('N/A')

    def setHabStatus( self, habStatus ):
        self.m_statusBar.SetStatusText(u"【HAB Status: " + habStatus + "】", 0)

    def setInfoStatus( self, infoStatus ):
        infoStatus = 'Info: ' + infoStatus
        self.m_statusBar.SetStatusText(infoStatus.encode('utf-8'), 1)

    def _initUsbDetection( self ):
        self.m_menuItem_usbDetectionAuto.Check(True)
        self.m_menuItem_usbDetectionStatic.Check(False)

    def setUsbDetection( self ):
        self.isAutoUsbDetection = self.m_menuItem_usbDetectionAuto.IsChecked()

    def setTargetSetupValue( self ):
        self.mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())

    def _initPortSetupValue( self ):
        usbIdList = self.getUsbid()
        self.setPortSetupValue(uidef.kConnectStage_Rom, usbIdList)

    def task_doDetectUsbhid( self ):
        while True:
            self._retryToDetectUsbhidDevice(False)
            time.sleep(1)

    def _retryToDetectUsbhidDevice( self, needToRetry = True ):
        usbVid = [None]
        usbPid = [None]
        self.isUsbhidConnected = False
        retryCnt = 1
        if needToRetry:
            retryCnt = kRetryDetectTimes
        while retryCnt > 0:
            # Auto detect USB-HID device
            hidFilter = pywinusb.hid.HidDeviceFilter(vendor_id = int(self.usbhidToConnect[0], 16), product_id = int(self.usbhidToConnect[1], 16))
            hidDevice = hidFilter.get_devices()
            if (not self.isAutoUsbDetection) or (len(hidDevice) > 0):
                self.isUsbhidConnected = True
                usbVid[0] = self.usbhidToConnect[0]
                usbPid[0] = self.usbhidToConnect[1]
                break
            retryCnt = retryCnt - 1
            if retryCnt != 0:
                time.sleep(2)
            else:
                usbVid[0] = 'N/A'
                usbPid[0] = usbVid[0]
        if self.usbhidVid != usbVid[0] or self.usbhidPid != usbPid[0]:
            self.usbhidVid = usbVid[0]
            self.usbhidPid = usbPid[0]
            self.m_textCtrl_usbPort.Clear()
            self.m_textCtrl_usbPort.write("USB-HID Device: " + self.usbhidVid + "," + self.usbhidPid)

    def adjustPortSetupValue( self, connectStage=uidef.kConnectStage_Rom, usbIdList=[] ):
        if connectStage == uidef.kConnectStage_Rom:
            self.usbhidToConnect[0] = usbIdList[0]
            self.usbhidToConnect[1] = usbIdList[1]
            self._retryToDetectUsbhidDevice(False)
        elif connectStage == uidef.kConnectStage_Flashloader:
            self.usbhidToConnect[0] = usbIdList[2]
            self.usbhidToConnect[1] = usbIdList[3]
            self._retryToDetectUsbhidDevice(False)
        else:
            pass

    def setPortSetupValue( self, connectStage=uidef.kConnectStage_Rom, usbIdList=[], retryToDetectUsb=False ):
        self.adjustPortSetupValue(connectStage, usbIdList)
        self.updatePortSetupValue(retryToDetectUsb)

    def updatePortSetupValue( self, retryToDetectUsb=False ):
        status = True
        if not self.isUsbhidConnected:
            self._retryToDetectUsbhidDevice(retryToDetectUsb)
            if not self.isUsbhidConnected:
                status = False
        return status

    def updateConnectStatus( self, color='black' ):
        if color == 'black':
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0x80, 0x80, 0x80 ) )
        elif color == 'yellow':
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0xff, 0xff, 0x80 ) )
        elif color == 'green':
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0x80, 0xff, 0x80 ) )
        elif color == 'blue':
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0x00, 0x80, 0xff ) )
        elif color == 'red':
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0xff, 0x80, 0x80 ) )
        else:
            pass

    def task_doIncreaseGauge( self ):
        while True:
            self._increaseGauge()
            global s_gaugeIntervalSec
            time.sleep(s_gaugeIntervalSec)

    def _increaseGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        global s_gaugeIntervalSec
        if s_isGaugeWorking:
            gaugePercentage = s_curGauge * 1.0 / s_maxGauge
            if gaugePercentage <= 0.9:
                s_gaugeIntervalSec = int(gaugePercentage  / 0.1) * 0.5 + 0.5
                self.m_gauge_action.SetValue(s_curGauge)
                s_curGauge += 1
            self.updateCostTime()

    def initGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        global s_gaugeIntervalSec
        s_isGaugeWorking = True
        s_curGauge = 0
        s_gaugeIntervalSec = 0.5
        s_maxGauge = self.m_gauge_action.GetRange()
        self.m_gauge_action.SetValue(s_curGauge)

    def deinitGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        global s_gaugeIntervalSec
        s_isGaugeWorking = False
        s_curGauge = s_maxGauge
        s_gaugeIntervalSec = 1
        self.m_gauge_action.SetValue(s_maxGauge)

    def getUserAppFilePath( self ):
        appPath = self.m_filePicker_appPath.GetPath()
        self.sbAppPath = appPath.encode('utf-8').encode("gbk")

    def _initLanguage( self ):
        self.m_menuItem_english.Check(True)
        self.m_menuItem_chinese.Check(False)

    def _getLastLangIndex( self ):
        label = self.m_staticText_mcuDevice.GetLabel()
        labelList = uilang.kMainLanguageContentDict['sText_mcuDevice'][:]
        for index in range(len(labelList)):
            if label == labelList[index]:
                return index
        return 0

    def setLanguage( self ):
        isEnglishLanguage = self.m_menuItem_english.IsChecked()
        lastIndex = self._getLastLangIndex()
        langIndex = 0
        if isEnglishLanguage:
            langIndex = uilang.kLanguageIndex_English
        else:
            langIndex = uilang.kLanguageIndex_Chinese
        self.languageIndex = langIndex
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_File, uilang.kMainLanguageContentDict['menu_file'][langIndex])
        self.m_menuItem_exit.SetItemLabel(uilang.kMainLanguageContentDict['mItem_exit'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Edit, uilang.kMainLanguageContentDict['menu_edit'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_View, uilang.kMainLanguageContentDict['menu_view'][langIndex])
        # Hard way to set label for submenu
        self.m_menu_view.SetLabel(self.m_menu_view.FindItem(uilang.kMainLanguageContentDict['subMenu_language'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_language'][langIndex])
        self.m_menuItem_english.SetItemLabel(uilang.kMainLanguageContentDict['mItem_english'][langIndex])
        self.m_menuItem_chinese.SetItemLabel(uilang.kMainLanguageContentDict['mItem_chinese'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Tools, uilang.kMainLanguageContentDict['menu_tools'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_usbDetection'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_usbDetection'][langIndex])
        self.m_menuItem_usbDetectionAuto.SetItemLabel(uilang.kMainLanguageContentDict['mItem_usbDetectionAuto'][langIndex])
        self.m_menuItem_usbDetectionStatic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_usbDetectionStatic'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Window, uilang.kMainLanguageContentDict['menu_window'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Help, uilang.kMainLanguageContentDict['menu_help'][langIndex])
        self.m_menuItem_homePage.SetItemLabel(uilang.kMainLanguageContentDict['mItem_homePage'][langIndex])
        self.m_menuItem_aboutAuthor.SetItemLabel(uilang.kMainLanguageContentDict['mItem_aboutAuthor'][langIndex])
        self.m_menuItem_revisionHistory.SetItemLabel(uilang.kMainLanguageContentDict['mItem_revisionHistory'][langIndex])

        self.m_notebook_targetSetup.SetPageText(0, uilang.kMainLanguageContentDict['panel_targetSetup'][langIndex])
        self.m_staticText_mcuDevice.SetLabel(uilang.kMainLanguageContentDict['sText_mcuDevice'][langIndex])

        self.m_notebook_portSetup.SetPageText(0, uilang.kMainLanguageContentDict['panel_portSetup'][langIndex])
        self.m_radioBtn_uart.SetLabel(uilang.kMainLanguageContentDict['radioBtn_uart'][langIndex])
        self.m_radioBtn_usbhid.SetLabel(uilang.kMainLanguageContentDict['radioBtn_usbhid'][langIndex])

        self.m_notebook_imageSeq.SetPageText(uilang.kPanelIndex_ImageSeq, uilang.kMainLanguageContentDict['panel_imageSeq'][langIndex])
        self.m_staticText_appPath.SetLabel(uilang.kMainLanguageContentDict['sText_appPath'][langIndex])
        self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction'][langIndex])

    def setCostTime( self, costTimeSec ):
        minValueStr = '00'
        secValueStr = '00'
        millisecValueStr = '000'
        if costTimeSec != 0:
            costTimeSecMod = math.modf(costTimeSec)
            minValue = int(costTimeSecMod[1] / 60)
            if minValue < 10:
                minValueStr = '0' + str(minValue)
            elif minValue <= 59:
                minValueStr = str(minValue)
            else:
                minValueStr = 'xx'
            secValue = int(costTimeSecMod[1]) % 60
            if secValue < 10:
                secValueStr = '0' + str(secValue)
            else:
                secValueStr = str(secValue)
            millisecValue = int(costTimeSecMod[0] * 1000)
            if millisecValue < 10:
                millisecValueStr = '00' + str(millisecValue)
            elif millisecValue < 100:
                millisecValueStr = '0' + str(millisecValue)
            else:
                millisecValueStr = str(millisecValue)
        self.m_staticText_costTime.SetLabel(' ' + minValueStr + ':' + secValueStr + '.' + millisecValueStr)

    def updateCostTime( self ):
        curTime = time.time()
        self.setCostTime(curTime - self.lastTime)
