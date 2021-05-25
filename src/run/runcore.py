#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys
import os
import array
import math
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from ui import uicore
from ui import uidef
from ui import uilang
from boot import bltest
from boot import target

def createTarget(device, exeBinRoot):
    cpu = "MIMXRT1052"
    if device == uidef.kMcuDevice_iMXRT500:
        cpu = "MIMXRT595"
    elif device == uidef.kMcuDevice_iMXRT600:
        cpu = "MIMXRT685"
    elif device == uidef.kMcuDevice_iMXRT1011:
        cpu = "MIMXRT1011"
    elif device == uidef.kMcuDevice_iMXRT1015:
        cpu = "MIMXRT1015"
    elif device == uidef.kMcuDevice_iMXRT102x:
        cpu = "MIMXRT1021"
    elif device == uidef.kMcuDevice_iMXRT1024:
        cpu = "MIMXRT1024"
    elif device == uidef.kMcuDevice_iMXRT105x:
        cpu = "MIMXRT1052"
    elif device == uidef.kMcuDevice_iMXRT106x:
        cpu = "MIMXRT1062"
    elif device == uidef.kMcuDevice_iMXRT1064:
        cpu = "MIMXRT1064"
    elif device == uidef.kMcuDevice_iMXRT116x:
        cpu = "MIMXRT1166"
    elif device == uidef.kMcuDevice_iMXRT117x:
        cpu = "MIMXRT1176"
    elif device in uidef.kMcuDevice_Niobe4minis:
        cpu = "LPC55S16"
    elif device in uidef.kMcuDevice_Niobe4s:
        cpu = "LPC55S69"
    elif device in uidef.kMcuDevice_Kinetis:
        cpu = "MKxx"
    else:
        pass
    targetBaseDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'targets', cpu)

    # Check for existing target directory.
    if not os.path.isdir(targetBaseDir):
        targetBaseDir = os.path.join(os.path.dirname(exeBinRoot), 'src', 'targets', cpu)
        if not os.path.isdir(targetBaseDir):
            raise ValueError("Missing target directory at path %s" % targetBaseDir)

    targetConfigFile = os.path.join(targetBaseDir, 'bltargetconfig.py')

    # Check for config file existence.
    if not os.path.isfile(targetConfigFile):
        raise RuntimeError("Missing target config file at path %s" % targetConfigFile)

    # Build locals dict by copying our locals and adjusting file path and name.
    targetConfig = locals().copy()
    targetConfig['__file__'] = targetConfigFile
    targetConfig['__name__'] = 'bltargetconfig'

    # Execute the target config script.
    execfile(targetConfigFile, globals(), targetConfig)

    # Create the target object.
    tgt = target.Target(**targetConfig)

    return tgt, targetBaseDir

##
# @brief
class flashRun(uicore.flashUi):

    def __init__(self, parent):
        uicore.flashUi.__init__(self, parent)
        self.blhost = [None] * uidef.kMaxMfgBoards
        self.sdphost = [None] * uidef.kMaxMfgBoards
        self.tgt = None
        self.cpuDir = None
        self.sdphostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'sdphost', 'win', 'vectors')
        self.blhostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'blhost2_3', 'win', 'vectors')
        self.mcuDeviceHabStatus = [None] * uidef.kMaxMfgBoards
        self.createMcuTarget()

    def createMcuTarget( self ):
        self.tgt, self.cpuDir = createTarget(self.mcuDevice, self.exeBinRoot)

    def getUsbid( self ):
        self.createMcuTarget()
        return [self.tgt.romUsbVid, self.tgt.romUsbPid, self.tgt.flashloaderUsbVid, self.tgt.flashloaderUsbPid]

    def connectToDevice( self , connectStage, deviceIndex=0 ):
        if connectStage == uidef.kConnectStage_Rom:
            # Create the target object.
            self.createMcuTarget()
            xhost = None
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                xhost = 'sdp_'
            elif (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy) or \
                 (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx) or \
                 (self.mcuSeries == uidef.kMcuSeries_LPC) or \
                 (self.mcuSeries == uidef.kMcuSeries_Kinetis):
                xhost = ''
            else:
                pass
            xPeripheral = None
            if self.isUartPortSelected:
                xPeripheral = xhost + 'uart'
                uartComPort = self.uartComPort[deviceIndex]
                uartBaudrate = int(self.uartBaudrate[deviceIndex])
                usbVid = None
                usbPid = None
                usbDevicePath = None
            elif self.isUsbhidPortSelected:
                xPeripheral = xhost + 'usb'
                uartComPort = ''
                uartBaudrate = ''
                if self.isDymaticUsbDetection:
                    usbVid = None
                    usbPid = None
                    usbDevicePath = self.usbDevicePath[deviceIndex]['rom']
                else:
                    usbVid = self.tgt.romUsbVid
                    usbPid = self.tgt.romUsbPid
                    usbDevicePath = None
            else:
                pass
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                self.sdphost[deviceIndex] = bltest.createBootloader(self.tgt,
                                                       self.sdphostVectorsDir,
                                                       xPeripheral,
                                                       uartBaudrate, uartComPort,
                                                       usbVid, usbPid, usbDevicePath)
            elif (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy) or \
                 (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx) or \
                 (self.mcuSeries == uidef.kMcuSeries_LPC) or \
                 (self.mcuSeries == uidef.kMcuSeries_Kinetis):
                self.blhost[deviceIndex] = bltest.createBootloader(self.tgt,
                                                      self.blhostVectorsDir,
                                                      xPeripheral,
                                                      uartBaudrate, uartComPort,
                                                      usbVid, usbPid, usbDevicePath,
                                                      True)
            else:
                pass
        elif connectStage == uidef.kConnectStage_Flashloader:
            if self.isUartPortSelected:
                blPeripheral = 'uart'
                uartComPort = self.uartComPort[deviceIndex]
                uartBaudrate = int(self.uartBaudrate[deviceIndex])
                usbVid = None
                usbPid = None
                usbDevicePath = None
            elif self.isUsbhidPortSelected:
                blPeripheral = 'usb'
                uartComPort = ''
                uartBaudrate = ''
                if self.isDymaticUsbDetection:
                    usbVid = None
                    usbPid = None
                    usbDevicePath = self.usbDevicePath[deviceIndex]['flashloader']
                else:
                    usbVid = self.tgt.flashloaderUsbVid
                    usbPid = self.tgt.flashloaderUsbPid
                    usbDevicePath = None
            else:
                pass
            self.blhost[deviceIndex] = bltest.createBootloader(self.tgt,
                                                  self.blhostVectorsDir,
                                                  blPeripheral,
                                                  uartBaudrate, uartComPort,
                                                  usbVid, usbPid, usbDevicePath,
                                                  True)
        elif connectStage == uidef.kConnectStage_Reset:
            #self.tgt = None
            pass
        else:
            pass

    def pingRom( self, deviceIndex=0  ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            status, results, cmdStr = self.sdphost[deviceIndex].errorStatus()
            return (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled)
        elif (self.mcuSeries == uidef.kMcuSeries_iMXRT11yy) or \
             (self.mcuSeries == uidef.kMcuSeries_iMXRTxxx) or \
             (self.mcuSeries == uidef.kMcuSeries_LPC) or \
             (self.mcuSeries == uidef.kMcuSeries_Kinetis):
            status, results, cmdStr = self.blhost[deviceIndex].getProperty(boot.properties.kPropertyTag_CurrentVersion)
            return (status == boot.status.kStatus_Success)
        else:
            pass

    def _getVal32FromBinFile( self, filename, offset=0):
        var32Vaule = 0
        if os.path.isfile(filename):
            var32Vaule = array.array('c', [chr(0xff)]) * 4
            with open(filename, 'rb') as fileObj:
                fileObj.seek(offset)
                var32Vaule = fileObj.read(4)
                fileObj.close()
            var32Vaule = (ord(var32Vaule[3])<<24) + (ord(var32Vaule[2])<<16) + (ord(var32Vaule[1])<<8) + ord(var32Vaule[0])
        return var32Vaule

    def _getDeviceRegisterBySdphost( self, regAddr, deviceIndex=0 ):
        if self.tgt.hasSdpReadRegisterCmd:
            filename = 'readReg.dat'
            filepath = os.path.join(self.sdphostVectorsDir, filename)
            status, results, cmdStr = self.sdphost[deviceIndex].readRegister(regAddr, 32, 4, filename)
            if (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled):
                regVal = self._getVal32FromBinFile(filepath)
                return regVal
            else:
                return None
            try:
                os.remove(filepath)
            except:
                pass

    def getMcuDeviceHabStatus( self, deviceIndex=0 ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            if self.tgt.hasSdpReadRegisterCmd:
                secConfig = self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_SRC_SBMR2'], deviceIndex)
                if secConfig != None:
                    self.mcuDeviceHabStatus[deviceIndex] = ((secConfig & self.tgt.registerDefnDict['kRegisterMask_SRC_SBMR2_SecConfig']) >> self.tgt.registerDefnDict['kRegisterShift_SRC_SBMR2_SecConfig'])
                    if self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_FAB:
                        self.setHabStatus(u"FAB")
                    elif self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_Open:
                        self.setHabStatus(u"Open")
                    elif self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_Closed0 or self.mcuDeviceHabStatus == rundef.kHabStatus_Closed1:
                        self.setHabStatus(u"Closed")
                    else:
                        pass
            else:
                status, results, cmdStr = self.sdphost[deviceIndex].errorStatus()
                if status == boot.status.kSDP_Status_HabEnabled:
                    self.mcuDeviceHabStatus[deviceIndex] = rundef.kHabStatus_Closed0
                    self.setHabStatus(u"Closed")
                elif status == boot.status.kSDP_Status_HabDisabled:
                    self.mcuDeviceHabStatus[deviceIndex] = rundef.kHabStatus_Open
                    self.setHabStatus(u"Open")
                else:
                    pass
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            status, results, cmdStr = self.blhost[deviceIndex].getProperty(boot.properties.kPropertyTag_FlashSecurityState)
            if status == boot.status.kStatus_Success:
                if results[0] == 0:
                    self.mcuDeviceHabStatus[deviceIndex] = rundef.kHabStatus_Open
                    self.setHabStatus(u"Open")
                else:
                    self.mcuDeviceHabStatus[deviceIndex] = rundef.kHabStatus_Closed0
                    self.setHabStatus(u"Closed")
            else:
                pass
        else:
            pass

    def jumpToFlashloader( self, deviceIndex=0 ):
        flashloaderBinFile = None
        if self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_Closed0 or self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_Closed1:
            flashloaderBinFile = os.path.join(self.cpuDir, 'ivt_flashloader_signed.bin')
            if not os.path.isfile(flashloaderBinFile):
                self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_notValidSignedFl'][self.languageIndex])
                return False
        elif self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_FAB or self.mcuDeviceHabStatus[deviceIndex] == rundef.kHabStatus_Open:
            flashloaderBinFile = os.path.join(self.cpuDir, 'ivt_flashloader.bin')
        else:
            pass
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            status, results, cmdStr = self.sdphost[deviceIndex].writeFile(self.tgt.flashloaderLoadAddr, flashloaderBinFile)
            if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
                return False
            status, results, cmdStr = self.sdphost[deviceIndex].jumpAddress(self.tgt.flashloaderJumpAddr)
            if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
                return False
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            status, results, cmdStr = self.blhost[deviceIndex].loadImage(flashloaderBinFile)
            if status != boot.status.kStatus_Success:
                return False
        else:
            pass
        return True

    def pingFlashloader( self, deviceIndex=0 ):
        status, results, cmdStr = self.blhost[deviceIndex].getProperty(boot.properties.kPropertyTag_CurrentVersion)
        return (status == boot.status.kStatus_Success)

    def flashSbImage( self, sbAppFile, deviceIndex=0  ):
        status, results, cmdStr = self.blhost[deviceIndex].receiveSbFile(sbAppFile)
        if (status == boot.status.kStatus_Success) or (status == boot.status.kStatus_AbortDataPhase):
            return True
        else:
            self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadError_failToDownload'][self.languageIndex])
            return False

    def resetMcuDevice( self, deviceIndex=0 ):
        status, results, cmdStr = self.blhost[deviceIndex].reset()
        return (status == boot.status.kStatus_Success)
