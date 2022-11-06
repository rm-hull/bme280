# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Richard Hull
# See LICENSE.rst for details.

from unittest.mock import Mock, MagicMock
from bme280.reader import Reader

smbus = Mock(unsafe=True)


def setup_function(function):
    smbus.reset_mock()


def test_unsigned_short():
    smbus.read_word_data = MagicMock(return_value=0xDEADBEEF)
    read = Reader(bus=smbus, address=0x76)
    assert read.unsigned_short(register=0x19A) == 0xBEEF
    smbus.read_word_data.assert_called_with(0x76, 0x19A)


def test_signed_short():
    smbus.read_word_data = MagicMock(return_value=0xCAFEBABE)
    read = Reader(bus=smbus, address=0x76)
    assert read.signed_short(register=0x19A) == 0xBABE - 0x10000
    smbus.read_word_data.assert_called_with(0x76, 0x19A)


def test_unsigned_byte():
    smbus.read_byte_data = MagicMock(return_value=0xEE)
    read = Reader(bus=smbus, address=0x76)
    assert read.unsigned_byte(register=0x19A) == 0xEE
    smbus.read_byte_data.assert_called_with(0x76, 0x19A)


def test_signed_byte():
    smbus.read_byte_data = MagicMock(return_value=0xEE)
    read = Reader(bus=smbus, address=0x76)
    assert read.signed_byte(register=0x19A) == 0xEE - 0x100
    smbus.read_byte_data.assert_called_with(0x76, 0x19A)
