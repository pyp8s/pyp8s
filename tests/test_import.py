#!/usr/bin/env python3
# pylint: disable=line-too-long, missing-function-docstring, logging-fstring-interpolation
# pylint: disable=too-many-locals, broad-except, too-many-arguments, raise-missing-from
"""
    py-p8s-metrics module
"""

from py_p8s_metrics import MetricsHandler


def test_inc_1():
    metrics_handler = MetricsHandler.inc("testMetric", 1)

