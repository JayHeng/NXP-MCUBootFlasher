
# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os

kUartSpeed_Blhost = ['115200', '57600', '19200', '9600', '4800']
kUartSpeed_Sdphost = ['115200']

registerAddrDict_RT10yy = {
                           'kRegisterAddr_SRC_SBMR2'  :0x400F801C,
                            }

registerDefnDict_RT10yy = {
                           'kRegisterMask_SRC_SBMR2_SecConfig'  :0x00000003,
                           'kRegisterShift_SRC_SBMR2_SecConfig' :0,
                            }

registerAddrDict_RT11yy = {
                           'kRegisterAddr_SRC_SBMR2'  :0x40C0400C,
                            }

registerDefnDict_RT11yy = {
                           'kRegisterMask_SRC_SBMR2_SecConfig'  :0x00000003,
                           'kRegisterShift_SRC_SBMR2_SecConfig' :0,
                            }

kHabStatus_FAB     = 0x0
kHabStatus_Open    = 0x1
kHabStatus_Closed0 = 0x2
kHabStatus_Closed1 = 0x3

