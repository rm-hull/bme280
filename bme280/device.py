#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2016 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import smbus

import reader
import const as compensation


def load_calibration_params(bus, address):
    """
    The BME280 output consists of the ADC output values. However, each sensing
    element behaves differently. Therefore, the actual pressure and temperature
    must be calculated using a set of calibration parameters.

    The calibration parameters are subsequently used to with some compensation
    formula to perform temperature readout in degC, humidity in % and pressure
    in hPA.
    """
    read = reader.reader(bus, address)

    # Temperature trimming params
    compensation.dig_T1 = read.unsigned_short(0x88)
    compensation.dig_T2 = read.signed_short(0x8A)
    compensation.dig_T3 = read.signed_short(0x8C)

    # Pressure trimming params
    compensation.dig_P1 = read.unsigned_short(0x8E)
    compensation.dig_P2 = read.signed_short(0x90)
    compensation.dig_P3 = read.signed_short(0x92)
    compensation.dig_P4 = read.signed_short(0x94)
    compensation.dig_P5 = read.signed_short(0x96)
    compensation.dig_P6 = read.signed_short(0x98)
    compensation.dig_P7 = read.signed_short(0x9A)
    compensation.dig_P8 = read.signed_short(0x9C)
    compensation.dig_P9 = read.signed_short(0x9E)

    # Humidity trimming params
    compensation.dig_H1 = read.unsigned_byte(0xA1)
    compensation.dig_H2 = read.signed_short(0xE1)
    compensation.dig_H3 = read.signed_byte(0xE3)

    e4 = read.signed_byte(0xE4)
    e5 = read.signed_byte(0xE5)
    e6 = read.signed_byte(0xE6)

    compensation.dig_H4 = e4 << 4 | e5 & 0x0F
    compensation.dig_H5 = (e5 & 0xF0) << 12 | e6
    compensation.dig_H6 = read.signed_byte(0xE7)
