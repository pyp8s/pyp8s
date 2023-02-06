#!/usr/bin/env python3
# pylint: disable=line-too-long, missing-function-docstring, logging-fstring-interpolation
# pylint: disable=too-many-locals, broad-except, too-many-arguments, raise-missing-from
"""
    pyp8s module
"""

import pytest

from pyp8s import MetricsHandler


def test_inc_1():
    MetricsHandler.inc("testMetric", 1)


@pytest.mark.xfail()
def test_double_start():
    MetricsHandler.serve()
    MetricsHandler.serve()

