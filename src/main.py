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
g_task_increaseGauge = None

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

    def _setUartUsbPort( self ):
        usbIdList = self.getUsbid()
        retryToDetectUsb = False
        self.setPortSetupValue(self.connectStage, usbIdList, retryToDetectUsb )

    def callbackSetUartPort( self, event ):
        self._setUartUsbPort()

    def callbackSetUsbhidPort( self, event ):
        self._setUartUsbPort()

    def callbackSetPortVid( self, event ):
        self.updatePortSetupValue()

    def callbackSetBaudPid( self, event ):
        self.updatePortSetupValue()

    def _retryToPingBootloader( self, bootType ):
        pingStatus = False
        pingCnt = kRetryPingTimes
        while (not pingStatus) and pingCnt > 0:
            if bootType == kBootloaderType_Rom:
                pingStatus = self.pingRom()
            elif bootType == kBootloaderType_Flashloader:
                # This is mainly for RT1170 flashloader, but it is also ok for other RT devices
                if self.isUartPortSelected:
                    time.sleep(3)
                pingStatus = self.pingFlashloader()
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

    def _connectFailureHandler( self ):
        self.connectStage = uidef.kConnectStage_Rom
        self.updateConnectStatus('red')
        usbIdList = self.getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList, False )
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
            if not self.updatePortSetupValue(retryToDetectUsb):
                self._connectFailureHandler()
                if not isConnectionFailureOnce:
                    isConnectionFailureOnce = True
                    continue
                else:
                    return False
            if self.connectStage == uidef.kConnectStage_Rom:
                self.connectToDevice(self.connectStage, deviceIndex)
                if self._retryToPingBootloader(kBootloaderType_Rom):
                    if (self.mcuSeries == uidef.kMcuSeries_iMXRT10yy) or \
                       (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy):
                        self.getMcuDeviceHabStatus()
                        if self.jumpToFlashloader():
                            self.connectStage = uidef.kConnectStage_Flashloader
                            usbIdList = self.getUsbid()
                            self.setPortSetupValue(self.connectStage, usbIdList, True )
                        else:
                            self.updateConnectStatus('red')
                            self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_failToJumpToFl'][self.languageIndex])
                            return False
                    elif (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx) or \
                         (self.mcuSeries == uidef.kMcuSeries_LPC) or \
                         (self.mcuSeries == uidef.kMcuSeries_Kinetis):
                        self.updateConnectStatus('green')
                        self.connectStage = uidef.kConnectStage_Ready
                    else:
                        pass
                else:
                    self.updateConnectStatus('red')
                    self._doubleCheckBootModeError()
                    return False
            elif self.connectStage == uidef.kConnectStage_Flashloader:
                self.connectToDevice(self.connectStage, deviceIndex)
                if self._retryToPingBootloader(kBootloaderType_Flashloader):
                    self.updateConnectStatus('green')
                    self.connectStage = uidef.kConnectStage_Ready
                else:
                    self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_failToPingFl'][self.languageIndex])
                    self._connectFailureHandler()
                    return False
            elif self.connectStage == uidef.kConnectStage_Ready:
                if connectSteps == 1:
                    self.setInfoStatus(uilang.kMsgLanguageContentDict['connectInfo_readyForDownload'][self.languageIndex])
                    return True
                else:
                    if self._retryToPingBootloader(kBootloaderType_Flashloader):
                        self.setInfoStatus(uilang.kMsgLanguageContentDict['connectInfo_readyForDownload'][self.languageIndex])
                        return True
                    else:
                        self.connectStage = uidef.kConnectStage_Rom
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
                    if self.flashSbImage(self.sbAppFiles[i]):
                        if i == len(self.sbAppFiles) - 1:
                            successes += 1
                        self.updateConnectStatus('blue')
                        self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadInfo_success'][self.languageIndex])
                    else:
                        self.updateConnectStatus('red')
                        break
                self.resetMcuDevice()
            self.connectStage = uidef.kConnectStage_Rom
            self._setUartUsbPort()
            self.setDownloadOperationResults(operations, successes)

    def callbackAllInOneAction( self, event ):
        if self.isUartPortSelected:
            self.isUartAllInOneActionTaskPending = True
            self._startGaugeTimer()

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
        self._stopTask(g_task_increaseGauge)
        global g_main_win
        g_main_win.Show(False)
        try:
            self.Destroy()
        except:
            pass

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
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_0_0'][self.languageIndex]))
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
    g_task_increaseGauge = threading.Thread(target=g_main_win.task_doIncreaseGauge)
    g_task_increaseGauge.setDaemon(True)
    g_task_increaseGauge.start()

    app.MainLoop()
