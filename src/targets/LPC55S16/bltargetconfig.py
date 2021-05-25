#!/usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os
sys.path.append(os.path.abspath(".."))
from boot.memoryrange import MemoryRange

cpu = 'LPC55S16'
board = 'LPCXpresso'
compiler = 'iar'
build = 'Release'

availablePeripherals = 0x17
romUsbVid = '0x1FC9'
romUsbPid = '0x0021'
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
ftfxNorMemBase = None
c040hdNorMemBase = 0x00000000

# memory map
memoryRange = {
    # SRAMX, 32KByte
    'sramx' : MemoryRange(0x04000000, 0x8000, 'state_mem0.dat'),
    # SRAM0/1/2, 64KByte
    'sram'  : MemoryRange(0x20000000, 0x10000, 'state_mem1.dat'),

    # FLASH, 4KByte / 256KByte
    'flash': MemoryRange(0x00000000, 0x40000, 'state_flash_mem.dat', True, 4096, 4, 4, 16)
}

reservedRegionDict = {
    # SRAM
    'sram' : [0x20000000, 0x20000000]
}
