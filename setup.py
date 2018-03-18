#!/usr/bin/env python

import os
import sys
from setuptools import setup

import bme280

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'mock;python_version<"3.3"',
    'pytest>=3.1',
    'pytest-cov'
]

setup(
    name="RPi.bme280",
    version=bme280.__version__,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description="A library to drive a Bosch BME280 temperature, humidity, pressure sensor over I2C",
    long_description=README,
    license="MIT",
    keywords=["raspberry pi", "orange pi", "banana pi", "rpi", "bosch", "BME280", "i2c", "temperature", "humidity", "pressure"],
    url="https://github.com/rm-hull/bme280",
    download_url="https://github.com/rm-hull/bme280/tarball/" + bme280.__version__,
    packages=['bme280'],
    install_requires=["smbus2"],
    setup_requires=pytest_runner,
    tests_require=test_deps,
    extras_require={
        'qa': [
            'rstcheck',
            'flake8'
        ],
        'test': test_deps
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
