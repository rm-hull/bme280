# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# See LICENSE.rst for details.


try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock, MagicMock  # noqa: F401

from datetime import datetime
import bme280
import pytz

smbus = Mock(unsafe=True)

compensation_params = bme280.params()
compensation_params.dig_H1 = 0
compensation_params.dig_H2 = 1
compensation_params.dig_H3 = 4
compensation_params.dig_H4 = 3
compensation_params.dig_H5 = 5
compensation_params.dig_H6 = 6
compensation_params.dig_P1 = 10
compensation_params.dig_P2 = 11
compensation_params.dig_P3 = 12
compensation_params.dig_P4 = 13
compensation_params.dig_P5 = 14
compensation_params.dig_P6 = 15
compensation_params.dig_P7 = 16
compensation_params.dig_P8 = 17
compensation_params.dig_P9 = 18
compensation_params.dig_T1 = 20
compensation_params.dig_T2 = 21
compensation_params.dig_T3 = 22


def setup_function(function):
    smbus.reset_mock()


def test_load_calibration_params():
    smbus.read_word_data = MagicMock(side_effect=list(range(400)))
    smbus.read_byte_data = MagicMock(side_effect=list(range(400)))
    calibration_params = bme280.load_calibration_params(bus=smbus, address=0x77)
    assert calibration_params == {
        'dig_H1': 0,
        'dig_H2': 12,
        'dig_H3': 1,
        'dig_H4': 35,
        'dig_H5': 64,
        'dig_H6': 5,
        'dig_P1': 3,
        'dig_P2': 4,
        'dig_P3': 5,
        'dig_P4': 6,
        'dig_P5': 7,
        'dig_P6': 8,
        'dig_P7': 9,
        'dig_P8': 10,
        'dig_P9': 11,
        'dig_T1': 0,
        'dig_T2': 1,
        'dig_T3': 2
    }


def test_sample_with_params():
    smbus.write_byte_data = MagicMock()
    smbus.read_i2c_block_data = MagicMock(return_value=list(range(8)))

    data = bme280.sample(bus=smbus, address=0x76,
                         compensation_params=compensation_params)

    assert data.pressure == 8801790.518824806
    assert data.temperature == 0.0030482932925224304
    assert data.humidity == 0.02082886288568924


def test_sample_without_params():
    smbus.write_byte_data = MagicMock()
    smbus.read_word_data = MagicMock(side_effect=list(range(400)))
    smbus.read_byte_data = MagicMock(side_effect=list(range(400)))
    smbus.read_i2c_block_data = MagicMock(return_value=list(range(8)))

    data = bme280.sample(bus=smbus, address=0x76)

    print(data)
    assert data.pressure == 37118275.30149117
    assert data.temperature == 0.0001507163979113102
    assert data.humidity == 0.0


def test_uncompensated_readings_repr():
    block = [1, 1, 2, 3, 5, 8, 13, 21]
    reading = bme280.uncompensated_readings(block)
    assert repr(reading) == "uncompensated_reading(temp=0x00003050, pressure=0x00001010, humidity=0x00000D15, block=01:01:02:03:05:08:0D:15)"


def test_compensated_readings_repr():
    block = [1, 1, 2, 3, 5, 8, 13, 21]
    raw = bme280.uncompensated_readings(block)
    reading = bme280.compensated_readings(raw, compensation_params)
    reading.id = "55fea298-5a5d-4873-a46d-b631c8748100"
    reading.timestamp = datetime(2018, 3, 18, 19, 26, 14, 206233, tzinfo=pytz.UTC)
    assert repr(reading) == "compensated_reading(id=55fea298-5a5d-4873-a46d-b631c8748100, timestamp=2018-03-18 19:26:14.206233UTC, temp=0.003 °C, pressure=8758647.58 hPa, humidity=0.05 % rH)"


def test_compensated_readings_repr_zero_millis():
    block = [1, 1, 2, 3, 5, 8, 13, 21]
    raw = bme280.uncompensated_readings(block)
    reading = bme280.compensated_readings(raw, compensation_params)
    reading.id = "55fea298-5a5d-4873-a46d-b631c8748100"
    reading.timestamp = datetime(2018, 3, 18, 19, 26, 14, tzinfo=pytz.UTC)
    assert repr(reading) == "compensated_reading(id=55fea298-5a5d-4873-a46d-b631c8748100, timestamp=2018-03-18 19:26:14.000000UTC, temp=0.003 °C, pressure=8758647.58 hPa, humidity=0.05 % rH)"
