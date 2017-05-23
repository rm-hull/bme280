#!/usr/bin/env python

# basic script to test BME280 functionality

import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address)

print("compensation_params = {0}".format(bme280.compensation_params))

# the compensated_reading class has the following attributes:
#
#   data.id
#   data.timestamp
#   data.temperature
#   data.pressure
#   data.humidity
#   data.uncompensated

print(data.uncompensated)

# there is a handy string representation too
print(data)
