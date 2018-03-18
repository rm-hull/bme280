#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull
# See LICENSE.rst for details.

import bme280.const as c

c.const1 = "goodbye"
c.const2 = "cruel"
c.const3 = "world"


def test_simple_assignment():
    assert c.const1 == "goodbye"


def test_to_string():
    assert "'const1': 'goodbye'" in str(c)
    assert "'const2': 'cruel'" in str(c)
    assert "'const3': 'world'" in str(c)
