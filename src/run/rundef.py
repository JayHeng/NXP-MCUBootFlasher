import sys, os

kUartSpeed_Blhost = ['115200', '57600', '19200', '9600', '4800']
kUartSpeed_Sdphost = ['115200']

kRegisterAddr_SRC_SBMR2  = 0x400F801C
kRegisterMask_SecConfig  = 0x00000003
kRegisterShift_SecConfig = 0

kHabStatus_FAB     = 0x0
kHabStatus_Open    = 0x1
kHabStatus_Closed0 = 0x2
kHabStatus_Closed1 = 0x3

