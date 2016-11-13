#!/usr/bin/env python

import os
from distutils.core import setup, Extension

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name = "bme280",
    version = "0.1.0",
    author = "Richard Hull",
    author_email = "richard.hull@destructuring-bind.org",
    description = "A library to drive a Bosch BME280 tempperature, humidity, pressure sensor over I2C",
    long_description = README,
    license = "MIT",
    keywords = ["raspberry pi", "rpi", "bosch", "BME280", "i2c", "temperature", "humidity", "pressure"],
    url = "https://github.com/rm-hull/bme280",
    download_url = "https://github.com/rm-hull/bme280/tarball/0.1.0",
    packages = ['bme280'],
    install_requires = ["smbus","pillow"],
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
