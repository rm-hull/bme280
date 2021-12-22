# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Richard Hull
# See LICENSE.rst for details.

import bme280.const as c
from bme280.const import ConstError
import pytest

c.const1 = "goodbye"
c.const2 = "cruel"
c.const3 = "world"


def test_simple_assignment():
    assert c.const1 == "goodbye"


def test_to_string():
    assert "'const1': 'goodbye'" in str(c)
    assert "'const2': 'cruel'" in str(c)
    assert "'const3': 'world'" in str(c)


def test_rebind_throws_error():
    with pytest.raises(ConstError) as excinfo:
        del c.const1
    assert "Can't unbind const(const1)" in str(excinfo.value)


def test_unbind_throws_error():
    with pytest.raises(ConstError) as excinfo:
        c.const1 = "hello"
    assert "Can't rebind const(const1)" in str(excinfo.value)
