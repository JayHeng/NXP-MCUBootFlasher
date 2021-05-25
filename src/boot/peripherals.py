#! /usr/bin/env python

# Copyright 2021 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

from collections import namedtuple

##
# @brief Supported bootloader peripherals.
kPeripheral_UART = 'uart'
kPeripheral_USB  = 'usb'

##
# @brief Supported SDP peripherals.
kPeripheral_SDP_UART = 'sdp_uart'
kPeripheral_SDP_USB = 'sdp_usb'

Peripherals = [kPeripheral_UART, kPeripheral_USB]
PeripheralsSDP = [kPeripheral_SDP_UART, kPeripheral_SDP_USB]

PeripheralMask = namedtuple('PeripheralMask', 'name, propertyMask')

PeripheralMasks = {
    kPeripheral_UART        : PeripheralMask(kPeripheral_UART,        0x01),
    kPeripheral_USB         : PeripheralMask(kPeripheral_USB,         0x10)
}

