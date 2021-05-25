#!/usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os
sys.path.append(os.path.abspath(".."))
from boot.memoryrange import MemoryRange

cpu = 'MIMXRT685'
board = 'EVK'
compiler = 'iar'
build = 'Release'

availablePeripherals = 0x11
romUsbVid = '0x1FC9'
romUsbPid = '0x0020'
hasSdpReadRegisterCmd = None
flashloaderUsbVid = None
flashloaderUsbPid = None
flashloaderLoadAddr = None
flashloaderJumpAddr = None
availableCommands = 0x5EFDF
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200] # @todo Verify
flexspiNorMemBase0 = 0x08000000
flexspiNorMemBase1 = None
xspiNorCfgInfoOffset = 0x400
isSipFlexspiNorDevice = False
quadspiNorMemBase = None
registerAddrDict = None
registerDefnDict  = None
ftfxNorMemBase = None
c040hdNorMemBase = None

# memory map
memoryRange = {
    # SRAM, 3MByte
    'sram' : MemoryRange(0x00000000, 0x480000, 'state_mem0.dat'),

    # FLASH, 64KByte / 512MByte
    'flash': MemoryRange(0x00000000, 0x20000000, 'state_flash_mem.dat', True, 0x10000)
}

reservedRegionDict = {
    # SRAM, 512KB
    'sram' : [0x20203800, 0x20207EF8]
}
