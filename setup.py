#!/usr/bin/env python

import os
import re
import sys
from setuptools import setup

here = os.path.dirname(__file__)

README = open(os.path.join(here, 'README.rst')).read()


def _read_version():
    with open(os.path.join(here, 'bme280', '__init__.py')) as code:
        contents = code.read()
    match = re.search(r'__version__\s*=\s*["\'](.*?)["\']', contents)
    return match.group(1)


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'mock;python_version<"3.3"',
    'pytest>=3.1',
    'pytest-cov'
]

version = _read_version()

setup(
    name="RPi.bme280",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description="A library to drive a Bosch BME280 temperature, humidity, pressure sensor over I2C",
    long_description=README,
    license="MIT",
    keywords=["raspberry pi", "orange pi", "banana pi", "rpi", "bosch", "BME280", "i2c", "temperature", "humidity", "pressure"],
    url="https://github.com/rm-hull/bme280",
    download_url="https://github.com/rm-hull/bme280/tarball/" + version,
    packages=['bme280'],
    install_requires=["pytz", "smbus2"],
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
