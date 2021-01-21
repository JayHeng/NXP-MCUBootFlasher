#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import math
import serial.tools.list_ports
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

        self.isDebugLogOn = True
        if self.isDebugLogOn:
            self.debugLogFile = os.path.join(self.exeTopRoot, 'bin', 'debug_log.txt')
            self.debugLogFileObj = open(self.debugLogFile, 'wb')

        self.connectStage = [uidef.kConnectStage_Rom] * uidef.kMaxMfgBoards
        self.connectStatusColor = None

        self.isUartPortSelected = None
        self.isUsbhidPortSelected = None
        self.connectedBoards = 0
        self.detectedBoards = 0
        self.serialPortIndex = 0

        self._initStatusBar()
        self.languageIndex = 0
        self._initLanguage()
        self.setLanguage()
        self.updateConnectStatus()
        self.isDymaticUsbDetection = None
        self._initUsbDetection()
        self.setUsbDetection()
        self.mcuSeries = None
        self.mcuDevice = None
        self._initTargetSetupValue()
        self.setTargetSetupValue()
        self.uartComPort = [None]
        self.uartBaudrate = [None]
        self.isUsbhidConnected = [False] * uidef.kMaxMfgBoards
        self.usbhidToConnect = [[None] * 2] * uidef.kMaxMfgBoards
        self.usbDevicePath = []
        for i in range(uidef.kMaxMfgBoards):
            self.usbDevicePath.append({'rom':None, 'flashloader':None})
        self.usbDeviceSlotId = [''] * uidef.kMaxMfgBoards
        self._initPortSetupValue()
        self._initMcuBoards()
        self.setMcuBoards()
        self.sbAppFilePath = None
        self.sbAppFolderPath = None
        self.sbAppFiles = []

    def writeDebugLog( self, logStr):
        if self.isDebugLogOn:
            self.debugLogFileObj.write(logStr + " \r\n")

    def closeDebugLog( self ):
        if self.isDebugLogOn:
            self.debugLogFileObj.close()

    def _initStatusBar( self ):
        self.m_statusBar.SetFieldsCount(2)
        self.m_statusBar.SetStatusWidths([130, 370])
        self.setHabStatus(u"N/A")
        self.setInfoStatus('N/A')

    def setHabStatus( self, habStatus ):
        self.m_statusBar.SetStatusText(u"【HAB Status: " + habStatus + "】", 0)

    def setInfoStatus( self, infoStatus ):
        self.m_statusBar.SetStatusText(infoStatus.encode('utf-8'), 1)

    def _initUsbDetection( self ):
        self.m_menuItem_usbDetectionDynamic.Check(True)
        self.m_menuItem_usbDetectionStatic.Check(False)

    def setUsbDetection( self ):
        self.isDymaticUsbDetection = self.m_menuItem_usbDetectionDynamic.IsChecked()

    def _initTargetSetupValue( self ):
        self.m_choice_mcuDevice.Clear()
        self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_Latest)
        self.m_choice_mcuDevice.SetSelection(6)

    def setTargetSetupValue( self ):
        self.mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        if self.mcuDevice in uidef.kMcuDevice_iMXRTxxx:
            self.mcuSeries = uidef.kMcuSeries_iMXRTxxx
        elif self.mcuDevice in uidef.kMcuDevice_iMXRT10yy:
            self.mcuSeries = uidef.kMcuSeries_iMXRT10yy
        elif self.mcuDevice in uidef.kMcuDevice_iMXRT11yy:
            self.mcuSeries = uidef.kMcuSeries_iMXRT11yy
        elif self.mcuDevice in uidef.kMcuDevice_LPC:
            self.mcuSeries = uidef.kMcuSeries_LPC
        elif self.mcuDevice in uidef.kMcuDevice_Kinetis:
            self.mcuSeries = uidef.kMcuSeries_Kinetis
        else:
            pass

    def _adjustSerialPortIndexValue( self ):
        itemNum = 0
        self.m_staticText_detectedBoardNum.SetLabel(str(self.detectedBoards))
        if self.isUartPortSelected:
            itemNum = self.connectedBoards
        elif self.isUsbhidPortSelected:
            itemNum = min(self.connectedBoards, self.detectedBoards)
        else:
            pass
        lastItem = self.m_choice_serialPortIndex.GetString(self.m_choice_serialPortIndex.GetSelection())
        itemList = range(itemNum)
        for i in range(itemNum):
            itemList[i] = str(i)
        self.m_choice_serialPortIndex.Clear()
        self.m_choice_serialPortIndex.SetItems(itemList)
        if lastItem in itemList:
            self.m_choice_serialPortIndex.SetSelection(self.m_choice_serialPortIndex.FindString(lastItem))
        else:
            self.m_choice_serialPortIndex.SetSelection(0)

    def _recoverLastSerialPort( self ):
        if self.isUartPortSelected:
            if len(self.uartComPort) > self.serialPortIndex and self.uartComPort[self.serialPortIndex] != None:
                self.m_choice_portVid.SetSelection(self.m_choice_portVid.FindString(self.uartComPort[self.serialPortIndex]))
                self.m_choice_baudPid.SetSelection(self.m_choice_baudPid.FindString(self.uartBaudrate[self.serialPortIndex]))
        elif self.isUsbhidPortSelected:
            pass
        else:
            pass

    def _setUsbDetectedBoardNum( self, num):
        if self.detectedBoards != num:
            self.m_staticText_detectedBoardNum.SetLabel(str(num))
            self.detectedBoards = num
            self._adjustSerialPortIndexValue()

    def _initMcuBoards( self ):
        self.m_textCtrl_connectedBoards.Clear()
        self.m_textCtrl_connectedBoards.write('1')
        self._setUsbDetectedBoardNum(0)

    def setMcuBoards( self ):
        try:
            boards = int(self.m_textCtrl_connectedBoards.GetLineText(0))
            self.connectedBoards = boards
            self._adjustSerialPortIndexValue()
        except:
            self.m_textCtrl_connectedBoards.Clear()
            self.m_textCtrl_connectedBoards.write(str(self.connectedBoards))

    def _updateSerialPortInfo( self ):
        if self.isUartPortSelected:
            if self.serialPortIndex < len(self.uartComPort) and self.uartComPort[self.serialPortIndex] != None:
                self.m_staticText_portInfo.SetLabel(uilang.kMsgLanguageContentDict['portInfo_alreadySet'][self.languageIndex])
            else:
                self.m_staticText_portInfo.SetLabel(uilang.kMsgLanguageContentDict['portInfo_notSet'][self.languageIndex])
        elif self.isUsbhidPortSelected:
            self.m_staticText_portInfo.SetLabel('N/A')
        else:
            pass

    def setSerialPortIndex( self ):
        self.serialPortIndex = int(self.m_choice_serialPortIndex.GetString(self.m_choice_serialPortIndex.GetSelection()))
        self._recoverLastSerialPort()
        self._updateSerialPortInfo()

    def _initPortSetupValue( self ):
        self.m_radioBtn_uart.SetValue(False)
        self.m_radioBtn_usbhid.SetValue(True)
        usbIdList = self.getUsbid()
        for i in range(uidef.kMaxMfgBoards):
            self.setPortSetupValue(i, uidef.kConnectStage_Rom, usbIdList)

    def task_doDetectUsbhid( self ):
        while True:
            if self.isUsbhidPortSelected:
                deviceNum = 0
                if self.isDymaticUsbDetection:
                    deviceNum = uidef.kMaxMfgBoards
                else:
                    deviceNum = 1
                for i in range(deviceNum):
                    self._retryToDetectUsbhidDevice(i, False)
            time.sleep(1)

    def _retryToDetectUsbhidDevice( self, deviceIndex=0, needToRetry = True ):
        self.writeDebugLog("Entering _retryToDetectUsbhidDevice(), deviceIndex =" + str(deviceIndex))
        usbVid = [None]
        usbPid = [None]
        self.isUsbhidConnected[deviceIndex] = False
        retryCnt = 1
        if needToRetry:
            retryCnt = kRetryDetectTimes
        while retryCnt > 0:
            # Auto detect USB-HID device
            hidFilter = pywinusb.hid.HidDeviceFilter(vendor_id = int(self.usbhidToConnect[deviceIndex][0], 16), product_id = int(self.usbhidToConnect[deviceIndex][1], 16))
            hidDevice = hidFilter.get_devices()
            #------------------------------------------------
            # Example RT1170
            # Port 1
            #rom: \\?\hid#vid_1fc9&pid_013d#a&2eb8245&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
            #fl:  \\?\hid#vid_15a2&pid_0073#a&20680ae4&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
            # Port 2
            #rom: \\?\hid#vid_1fc9&pid_013d#9&17f9e48f&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
            #fl:  \\?\hid#vid_15a2&pid_0073#9&35766d2e&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
            #------------------------------------------------
            # Example RT1050
            # Port 2
            #rom: \\?\hid#vid_1fc9&pid_0130#9&2897791a&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
            #fl:  \\?\hid#vid_15a2&pid_0073#9&35766d2e&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
            self._setUsbDetectedBoardNum(len(hidDevice))
            if (not self.isDymaticUsbDetection) or (len(hidDevice) > 0):
                #----------------------------------------------------------------
                if self.connectStage[deviceIndex] == uidef.kConnectStage_Rom:
                    romHidDevice = hidDevice
                    for i in range(len(romHidDevice)):
                        self.writeDebugLog("Stage: ROM, Loop = " + str(i)+ ", Checking " + romHidDevice[i].device_path)
                        if self.usbDevicePath[deviceIndex]['rom'] == romHidDevice[i].device_path:
                            break
                        elif self.usbDevicePath[deviceIndex]['rom'] == None:
                            hasThisPath = False
                            nullDeviceIndex_1st = 0
                            j = len(self.usbDevicePath) - 1
                            while (j >= 0):
                                if self.usbDevicePath[j]['rom'] == None:
                                    nullDeviceIndex_1st = j
                                elif self.usbDevicePath[j]['rom'] == romHidDevice[i].device_path:
                                    hasThisPath = True
                                    continue
                                j -= 1
                            # If this path was in usbDevicePath, we don't need to save it here
                            if hasThisPath:
                                break
                            # If deviceIndex is not the first null device in usbDevicePath, we don't need to savt it here
                            elif nullDeviceIndex_1st != deviceIndex:
                                break
                            romUsbPath = romHidDevice[i].device_path
                            flUsbPath = self.usbDevicePath[deviceIndex]['flashloader']
                            if flUsbPath == None:
                                self.usbDevicePath[deviceIndex]['rom'] = romUsbPath[:]
                                self.writeDebugLog("Set self.usbDevicePath[" + str(deviceIndex) + "]['rom']")
                                break
                            else:
                                if (romUsbPath[26] == flUsbPath[26]) and \
                                   (romUsbPath[27] == flUsbPath[27]):
                                    if romUsbPath[27] == "&":
                                        self.usbDevicePath[deviceIndex]['rom'] = romUsbPath[:]
                                        self.writeDebugLog("Set self.usbDevicePath[" + str(deviceIndex) + "]['rom']")
                                        break
                                    elif flUsbPath[27] == "&":
                                        continue
                                    else:
                                        if (romUsbPath[28] == flUsbPath[28]):
                                            if romUsbPath[28] == "&":
                                                self.usbDevicePath[deviceIndex]['rom'] = romUsbPath[:]
                                                self.writeDebugLog("Set self.usbDevicePath[" + str(deviceIndex) + "]['rom']")
                                                break
                        else:
                            pass
                elif self.connectStage[deviceIndex] == uidef.kConnectStage_Flashloader:
                    flHidDevice = hidDevice
                    for i in range(len(flHidDevice)):
                        self.writeDebugLog("Stage: FLD, Loop = " + str(i)+ ", Checking " + flHidDevice[i].device_path)
                        romUsbPath = self.usbDevicePath[deviceIndex]['rom']
                        flUsbPath = flHidDevice[i].device_path
                        if romUsbPath != None and romUsbPath[25] == "#":
                            # max 256 usb instance
                            if (romUsbPath[26] == flUsbPath[26]) and \
                               (romUsbPath[27] == flUsbPath[27]):
                                if romUsbPath[27] == "&":
                                    self.usbDevicePath[deviceIndex]['flashloader'] = flUsbPath[:]
                                    self.usbDeviceSlotId[deviceIndex] = flUsbPath[26]
                                    self.writeDebugLog("Set self.usbDevicePath[" + str(deviceIndex) + "]['flashloader']")
                                    break
                                elif flUsbPath[27] == "&":
                                    continue
                                else:
                                    if (romUsbPath[28] == flUsbPath[28]):
                                        if romUsbPath[28] == "&":
                                            self.usbDevicePath[deviceIndex]['flashloader'] = flUsbPath[:]
                                            self.usbDeviceSlotId[deviceIndex] = flUsbPath[26:28]
                                            self.writeDebugLog("Set self.usbDevicePath[" + str(deviceIndex) + "]['flashloader']")
                                            break
                else:
                    pass
                #----------------------------------------------------------------
                self.isUsbhidConnected[deviceIndex] = True
                if self.connectStatusColor == 'yellow':
                    self.updateConnectStatus('black')
                if self.isDymaticUsbDetection:
                    usbVid[0] = self.tgt.romUsbVid
                    usbPid[0] = self.tgt.romUsbPid
                else:
                    usbVid[0] = self.usbhidToConnect[deviceIndex][0]
                    usbPid[0] = self.usbhidToConnect[deviceIndex][1]
                break
            retryCnt = retryCnt - 1
            if retryCnt != 0:
                time.sleep(2)
            else:
                usbVid[0] = 'N/A - Not Found'
                usbPid[0] = 'N/A - Not Found'
        if not self.isUsbhidConnected[deviceIndex]:
            self.updateConnectStatus('yellow')
        if self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection()) != usbVid[0] or \
           self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection()) != usbPid[0]:
            self.m_choice_portVid.Clear()
            self.m_choice_portVid.SetItems(usbVid)
            self.m_choice_portVid.SetSelection(0)
            self.m_choice_baudPid.Clear()
            self.m_choice_baudPid.SetItems(usbPid)
            self.m_choice_baudPid.SetSelection(0)

    def adjustPortSetupValue( self, deviceIndex=0, connectStage=uidef.kConnectStage_Rom, usbIdList=[] ):
        self.isUartPortSelected = self.m_radioBtn_uart.GetValue()
        self.isUsbhidPortSelected = self.m_radioBtn_usbhid.GetValue()
        if self.isUartPortSelected:
            self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_comPort'][self.languageIndex])
            self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_baudrate'][self.languageIndex])
            # Auto detect available ports
            comports = list(serial.tools.list_ports.comports())
            ports = [None] * len(comports)
            for i in range(len(comports)):
                comport = list(comports[i])
                ports[i] = comport[0]
            lastPort = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
            lastBaud = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
            self.m_choice_portVid.Clear()
            self.m_choice_portVid.SetItems(ports)
            if lastPort in ports:
                self.m_choice_portVid.SetSelection(self.m_choice_portVid.FindString(lastPort))
            else:
                self.m_choice_portVid.SetSelection(0)
            baudItems = ['115200']
            if connectStage == uidef.kConnectStage_Rom:
                baudItems = rundef.kUartSpeed_Sdphost
            elif connectStage == uidef.kConnectStage_Flashloader:
                baudItems = rundef.kUartSpeed_Blhost
            else:
                pass
            self.m_choice_baudPid.Clear()
            self.m_choice_baudPid.SetItems(baudItems)
            if lastBaud in baudItems:
                self.m_choice_baudPid.SetSelection(self.m_choice_baudPid.FindString(lastBaud))
            else:
                self.m_choice_baudPid.SetSelection(0)
        elif self.isUsbhidPortSelected:
            self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_vid'][self.languageIndex])
            self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_pid'][self.languageIndex])
            if connectStage == uidef.kConnectStage_Rom:
                self.usbhidToConnect[deviceIndex][0] = usbIdList[0]
                self.usbhidToConnect[deviceIndex][1] = usbIdList[1]
                self._retryToDetectUsbhidDevice(deviceIndex, False)
            elif connectStage == uidef.kConnectStage_Flashloader:
                self.usbhidToConnect[deviceIndex][0] = usbIdList[2]
                self.usbhidToConnect[deviceIndex][1] = usbIdList[3]
                self._retryToDetectUsbhidDevice(deviceIndex, False)
            else:
                pass
        else:
            pass

    def setPortSetupValue( self, deviceIndex=0, connectStage=uidef.kConnectStage_Rom, usbIdList=[], retryToDetectUsb=False ):
        self.adjustPortSetupValue(deviceIndex, connectStage, usbIdList)
        self.updatePortSetupValue(deviceIndex, retryToDetectUsb)
        self._adjustSerialPortIndexValue()

    def updatePortSetupValue( self, deviceIndex=0, retryToDetectUsb=False ):
        status = True
        self.isUartPortSelected = self.m_radioBtn_uart.GetValue()
        self.isUsbhidPortSelected = self.m_radioBtn_usbhid.GetValue()
        if self.isUartPortSelected:
            if len(self.uartComPort) <= self.serialPortIndex:
                for i in range(self.serialPortIndex - len(self.uartComPort) + 1):
                    self.uartComPort.append(None)
                    self.uartBaudrate.append(None)
            self.uartComPort[self.serialPortIndex] = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
            self.uartBaudrate[self.serialPortIndex] = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
            self.detectedBoards = 0
            for i in range(len(self.uartComPort)):
                if self.uartComPort[i] != None:
                    self.detectedBoards += 1
            self.m_staticText_detectedBoardNum.SetLabel(str(self.detectedBoards))
        elif self.isUsbhidPortSelected:
            if not self.isUsbhidConnected[deviceIndex]:
                self._retryToDetectUsbhidDevice(deviceIndex, retryToDetectUsb)
                if not self.isUsbhidConnected[deviceIndex]:
                    status = False
        else:
            pass
        self._updateSerialPortInfo()
        return status

    def updateConnectStatus( self, color='black' ):
        self.connectStatusColor = color
        if color == 'black':
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction_black'][self.languageIndex])
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0x80, 0x80, 0x80 ) )
        elif color == 'yellow':
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction_yellow'][self.languageIndex])
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0xff, 0xff, 0x80 ) )
        elif color == 'green':
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction_green'][self.languageIndex])
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0x80, 0xff, 0x80 ) )
        elif color == 'blue':
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction_blue'][self.languageIndex])
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0x00, 0x80, 0xff ) )
        elif color == 'red':
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction_red'][self.languageIndex])
            self.m_button_allInOneAction.SetBackgroundColour( wx.Colour( 0xff, 0x80, 0x80 ) )
        else:
            pass

    def updateSlotStatus( self, slotIdx, color='black' ):
        if slotIdx == 0:
            slotObj = self.m_button_slot0
        elif slotIdx == 1:
            slotObj = self.m_button_slot1
        elif slotIdx == 2:
            slotObj = self.m_button_slot2
        elif slotIdx == 3:
            slotObj = self.m_button_slot3
        elif slotIdx == 4:
            slotObj = self.m_button_slot4
        elif slotIdx == 5:
            slotObj = self.m_button_slot5
        elif slotIdx == 6:
            slotObj = self.m_button_slot6
        elif slotIdx == 7:
            slotObj = self.m_button_slot7
        else:
            pass
        slotObj.SetLabel(uilang.kMainLanguageContentDict['button_slot'][self.languageIndex] + str(slotIdx) + ', #' + self.usbDeviceSlotId[slotIdx])
        if color == 'black':
            slotObj.SetBackgroundColour( wx.Colour( 0x80, 0x80, 0x80 ) )
        elif color == 'yellow':
            slotObj.SetBackgroundColour( wx.Colour( 0xff, 0xff, 0x80 ) )
        elif color == 'green':
            slotObj.SetBackgroundColour( wx.Colour( 0x80, 0xff, 0x80 ) )
        elif color == 'blue':
            slotObj.SetBackgroundColour( wx.Colour( 0x00, 0x80, 0xff ) )
        elif color == 'red':
            slotObj.SetBackgroundColour( wx.Colour( 0xff, 0x80, 0x80 ) )
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
        appFilePath = self.m_filePicker_appFilePath.GetPath()
        self.sbAppFilePath = appFilePath.encode('utf-8').encode("gbk")
        self.sbAppFiles = []
        self.sbAppFiles.append(self.sbAppFilePath)

    def getUserAppFolderPath( self ):
        appFolderPath = self.m_dirPicker_appFolderPath.GetPath()
        self.sbAppFolderPath = appFolderPath.encode('utf-8').encode("gbk")
        sbAppFiles = []
        files = os.listdir(self.sbAppFolderPath)
        for file in files:
            if os.path.splitext(file)[1] == '.sb':
                sbAppFiles.append(os.path.join(self.sbAppFolderPath, file))
        self.sbAppFiles = sbAppFiles[:]
        if len(sbAppFiles) == 0:
            self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadError_notValidImageFolder'][self.languageIndex])

    def resetUserAppFolderPath( self ):
        self.m_dirPicker_appFolderPath.SetPath('')

    def _initLanguage( self ):
        self.m_menuItem_english.Check(True)
        self.m_menuItem_chinese.Check(False)

    def setDownloadOperationResults( self, totalCnt, successCnt=0 ):
        failureCnt = 0
        if totalCnt:
            failureCnt = totalCnt - successCnt
        else:
            successCnt = 0
        self.m_staticText_successfulBoardNum.SetLabel(str(successCnt))
        self.m_staticText_failedBoardNum.SetLabel(str(failureCnt))

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
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Tools, uilang.kMainLanguageContentDict['menu_tools'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_usbDetection'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_usbDetection'][langIndex])
        self.m_menuItem_usbDetectionDynamic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_usbDetectionDynamic'][langIndex])
        self.m_menuItem_usbDetectionStatic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_usbDetectionStatic'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Window, uilang.kMainLanguageContentDict['menu_window'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Help, uilang.kMainLanguageContentDict['menu_help'][langIndex])
        self.m_menuItem_homePage.SetItemLabel(uilang.kMainLanguageContentDict['mItem_homePage'][langIndex])
        self.m_menuItem_aboutAuthor.SetItemLabel(uilang.kMainLanguageContentDict['mItem_aboutAuthor'][langIndex])
        self.m_menuItem_revisionHistory.SetItemLabel(uilang.kMainLanguageContentDict['mItem_revisionHistory'][langIndex])

        self.m_notebook_setup.SetPageText(0, uilang.kMainLanguageContentDict['panel_setup'][langIndex])
        self.m_staticText_mcuDevice.SetLabel(uilang.kMainLanguageContentDict['sText_mcuDevice'][langIndex])
        self.m_staticText_mcuBoard.SetLabel(uilang.kMainLanguageContentDict['sText_mcuBoard'][langIndex])
        self.m_staticText_connectedBoards.SetLabel(uilang.kMainLanguageContentDict['sText_connectedBoards'][langIndex])
        self.m_staticText_detectedBoards.SetLabel(uilang.kMainLanguageContentDict['sText_detectedBoards'][langIndex])
        self.m_staticText_serialPortIndex.SetLabel(uilang.kMainLanguageContentDict['sText_serialPortIndex'][langIndex])
        self.m_radioBtn_uart.SetLabel(uilang.kMainLanguageContentDict['radioBtn_uart'][langIndex])
        self.m_radioBtn_usbhid.SetLabel(uilang.kMainLanguageContentDict['radioBtn_usbhid'][langIndex])
        if self.isUartPortSelected != None and self.isUartPortSelected:
            self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_comPort'][langIndex])
            self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_baudrate'][langIndex])
        elif self.isUsbhidPortSelected != None and self.isUsbhidPortSelected:
            self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_vid'][langIndex])
            self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_pid'][langIndex])
        else:
            pass

        self.m_notebook_download.SetPageText(uilang.kPanelIndex_Download, uilang.kMainLanguageContentDict['panel_download'][langIndex])
        self.m_staticText_appPath.SetLabel(uilang.kMainLanguageContentDict['sText_appPath'][langIndex])
        self.m_staticText_successfulBoards.SetLabel(uilang.kMainLanguageContentDict['sText_successfulBoards'][langIndex])
        self.m_staticText_failedBoards.SetLabel(uilang.kMainLanguageContentDict['sText_failedBoards'][langIndex])
        self.m_button_slot0.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"0")
        self.m_button_slot1.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"1")
        self.m_button_slot2.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"2")
        self.m_button_slot3.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"3")
        self.m_button_slot4.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"4")
        self.m_button_slot5.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"5")
        self.m_button_slot6.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"6")
        self.m_button_slot7.SetLabel(uilang.kMainLanguageContentDict['button_slot'][langIndex] + u"7")
        if self.connectStatusColor != None:
            self.updateConnectStatus(self.connectStatusColor)

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
