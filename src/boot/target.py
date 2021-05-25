#! /usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os
import commands, memoryrange, peripherals
sys.path.append(os.path.abspath(".."))
from utils import misc

##
# Bootloader target definition.
class Target(object):

    def __init__(self, cpu, board='', build='', **kwargs):
                #baseDir='.', elfFile=None, memory={}, availableCommands=0,
                #availablePeripherals=0, deviceMemoryAccessable=False, systemDeviceId=0, isBootROM=False, isCrcCheckSupported=False):
        self.cpu = cpu
        self.board = board
        self.build = build

        self.baseDir = misc.get_dict_default(kwargs, 'baseDir', '.')
        self.memoryRange = misc.get_dict_default(kwargs, 'memoryRange', {})
        self.availableCommands = misc.get_dict_default(kwargs, 'availableCommands', 0)
        self.availablePeripherals = misc.get_dict_default(kwargs, 'availablePeripherals', 0)
        self.romUsbVid = misc.get_dict_default(kwargs, 'romUsbVid', None)
        self.romUsbPid = misc.get_dict_default(kwargs, 'romUsbPid', None)
        self.hasSdpReadRegisterCmd = misc.get_dict_default(kwargs, 'hasSdpReadRegisterCmd', None)
        self.flashloaderUsbVid = misc.get_dict_default(kwargs, 'flashloaderUsbVid', None)
        self.flashloaderUsbPid = misc.get_dict_default(kwargs, 'flashloaderUsbPid', None)
        self.flashloaderLoadAddr = misc.get_dict_default(kwargs, 'flashloaderLoadAddr', None)
        self.flashloaderJumpAddr = misc.get_dict_default(kwargs, 'flashloaderJumpAddr', None)
        self.supportedPeripheralSpeed_uart = misc.get_dict_default(kwargs, 'supportedPeripheralSpeed_uart', None)
        self.flexspiNorMemBase = misc.get_dict_default(kwargs, 'flexspiNorMemBase0', None)
        self.flexspiNorMemBase0 = misc.get_dict_default(kwargs, 'flexspiNorMemBase0', None)
        self.flexspiNorMemBase1 = misc.get_dict_default(kwargs, 'flexspiNorMemBase1', None)
        self.xspiNorCfgInfoOffset = misc.get_dict_default(kwargs, 'xspiNorCfgInfoOffset', None)
        self.isSipFlexspiNorDevice = misc.get_dict_default(kwargs, 'isSipFlexspiNorDevice', None)
        self.quadspiNorMemBase = misc.get_dict_default(kwargs, 'quadspiNorMemBase', None)
        self.registerAddrDict = misc.get_dict_default(kwargs, 'registerAddrDict', None)
        self.registerDefnDict = misc.get_dict_default(kwargs, 'registerDefnDict', None)
        self.ftfxNorMemBase = misc.get_dict_default(kwargs, 'ftfxNorMemBase', None)
        self.c040hdNorMemBase = misc.get_dict_default(kwargs, 'c040hdNorMemBase', None)

    ##
    # @brief Check if a command is supported by the target.
    #
    # @return True if the command is supported. False if not.
    def isCommandSupported(self, tag):
        return bool(commands.Commands[tag].propertyMask & self.availableCommands)

    ##
    # @brief Check if a peripheral is supported by the target.
    #
    # @return True if the peripheral is supported. False if not.
    def isPeripheralSupported(self, name):
        return bool(peripherals.PeripheralMasks[name].propertyMask & self.availablePeripherals)



