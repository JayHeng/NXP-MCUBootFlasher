#!/usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os
sys.path.append(os.path.abspath(".."))
from boot.memoryrange import MemoryRange
from run import rundef

cpu = 'MIMXRT1011'
board = 'EVK'
compiler = 'iar'
build = 'Release'

availablePeripherals = 0x11
romUsbVid = '0x1FC9'
romUsbPid = '0x0145'
hasSdpReadRegisterCmd = False
flashloaderUsbVid = '0x15A2'
flashloaderUsbPid = '0x0073'
flashloaderLoadAddr = 0x20205800
flashloaderJumpAddr = 0x20205800
availableCommands = 0x5EFDF
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200] # @todo Verify
flexspiNorMemBase0 = 0x60000000
flexspiNorMemBase1 = None
xspiNorCfgInfoOffset = 0x400
isSipFlexspiNorDevice = False
quadspiNorMemBase = None
registerAddrDict = rundef.registerAddrDict_RT10yy
registerDefnDict  = rundef.registerDefnDict_RT10yy
ftfxNorMemBase = None
c040hdNorMemBase = None

# memory map
memoryRange = {
    # ITCM, 128KByte
    'itcm' : MemoryRange(0x00000000, 0x20000, 'state_mem0.dat'),
    # DTCM, 128KByte
    'dtcm' : MemoryRange(0x20000000, 0x20000, 'state_mem1.dat'),
    # OCRAM, 128KByte
    'ocram' : MemoryRange(0x20200000, 0x20000, 'state_mem2.dat'),

    # FLASH, 64KByte / 512MByte
    'flash': MemoryRange(0x00000000, 0x20000000, 'state_flash_mem.dat', True, 0x10000)
}

reservedRegionDict = {   # new
    # OCRAM, 22KB
    'ram' : [0x20200000, 0x202057FF]
}

