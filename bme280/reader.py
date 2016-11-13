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


# bus is an instance of SMBus
# default is little endian

class reader(object):
    """
    Wraps a I2C SMBus instance to provide methods for reading
    signed/unsigned bytes and 16-bit words
    """
    def __init__(self, bus, address):
        self._bus = bus
        self._address = address

    def unsigned_short(self, register):
        return self._bus.read_word_data(self._address, register) & 0xffff

    def signed_short(self, register):
        word = self.unsigned_short(register)
        return word if word < 0x8000 else word - 0x10000

    def unsigned_byte(self, register):
        return self._bus.read_byte_data(self._address, register) & 0xff

    def signed_byte(self, register):
        byte = self.unsigned_byte(register) & 0xff
        return byte if byte < 0x80 else byte - 0x100
