
# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import wx
import sys, os

kMaxMfgBoards = 8

kConnectStage_Rom            = 1
kConnectStage_Flashloader    = 2
kConnectStage_Ready          = 3

kMcuSeries_iMXRT10yy = 'RT10yy'
kMcuSeries_iMXRT11yy = 'RT11yy'

kMcuSeries_iMXRTyyyy = [kMcuSeries_iMXRT10yy, kMcuSeries_iMXRT11yy]
kMcuSeries_iMXRTxxx  = 'RTxxx'
kMcuSeries_LPC       = 'LPC'
kMcuSeries_Kinetis   = 'Kinetis'

kMcuDevice_iMXRT500  = 'i.MXRT5xx'
kMcuDevice_iMXRT500S = 'i.MXRT5xxS'
kMcuDevice_iMXRT600  = 'i.MXRT6xx'
kMcuDevice_iMXRT600S = 'i.MXRT6xxS'
kMcuDevice_iMXRTxxx = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT600]

kMcuDevice_iMXRT1011 = 'i.MXRT1011'
kMcuDevice_iMXRT1015 = 'i.MXRT1015'
kMcuDevice_iMXRT102x = 'i.MXRT1021'
kMcuDevice_iMXRT1024 = 'i.MXRT1024 SIP'
kMcuDevice_iMXRT105x = 'i.MXRT105x'
kMcuDevice_iMXRT106x = 'i.MXRT106x'
kMcuDevice_iMXRT1064 = 'i.MXRT1064 SIP'
kMcuDevice_iMXRT10yy = [kMcuDevice_iMXRT1011, kMcuDevice_iMXRT1015, kMcuDevice_iMXRT102x, kMcuDevice_iMXRT1024, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064]

kMcuDevice_iMXRT116x = 'i.MXRT116x'
kMcuDevice_iMXRT117x = 'i.MXRT117x'
kMcuDevice_iMXRT11yy = [kMcuDevice_iMXRT116x, kMcuDevice_iMXRT117x]

kMcuDevice_L0PB      = 'MKL03Z'
kMcuDevice_L3KS_0    = 'MKL13Z'
kMcuDevice_L2KS_0    = 'MKL27Z'
kMcuDevice_L5K       = 'MKL28Z'
kMcuDevice_L3KS_1    = 'MKL33Z'
kMcuDevice_L4KS_0    = 'MKL43Z'
kMcuDevice_MKL80     = 'MKL8xZ'
kMcuDevice_MT256P    = 'MKE16Z'
kMcuDevice_MT512P    = 'MKE18F'
kMcuDevice_MK28F_0   = 'MK27F'
kMcuDevice_MK28F_1   = 'MK28F'
kMcuDevice_MK80      = 'MK8xF'
kMcuDevice_L2KS_1    = 'K32L2'
kMcuDevice_L4KS_1    = 'K32L3'

kMcuDevice_L3KSs     = [kMcuDevice_L3KS_0, kMcuDevice_L3KS_1]
kMcuDevice_MK28Fs    = [kMcuDevice_MK28F_0, kMcuDevice_MK28F_1]
kMcuDevice_Kinetis   = [kMcuDevice_L0PB, kMcuDevice_L3KS_0, kMcuDevice_L3KS_1, kMcuDevice_L2KS_0, kMcuDevice_L5K, kMcuDevice_L4KS_0, kMcuDevice_MKL80, kMcuDevice_MT256P, kMcuDevice_MT512P, kMcuDevice_MK28F_0, kMcuDevice_MK28F_1, kMcuDevice_MK80, kMcuDevice_L2KS_1, kMcuDevice_L4KS_1]

kMcuDevice_Niobe4mini_0 = 'LPC55(S)0x'
kMcuDevice_Niobe4mini_1 = 'LPC55(S)1x'
kMcuDevice_Niobe4_0     = 'LPC55(S)2x'
kMcuDevice_Niobe4_1     = 'LPC55S6x'

kMcuDevice_Niobe4minis = [kMcuDevice_Niobe4mini_0, kMcuDevice_Niobe4mini_1]
kMcuDevice_Niobe4s     = [kMcuDevice_Niobe4_0, kMcuDevice_Niobe4_1]
kMcuDevice_LPC         = [kMcuDevice_Niobe4mini_0, kMcuDevice_Niobe4mini_1, kMcuDevice_Niobe4_0, kMcuDevice_Niobe4_1]

kMcuDevice_Latest     = kMcuDevice_iMXRTxxx + kMcuDevice_iMXRT10yy + kMcuDevice_iMXRT11yy + kMcuDevice_LPC + kMcuDevice_Kinetis
