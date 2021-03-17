#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import threading
import inspect
import ctypes
from run import runcore
from ui import uidef
from ui import uilang

g_main_win = None
g_task_detectUsbhid = None
g_task_uartAllInOneAction = None
g_task_usbAllInOneAction = [None] * uidef.kMaxMfgBoards
g_task_increaseGauge = None

g_usbAutoDownloadResult_success = [0] * uidef.kMaxMfgBoards
g_usbAutoDownloadResult_total   = [0] * uidef.kMaxMfgBoards

kRetryPingTimes = 5

kBootloaderType_Rom         = 0
kBootloaderType_Flashloader = 1

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class flashMain(runcore.flashRun):

    def __init__(self, parent):
        runcore.flashRun.__init__(self, parent)
        self.lastTime = None
        self.isUartAllInOneActionTaskPending = False
        self.isUsbAllInOneActionTaskPending = [False] * uidef.kMaxMfgBoards

    def _startGaugeTimer( self ):
        self.lastTime = time.time()
        self.initGauge()

    def _stopGaugeTimer( self ):
        self.deinitGauge()
        self.updateCostTime()

    def callbackSetMcuDevice( self, event ):
        self.setTargetSetupValue()
        self.createMcuTarget()
        self._setUartUsbPort()

    def callbackSetConnectedBoards( self, event ):
        self.setMcuBoards()

    def callbackSwitchSerialPortIndex( self, event ):
        self.setSerialPortIndex()

    def _setUartUsbPort( self, deviceIndex=0 ):
        usbIdList = self.getUsbid()
        retryToDetectUsb = False
        self.setPortSetupValue(deviceIndex, self.connectStage[deviceIndex], usbIdList, retryToDetectUsb )

    def callbackSetUartPort( self, event ):
        self._setUartUsbPort()

    def callbackSetUsbhidPort( self, event ):
        self._setUartUsbPort()

    def callbackSetPortVid( self, event ):
        self.updatePortSetupValue()

    def callbackSetBaudPid( self, event ):
        self.updatePortSetupValue()

    def _retryToPingBootloader( self, bootType, deviceIndex=0 ):
        pingStatus = False
        pingCnt = kRetryPingTimes
        while (not pingStatus) and pingCnt > 0:
            if bootType == kBootloaderType_Rom:
                self.writeDebugLog("Entering pingRom(), deviceIndex = " + str(deviceIndex) + ", usb path is " + self.usbDevicePath[deviceIndex]['rom'])
                pingStatus = self.pingRom(deviceIndex)
            elif bootType == kBootloaderType_Flashloader:
                # This is mainly for RT1170 flashloader, but it is also ok for other RT devices
                if self.isUartPortSelected:
                    time.sleep(3)
                if self.usbDevicePath[deviceIndex]['flashloader'] != None:
                    self.connectToDevice(self.connectStage[deviceIndex], deviceIndex)
                    self.writeDebugLog("Entering pingFlashloader(), deviceIndex = " + str(deviceIndex) + ", usb path is " + self.usbDevicePath[deviceIndex]['flashloader'])
                pingStatus = self.pingFlashloader(deviceIndex)
            else:
                pass
            if pingStatus:
                break
            pingCnt = pingCnt - 1
            time.sleep(2)
        return pingStatus

    def _doubleCheckBootModeError( self ):
        if (self.mcuSeries == uidef.kMcuSeries_iMXRT10yy) or \
           (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy):
            self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_doubleCheckBmod'][self.languageIndex])
        elif (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx):
            self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_doubleCheckIsp'][self.languageIndex])
        elif (self.mcuSeries == uidef.kMcuSeries_LPC):
            self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspBoot'][self.languageIndex])
        elif (self.mcuSeries == uidef.kMcuSeries_Kinetis):
            self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])
        else:
            pass

    def _connectFailureHandler( self, deviceIndex=0 ):
        self.connectStage[deviceIndex] = uidef.kConnectStage_Rom
        self.updateConnectStatus('red')
        usbIdList = self.getUsbid()
        self.setPortSetupValue(deviceIndex, self.connectStage[deviceIndex], usbIdList, False )
        self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_checkUsbCable'][self.languageIndex])

    def _connectStateMachine( self, deviceIndex=0 ):
        retryToDetectUsb = False
        connectSteps = 0
        if (self.mcuSeries == uidef.kMcuSeries_iMXRT10yy) or \
           (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy):
            connectSteps = 3
        if (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx) or \
           (self.mcuSeries == uidef.kMcuSeries_LPC) or \
           (self.mcuSeries == uidef.kMcuSeries_Kinetis):
            connectSteps = 2
        else:
            pass
        isConnectionFailureOnce = False
        while connectSteps:
            if not self.updatePortSetupValue(deviceIndex, retryToDetectUsb):
                self._connectFailureHandler(deviceIndex)
                if not isConnectionFailureOnce:
                    isConnectionFailureOnce = True
                    continue
                else:
                    return False
            if self.connectStage[deviceIndex] == uidef.kConnectStage_Rom:
                self.connectToDevice(self.connectStage[deviceIndex], deviceIndex)
                if self._retryToPingBootloader(kBootloaderType_Rom, deviceIndex):
                    if (self.mcuSeries == uidef.kMcuSeries_iMXRT10yy) or \
                       (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy):
                        self.getMcuDeviceHabStatus(deviceIndex)
                        if self.jumpToFlashloader(deviceIndex):
                            self.connectStage[deviceIndex] = uidef.kConnectStage_Flashloader
                            usbIdList = self.getUsbid()
                            self.setPortSetupValue(deviceIndex, self.connectStage[deviceIndex], usbIdList, True )
                        else:
                            self.updateConnectStatus('red')
                            self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_failToJumpToFl'][self.languageIndex])
                            return False
                    elif (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx) or \
                         (self.mcuSeries == uidef.kMcuSeries_LPC) or \
                         (self.mcuSeries == uidef.kMcuSeries_Kinetis):
                        self.updateConnectStatus('green')
                        self.connectStage[deviceIndex] = uidef.kConnectStage_Ready
                    else:
                        pass
                else:
                    self.updateConnectStatus('red')
                    self._doubleCheckBootModeError()
                    return False
            elif self.connectStage[deviceIndex] == uidef.kConnectStage_Flashloader:
                self.connectToDevice(self.connectStage[deviceIndex], deviceIndex)
                if self._retryToPingBootloader(kBootloaderType_Flashloader, deviceIndex):
                    self.updateConnectStatus('green')
                    self.connectStage[deviceIndex] = uidef.kConnectStage_Ready
                else:
                    self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_failToPingFl'][self.languageIndex])
                    self._connectFailureHandler(deviceIndex)
                    return False
            elif self.connectStage[deviceIndex] == uidef.kConnectStage_Ready:
                if connectSteps == 1:
                    self.setInfoStatus(uilang.kMsgLanguageContentDict['connectInfo_readyForDownload'][self.languageIndex])
                    return True
                else:
                    if self._retryToPingBootloader(kBootloaderType_Flashloader, deviceIndex):
                        self.setInfoStatus(uilang.kMsgLanguageContentDict['connectInfo_readyForDownload'][self.languageIndex])
                        return True
                    else:
                        self.connectStage[deviceIndex] = uidef.kConnectStage_Rom
                        connectSteps += 1
            else:
                pass
            connectSteps -= 1

    def task_doUartAllInOneAction( self ):
        while True:
            if self.isUartAllInOneActionTaskPending:
                self._doUartAllInOneAction()
                self.isUartAllInOneActionTaskPending = False
                self._stopGaugeTimer()
            time.sleep(1)

    def _doUartAllInOneAction( self ):
        if len(self.sbAppFiles) == 0:
            self.updateConnectStatus('red')
            self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadError_notValidImage'][self.languageIndex])
            return
        boards = len(self.uartComPort)
        operations = 0
        successes = 0
        for board in range(boards):
            if self.uartComPort[board] == None:
                continue
            operations += 1
            if self._connectStateMachine(board):
                for i in range(len(self.sbAppFiles)):
                    if self.flashSbImage(self.sbAppFiles[i], board):
                        if i == len(self.sbAppFiles) - 1:
                            successes += 1
                        self.updateConnectStatus('blue')
                        self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadInfo_success'][self.languageIndex])
                    else:
                        self.updateConnectStatus('red')
                        break
                self.resetMcuDevice(board)
            self.connectStage[board] = uidef.kConnectStage_Rom
            self._setUartUsbPort()
            self.setDownloadOperationResults(operations, successes)
        self.updateConnectStatus('black')

    def _doUsbxAllInOneAction( self, deviceIndex=0 ):
        while True:
            if self.isUsbAllInOneActionTaskPending[deviceIndex]:
                self._doUsbAutoAllInOneAction(deviceIndex)
                self.isUsbAllInOneActionTaskPending[deviceIndex] = False
                if (deviceIndex == 0) and (not self.isDymaticUsbDetection):
                    self._stopGaugeTimer()
            else:
                if ((deviceIndex == 0) and self.isDymaticUsbDetection) or \
                   (deviceIndex != 0):
                    try:
                        if self.usbDevicePath[deviceIndex]['rom'] != None:
                            self.writeDebugLog("Entering task_doUsbxAllInOneAction(), Set Pending flag " + str(deviceIndex) + ", usb path is " + self.usbDevicePath[deviceIndex]['rom'])
                            self.isUsbAllInOneActionTaskPending[deviceIndex] = True
                            global g_usbAutoDownloadResult_success
                            global g_usbAutoDownloadResult_total
                            self.updateSlotStatus(deviceIndex, 'green', g_usbAutoDownloadResult_success[deviceIndex], g_usbAutoDownloadResult_total[deviceIndex])
                        else:
                            pass
                    except:
                        pass
            time.sleep(1)

    def task_doUsb0AllInOneAction( self ):
        self._doUsbxAllInOneAction(0)

    def task_doUsb1AllInOneAction( self ):
        self._doUsbxAllInOneAction(1)

    def task_doUsb2AllInOneAction( self ):
        self._doUsbxAllInOneAction(2)

    def task_doUsb3AllInOneAction( self ):
        self._doUsbxAllInOneAction(3)

    def task_doUsb4AllInOneAction( self ):
        self._doUsbxAllInOneAction(4)

    def task_doUsb5AllInOneAction( self ):
        self._doUsbxAllInOneAction(5)

    def task_doUsb6AllInOneAction( self ):
        self._doUsbxAllInOneAction(6)

    def task_doUsb7AllInOneAction( self ):
        self._doUsbxAllInOneAction(7)

    def _doUsbAutoAllInOneAction( self, deviceIndex=0 ):
        global g_usbAutoDownloadResult_success
        global g_usbAutoDownloadResult_total
        if len(self.sbAppFiles) == 0:
            self.updateConnectStatus('red')
            if not self.isDymaticUsbDetection:
                self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadError_notValidImage'][self.languageIndex])
            return
        successes = 0
        g_usbAutoDownloadResult_total[deviceIndex] += 1
        if self._connectStateMachine(deviceIndex):
            for i in range(len(self.sbAppFiles)):
                if self.flashSbImage(self.sbAppFiles[i], deviceIndex):
                    if i == len(self.sbAppFiles) - 1:
                        successes = 1
                        g_usbAutoDownloadResult_success[deviceIndex] += 1
                        self.updateSlotStatus(deviceIndex, 'blue', g_usbAutoDownloadResult_success[deviceIndex], g_usbAutoDownloadResult_total[deviceIndex])
                    self.updateConnectStatus('blue')
                    if not self.isDymaticUsbDetection:
                        self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadInfo_success'][self.languageIndex])
                else:
                    self.updateConnectStatus('red')
                    self.updateSlotStatus(deviceIndex, 'red', g_usbAutoDownloadResult_success[deviceIndex], g_usbAutoDownloadResult_total[deviceIndex])
                    break
            if not self.isDymaticUsbDetection:
                self.resetMcuDevice(deviceIndex)
                time.sleep(2)
        else:
            self.updateSlotStatus(deviceIndex, 'red', g_usbAutoDownloadResult_success[deviceIndex], g_usbAutoDownloadResult_total[deviceIndex])
        self.connectStage[deviceIndex] = uidef.kConnectStage_Rom
        self._setUartUsbPort(deviceIndex)
        self.isUsbhidConnected[deviceIndex] = False
        if self.isDymaticUsbDetection:
            self.usbDevicePath[deviceIndex]['rom'] = None
            # Never clear 'flashloader' here, it will be used to help insert usb device
            #self.usbDevicePath[deviceIndex]['flashloader'] = None
        else:
            self.updateConnectStatus('black')
            self.setDownloadOperationResults(1, successes)
            self.initUsbDevicePath()
        # Back to set gray color for slot button
        time.sleep(0.5)
        self.updateSlotStatus(deviceIndex, 'gray', g_usbAutoDownloadResult_success[deviceIndex], g_usbAutoDownloadResult_total[deviceIndex])

    def callbackAllInOneAction( self, event ):
        if self.isUartPortSelected:
            self.isUartAllInOneActionTaskPending = True
            self._startGaugeTimer()
        elif self.isUsbhidPortSelected and (not self.isDymaticUsbDetection):
            self.isUsbAllInOneActionTaskPending[0] = True
            self._startGaugeTimer()
        else:
            pass

    def callbackChangedAppFile( self, event ):
        self.getUserAppFilePath()
        self.setCostTime(0)
        self.setDownloadOperationResults(0)
        self.updateConnectStatus('black')

    def callbackChangedAppFolder( self, event ):
        self.getUserAppFilePath()
        if os.path.isfile(self.sbAppFilePath):
            self.resetUserAppFolderPath()
            self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadError_clearImageFileFirst'][self.languageIndex])
        else:
            self.getUserAppFolderPath()
            self.setCostTime(0)
            self.setDownloadOperationResults(0)
            self.updateConnectStatus('black')

    def _stopTask( self, thread ):
        _async_raise(thread.ident, SystemExit)

    def _deinitToolToExit( self ):
        self._stopTask(g_task_detectUsbhid)
        self._stopTask(g_task_uartAllInOneAction)
        self._stopTask(g_task_usbAllInOneAction[0])
        self._stopTask(g_task_increaseGauge)
        global g_main_win
        g_main_win.Show(False)
        try:
            self.Destroy()
        except:
            pass
        self.closeDebugLog()

    def callbackExit( self, event ):
        self._deinitToolToExit()

    def callbackClose( self, event ):
        self._deinitToolToExit()

    def callbackSetUsbDetectionAsDynamic( self, event ):
        self.setUsbDetection()

    def callbackSetUsbDetectionAsStatic( self, event ):
        self.setUsbDetection()

    def callbackSetLanguageAsEnglish( self, event ):
        self.setLanguage()

    def callbackSetLanguageAsChinese( self, event ):
        self.setLanguage()

    def callbackShowHomePage( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['homePage_info'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['homePage_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

    def callbackShowAboutAuthor( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['aboutAuthor_author'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email2'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_blog'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['aboutAuthor_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

    def callbackShowRevisionHistory( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['revisionHistory_v1_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_1_0'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['revisionHistory_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()

    g_main_win = flashMain(None)
    g_main_win.SetTitle(u"NXP MCU Boot Flasher v3.0.0")
    g_main_win.Show()

    g_task_detectUsbhid = threading.Thread(target=g_main_win.task_doDetectUsbhid)
    g_task_detectUsbhid.setDaemon(True)
    g_task_detectUsbhid.start()
    g_task_uartAllInOneAction = threading.Thread(target=g_main_win.task_doUartAllInOneAction)
    g_task_uartAllInOneAction.setDaemon(True)
    g_task_uartAllInOneAction.start()
    g_task_usbAllInOneAction[0] = threading.Thread(target=g_main_win.task_doUsb0AllInOneAction)
    g_task_usbAllInOneAction[0].setDaemon(True)
    g_task_usbAllInOneAction[0].start()
    g_task_usbAllInOneAction[1] = threading.Thread(target=g_main_win.task_doUsb1AllInOneAction)
    g_task_usbAllInOneAction[1].setDaemon(True)
    g_task_usbAllInOneAction[1].start()
    g_task_usbAllInOneAction[2] = threading.Thread(target=g_main_win.task_doUsb2AllInOneAction)
    g_task_usbAllInOneAction[2].setDaemon(True)
    g_task_usbAllInOneAction[2].start()
    g_task_usbAllInOneAction[3] = threading.Thread(target=g_main_win.task_doUsb3AllInOneAction)
    g_task_usbAllInOneAction[3].setDaemon(True)
    g_task_usbAllInOneAction[3].start()
    g_task_usbAllInOneAction[4] = threading.Thread(target=g_main_win.task_doUsb4AllInOneAction)
    g_task_usbAllInOneAction[4].setDaemon(True)
    g_task_usbAllInOneAction[4].start()
    g_task_usbAllInOneAction[5] = threading.Thread(target=g_main_win.task_doUsb5AllInOneAction)
    g_task_usbAllInOneAction[5].setDaemon(True)
    g_task_usbAllInOneAction[5].start()
    g_task_usbAllInOneAction[6] = threading.Thread(target=g_main_win.task_doUsb6AllInOneAction)
    g_task_usbAllInOneAction[6].setDaemon(True)
    g_task_usbAllInOneAction[6].start()
    g_task_usbAllInOneAction[7] = threading.Thread(target=g_main_win.task_doUsb7AllInOneAction)
    g_task_usbAllInOneAction[7].setDaemon(True)
    g_task_usbAllInOneAction[7].start()
    g_task_increaseGauge = threading.Thread(target=g_main_win.task_doIncreaseGauge)
    g_task_increaseGauge.setDaemon(True)
    g_task_increaseGauge.start()

    app.MainLoop()
