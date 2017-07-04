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

import RPi.GPIO as GPIO
import smbus2
import time

import bme280
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306


def toggle_display(_):
    global visible
    if visible:
        oled_device.hide()
        visible = False
    else:
        oled_device.show()
        visible = True


# Setup to flash a LED on GPIO-14 (TXD)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(15, GPIO.RISING, callback=toggle_display, bouncetime=200)

visible = True
port = 1
bus = smbus2.SMBus(port)

serial = i2c(bus, address=0x3C)
oled_device = ssd1306(serial)

bme280.load_calibration_params(bus, address=0x76)  # or 0x77
fmt = '{0:5d}:  {1}  {2:0.3f} deg C,  {3:0.2f} hPa,  {4:0.2f} %'
counter = 1
while True:
    GPIO.output(14, True)
    data = bme280.sample(bus, address=0x76)  # or 0x77
    print(fmt.format(counter, data.timestamp, data.temperature, data.pressure, data.humidity))
    with canvas(oled_device) as draw:
        draw.text((0, 0), text=data.timestamp.strftime("%Y-%m-%d %H:%M:%S"), fill=255)
        draw.line((0, 12, 128, 12), fill=255)
        draw.text((0, 14), text='{0:0.3f} deg C'.format(data.temperature), fill=255)
        draw.text((0, 24), text='{0:0.2f} hPa'.format(data.pressure), fill=255)
        draw.text((0, 34), text='{0:0.2f} % rH'.format(data.humidity), fill=255)

    GPIO.output(14, False)
    time.sleep(5)
    counter += 1
