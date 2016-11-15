#!/usr/bin/env python

import os
from setuptools import setup

import bme280

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name = "RPi.bme280",
    version = bme280.__version__,
    author = "Richard Hull",
    author_email = "richard.hull@destructuring-bind.org",
    description = "A library to drive a Bosch BME280 tempperature, humidity, pressure sensor over I2C",
    long_description = README,
    license = "MIT",
    keywords = ["raspberry pi", "rpi", "bosch", "BME280", "i2c", "temperature", "humidity", "pressure"],
    url = "https://github.com/rm-hull/bme280",
    download_url = "https://github.com/rm-hull/bme280/tarball/" + bme280.__version__,
    packages = ['bme280'],
    install_requires = ["pillow", "smbus2"],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
