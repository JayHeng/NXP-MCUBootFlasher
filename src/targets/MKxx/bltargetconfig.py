#!/usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os
sys.path.append(os.path.abspath(".."))
from boot.memoryrange import MemoryRange

cpu = 'MKxx'
board = 'FRDM'
compiler = 'iar'
build = 'Release'

availablePeripherals = 0x17
romUsbVid = '0x15A2'
romUsbPid = '0x0073'
hasSdpReadRegisterCmd = None
flashloaderUsbVid = None
flashloaderUsbPid = None
flashloaderLoadAddr = None
flashloaderJumpAddr = None
availableCommands = 0x1ffff
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200] # @todo Verify
flexspiNorMemBase0 = None
flexspiNorMemBase1 = None
xspiNorCfgInfoOffset = None
isSipFlexspiNorDevice = None
quadspiNorMemBase = None
registerAddrDict = None
registerDefnDict  = None
ftfxNorMemBase = 0x00000000
c040hdNorMemBase = None

# memory map
memoryRange = {
    # SRAM, 1MByte
    'sram' : MemoryRange(0x1fff0000, 0x100000, 'state_mem0.dat'),

    # FLASH, 4KByte / 2MByte
    'flash': MemoryRange(0x00000000, 0x200000, 'state_flash_mem.dat', True, 4096, 4, 4, 16)
}

reservedRegionDict = {
    # SRAM
    'sram' : [0x1fff0000, 0x1fff1d90]
}
