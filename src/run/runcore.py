#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
    # Build path to target directory and config file.
    if device == uidef.kMcuDevice_iMXRT1015:
        cpu = "MIMXRT1015"
    elif device == uidef.kMcuDevice_iMXRT102x:
        cpu = "MIMXRT1021"
    elif device == uidef.kMcuDevice_iMXRT105x:
        cpu = "MIMXRT1052"
    elif device == uidef.kMcuDevice_iMXRT106x:
        cpu = "MIMXRT1062"
    elif device == uidef.kMcuDevice_iMXRT1064:
        cpu = "MIMXRT1064"
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
        self.blhost = None
        self.sdphost = None
        self.tgt = None
        self.cpuDir = None
        self.sdphostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'sdphost', 'win', 'vectors')
        self.blhostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'blhost', 'win', 'vectors')
        self.mcuDeviceHabStatus = None
        self.createMcuTarget()

    def createMcuTarget( self ):
        self.tgt, self.cpuDir = createTarget(self.mcuDevice, self.exeBinRoot)

    def getUsbid( self ):
        self.createMcuTarget()
        return [self.tgt.romUsbVid, self.tgt.romUsbPid, self.tgt.flashloaderUsbVid, self.tgt.flashloaderUsbPid]

    def connectToDevice( self , connectStage):
        if connectStage == uidef.kConnectStage_Rom:
            # Create the target object.
            self.createMcuTarget()
            if self.isUartPortSelected:
                sdpPeripheral = 'sdp_uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
                usbVid = ''
                usbPid = ''
            elif self.isUsbhidPortSelected:
                sdpPeripheral = 'sdp_usb'
                uartComPort = ''
                uartBaudrate = ''
                usbVid = self.tgt.romUsbVid
                usbPid = self.tgt.romUsbPid
            else:
                pass
            self.sdphost = bltest.createBootloader(self.tgt,
                                                   self.sdphostVectorsDir,
                                                   sdpPeripheral,
                                                   uartBaudrate, uartComPort,
                                                   usbVid, usbPid)
        elif connectStage == uidef.kConnectStage_Flashloader:
            if self.isUartPortSelected:
                blPeripheral = 'uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
                usbVid = ''
                usbPid = ''
            elif self.isUsbhidPortSelected:
                blPeripheral = 'usb'
                uartComPort = ''
                uartBaudrate = ''
                usbVid = self.tgt.flashloaderUsbVid
                usbPid = self.tgt.flashloaderUsbPid
            else:
                pass
            self.blhost = bltest.createBootloader(self.tgt,
                                                  self.blhostVectorsDir,
                                                  blPeripheral,
                                                  uartBaudrate, uartComPort,
                                                  usbVid, usbPid,
                                                  True)
        elif connectStage == uidef.kConnectStage_Reset:
            self.tgt = None
        else:
            pass

    def pingRom( self ):
        status, results, cmdStr = self.sdphost.errorStatus()
        return (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled)

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

    def _getDeviceRegisterBySdphost( self, regAddr):
        filename = 'readReg.dat'
        filepath = os.path.join(self.sdphostVectorsDir, filename)
        status, results, cmdStr = self.sdphost.readRegister(regAddr, 32, 4, filename)
        if (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled):
            regVal = self._getVal32FromBinFile(filepath)
            return regVal
        else:
            return None
        try:
            os.remove(filepath)
        except:
            pass

    def getMcuDeviceHabStatus( self ):
        secConfig = self._getDeviceRegisterBySdphost( rundef.kRegisterAddr_SRC_SBMR2)
        if secConfig != None:
            self.mcuDeviceHabStatus = ((secConfig & rundef.kRegisterMask_SecConfig) >> rundef.kRegisterShift_SecConfig)
            if self.mcuDeviceHabStatus == rundef.kHabStatus_FAB:
                self.setHabStatus(u"FAB")
            elif self.mcuDeviceHabStatus == rundef.kHabStatus_Open:
                self.setHabStatus(u"Open")
            elif self.mcuDeviceHabStatus == rundef.kHabStatus_Closed0 or self.mcuDeviceHabStatus == rundef.kHabStatus_Closed1:
                self.setHabStatus(u"Closed")
            else:
                pass

    def jumpToFlashloader( self ):
        flashloaderBinFile = None
        if self.mcuDeviceHabStatus == rundef.kHabStatus_Closed0 or self.mcuDeviceHabStatus == rundef.kHabStatus_Closed1:
            flashloaderBinFile = os.path.join(self.cpuDir, 'ivt_flashloader_signed.bin')
            if not os.path.isfile(flashloaderBinFile):
                self.setInfoStatus(uilang.kMsgLanguageContentDict['connectError_notValidSignedFl'][self.languageIndex])
                return False
        elif self.mcuDeviceHabStatus == rundef.kHabStatus_FAB or self.mcuDeviceHabStatus == rundef.kHabStatus_Open:
            flashloaderBinFile = os.path.join(self.cpuDir, 'ivt_flashloader.bin')
        else:
            pass
        status, results, cmdStr = self.sdphost.writeFile(self.tgt.flashloaderLoadAddr, flashloaderBinFile)
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return False
        status, results, cmdStr = self.sdphost.jumpAddress(self.tgt.flashloaderJumpAddr)
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return False
        return True

    def pingFlashloader( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        return (status == boot.status.kStatus_Success)

    def flashSbImage( self ):
        status, results, cmdStr = self.blhost.receiveSbFile(self.sbAppPath)
        if (status == boot.status.kStatus_Success) or (status == boot.status.kStatus_AbortDataPhase):
            return True
        else:
            self.setInfoStatus(uilang.kMsgLanguageContentDict['downloadError_failToDownload'][self.languageIndex])
            return False

    def resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        return (status == boot.status.kStatus_Success)
