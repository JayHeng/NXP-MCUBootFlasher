#!/usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os
sys.path.append(os.path.abspath(".."))
from boot.memoryrange import MemoryRange
from run import rundef

cpu = 'MIMXRT1166'
board = 'EVK'
compiler = 'iar'
build = 'Release'

availablePeripherals = 0x11
romUsbVid = '0x1FC9'
romUsbPid = '0x013D'
hasSdpReadRegisterCmd = None
flashloaderUsbVid = '0x15A2'
flashloaderUsbPid = '0x0073'
flashloaderLoadAddr = None
flashloaderJumpAddr = None
availableCommands = 0x5EFDF
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200] # @todo Verify
flexspiNorMemBase0 = 0x30000000
flexspiNorMemBase1 = 0x60000000
xspiNorCfgInfoOffset = 0x400
isSipFlexspiNorDevice = False
quadspiNorMemBase = None
registerAddrDict = rundef.registerAddrDict_RT11yy
registerDefnDict  = rundef.registerDefnDict_RT11yy
ftfxNorMemBase = None
c040hdNorMemBase = None

# memory map
memoryRange = {
    # ITCM_CM7, 512KByte
    'itcm' : MemoryRange(0x00000000, 0x80000, 'state_mem0.dat'),
    # ITCM_CM4, 128KByte
    'itcm_cm4' : MemoryRange(0x1FFE0000, 0x20000, 'state_mem0.dat'),
    # DTCM, 512KByte
    'dtcm' : MemoryRange(0x20000000, 0x80000, 'state_mem1.dat'),
    # OCRAM, 1MByte
    'ocram' : MemoryRange(0x20200000, 0x100000, 'state_mem2.dat'),

    # FLASH, 64KByte / 512MByte
    'flash': MemoryRange(0x00000000, 0x20000000, 'state_flash_mem.dat', True, 0x10000)
}

reservedRegionDict = {   # new
    # OCRAM, 2MB
    'ram' : [0x20203800, 0x20207F58]
}

