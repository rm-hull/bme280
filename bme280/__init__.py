#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

"""
Raspberry Pi BME280 Driver.
"""

__version__ = "0.2.2"

import datetime
import time
import uuid

from bme280.reader import reader
import bme280.const as oversampling

# Oversampling modes
oversampling.x1 = 1
oversampling.x2 = 2
oversampling.x4 = 3
oversampling.x8 = 4
oversampling.x16 = 5

DEFAULT_PORT = 0x76


class uncompensated_readings(object):

    def __init__(self, block):
        self._block = block
        self.pressure = (block[0] << 16 | block[1] << 8 | block[2]) >> 4
        self.temperature = (block[3] << 16 | block[4] << 8 | block[5]) >> 4
        self.humidity = block[6] << 8 | block[7]

    def __repr__(self):
        return "uncompensated_reading(temp=0x{0:08X}, pressure=0x{1:08X}, humidity=0x{2:08X}, block={3})".format(
            self.temperature, self.pressure, self.humidity,
            ":".join("{0:02X}".format(c) for c in self._block))


class compensated_readings(object):
    """
    Compensation formulas translated from Appendix A (8.1) of BME280 datasheet:

       * Temperature in °C, double precision. Output value of "51.23"
         equals 51.23 °C

       * Pressure in hPa as double. Output value of "963.862" equals
         963.862 hPa

       * Humidity in %rH as as double. Output value of "46.332" represents
         46.332 %rH
    """
    def __init__(self, raw_readings, compensation_params):
        self._comp = compensation_params
        self.id = uuid.uuid4()
        self.uncompensated = raw_readings
        self.timestamp = datetime.datetime.now()
        self.temperature = self.__tfine(raw_readings.temperature) / 5120.0
        self.humidity = self.__calc_humidity(raw_readings.humidity,
                                             raw_readings.temperature)
        self.pressure = self.__calc_pressure(raw_readings.pressure,
                                             raw_readings.temperature) / 100.0

    def __tfine(self, t):
        v1 = (t / 16384.0 - self._comp.dig_T1 / 1024.0) * self._comp.dig_T2
        v2 = ((t / 131072.0 - self._comp.dig_T1 / 8192.0) ** 2) * self._comp.dig_T3
        return v1 + v2

    def __calc_humidity(self, h, t):
        res = self.__tfine(t) - 76800.0
        res = (h - (self._comp.dig_H4 * 64.0 + self._comp.dig_H5 / 16384.0 * res)) * \
            (self._comp.dig_H2 / 65536.0 * (1.0 + self._comp.dig_H6 / 67108864.0 * res *
                                            (1.0 + self._comp.dig_H3 / 67108864.0 * res)))
        res = res * (1.0 - (self._comp.dig_H1 * res / 524288.0))
        return max(0.0, min(res, 100.0))

    def __calc_pressure(self, p, t):
        v1 = self.__tfine(t) / 2.0 - 64000.0
        v2 = v1 * v1 * self._comp.dig_P6 / 32768.0
        v2 = v2 + v1 * self._comp.dig_P5 * 2.0
        v2 = v2 / 4.0 + self._comp.dig_P4 * 65536.0
        v1 = (self._comp.dig_P3 * v1 * v1 / 524288.0 + self._comp.dig_P2 * v1) / 524288.0
        v1 = (1.0 + v1 / 32768.0) * self._comp.dig_P1

        # Prevent divide by zero
        if v1 == 0:
            return 0

        res = 1048576.0 - p
        res = ((res - v2 / 4096.0) * 6250.0) / v1
        v1 = self._comp.dig_P9 * res * res / 2147483648.0
        v2 = res * self._comp.dig_P8 / 32768.0
        res = res + (v1 + v2 + self._comp.dig_P7) / 16.0
        return res

    def __repr__(self):
        return "compensated_reading(id={0}, timestamp={1}, temp={2:0.3f} °C, pressure={3:0.2f} hPa, humidity={4:0.2f} % rH)".format(
            self.id, self.timestamp, self.temperature, self.pressure, self.humidity)


class params(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


def load_calibration_params(bus, address=DEFAULT_PORT):
    """
    The BME280 output consists of the ADC output values. However, each sensing
    element behaves differently. Therefore, the actual pressure and temperature
    must be calculated using a set of calibration parameters.

    The calibration parameters are subsequently used to with some compensation
    formula to perform temperature readout in degC, humidity in % and pressure
    in hPA.
    """
    read = reader(bus, address)
    compensation_params = params()

    # Temperature trimming params
    compensation_params.dig_T1 = read.unsigned_short(0x88)
    compensation_params.dig_T2 = read.signed_short(0x8A)
    compensation_params.dig_T3 = read.signed_short(0x8C)

    # Pressure trimming params
    compensation_params.dig_P1 = read.unsigned_short(0x8E)
    compensation_params.dig_P2 = read.signed_short(0x90)
    compensation_params.dig_P3 = read.signed_short(0x92)
    compensation_params.dig_P4 = read.signed_short(0x94)
    compensation_params.dig_P5 = read.signed_short(0x96)
    compensation_params.dig_P6 = read.signed_short(0x98)
    compensation_params.dig_P7 = read.signed_short(0x9A)
    compensation_params.dig_P8 = read.signed_short(0x9C)
    compensation_params.dig_P9 = read.signed_short(0x9E)

    # Humidity trimming params
    compensation_params.dig_H1 = read.unsigned_byte(0xA1)
    compensation_params.dig_H2 = read.signed_short(0xE1)
    compensation_params.dig_H3 = read.signed_byte(0xE3)

    e4 = read.signed_byte(0xE4)
    e5 = read.signed_byte(0xE5)
    e6 = read.signed_byte(0xE6)

    compensation_params.dig_H4 = e4 << 4 | e5 & 0x0F
    compensation_params.dig_H5 = ((e5 >> 4) & 0x0F) | (e6 << 4)
    compensation_params.dig_H6 = read.signed_byte(0xE7)

    return compensation_params


__cache_calibration_params = memoize(load_calibration_params)


def __calc_delay(t_oversampling, h_oversampling, p_oversampling):
    t_delay = 0.000575 + 0.0023 * (1 << t_oversampling)
    h_delay = 0.000575 + 0.0023 * (1 << h_oversampling)
    p_delay = 0.001250 + 0.0023 * (1 << p_oversampling)
    return t_delay + h_delay + p_delay


def sample(bus, address=DEFAULT_PORT, compensation_params=None, sampling=oversampling.x1):
    """
    Primes the sensor for reading (defaut: x1 oversampling), pauses for a set
    amount of time so that the reading stabilizes, and then returns a
    compensated reading object with the following attributes:
        * timestamp (Python's datetime object) when reading was taken.
        * temperature, in degrees Celcius.
        * humidity, in % relative humidity.
        * pressure, in hPa.
    """
    if compensation_params is None:
        compensation_params = __cache_calibration_params(bus, address)

    mode = 1  # forced
    t_oversampling = sampling or oversampling.x1
    h_oversampling = sampling or oversampling.x1
    p_oversampling = sampling or oversampling.x1

    bus.write_byte_data(address, 0xF2, h_oversampling)  # ctrl_hum
    bus.write_byte_data(address, 0xF4, t_oversampling << 5 | p_oversampling << 2 | mode)  # ctrl
    delay = __calc_delay(t_oversampling, h_oversampling, p_oversampling)
    time.sleep(delay)

    block = bus.read_i2c_block_data(address, 0xF7, 8)
    raw_data = uncompensated_readings(block)
    return compensated_readings(raw_data, compensation_params)
