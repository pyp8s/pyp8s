#!/usr/bin/env python3
# pylint: disable=line-too-long, missing-function-docstring, logging-fstring-interpolation
# pylint: disable=too-many-locals, broad-except, too-many-arguments, raise-missing-from
# pylint: disable=import-error
"""

  Prometheus metrics server and collector
  =======================================

  Starts HTTP server and serves Prometheus metrics

  GitHub repository:
  https://github.com/pyp8s/pyp8s

  Community support:
  https://github.com/pyp8s/pyp8s/issues

  Copyright © 2022, Pavel Kim

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import logging
import uuid
import json
import time


class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Metric():

    def __init__(self, metric_name=None):
        self.metric_name = metric_name
        self.help_header = None
        self.metric_type = None

        self.data = {}

    def __unicode__(self):
        return f"<Metric {self.metric_name} ({self.metric_type}) with {len(self.data.keys())} labels>"

    def __str__(self):
        return f"<Metric {self.metric_name} ({self.metric_type}) with {len(self.data.keys())} labels>"

    def __repr__(self):
        return self.__str__()

    def __format_labels(self, **kwargs):
        return ["=".join([f"{pair[0]}", f'"{pair[1]}"']) for pair in kwargs.items()]

    def __craft_labelset_key(self, **kwargs):
        kwargs_items_sorted = sorted(kwargs.items(), key=lambda x: x[0].casefold())
        kwargs_items_joined_pairs = ["_".join([str(pair[0]), str(pair[1])]) for pair in kwargs_items_sorted]
        kwargs_items_joined_full = "_".join(kwargs_items_joined_pairs)

        return kwargs_items_joined_full

    def __get_labelset_item(self, *args, **kwargs):

        labelset_key = self.__craft_labelset_key(**kwargs)

        if labelset_key not in self.data:

            self.data[labelset_key] = {
                "value": 0,
                "labels": {
                    **kwargs  # TODO: Validate kwargs before saving them
                },
                "labels_formatted": self.__format_labels(**kwargs)
            }

        return self.data[labelset_key]

    def set_name(self, metric_name):
        self.metric_name = metric_name

    def set_type(self, metric_type):
        self.metric_type = metric_type

    def set_help(self, help_header):
        self.help_header = help_header

    def get_name(self):
        return self.metric_name

    def get_type(self):
        return self.metric_type

    def get_help(self):
        return self.help_header

    def get_labelsets(self):
        return self.data

    def inc(self, increment, *args, **kwargs):
        """Increments metric by given number

        :param increment: How much the metric should be incremented by
        :type increment: int
        :param **args: Ignored
        :type **args: any
        :param **kwargs: Additional labels for the metric
        :type **kwargs: dict[str]

        :return: None
        :rtype: None
        """

        metric = self.__get_labelset_item(**kwargs)
        metric["value"] += increment
        logging.debug(f"Incremented metric '{metric}' (new {metric['value']})")

    def set(self, value, *args, **kwargs):
        """Sets metric value to a given number

        :param value: New value for the metric to set
        :type value: int
        :param **args: Ignored
        :type **args: any
        :param **kwargs: Additional labels for the metric
        :type **kwargs: dict[str]

        :return: None
        :rtype: None
        """

        metric = self.__get_labelset_item(**kwargs)
        metric["value"] = value
        logging.debug(f"Incremented metric '{metric}' (new {metric['value']})")


class MetricsHandler(metaclass=Singleton):

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.server = None
        self.metrics = {}

    def __is_serving(self):
        return self.server is not None

    @staticmethod
    def serve(listen_address="127.0.0.1", listen_port=19001):
        self = MetricsHandler()

        if not self.__is_serving():

            logging.debug(f"Starting the metrics server on {listen_address} port {listen_port}")

            self.server = ThreadedHTTPServer((listen_address, listen_port), ReqHandlerMetrics)
            self.server_thread = threading.Thread(target=self.server.serve_forever)

            self.server_thread.daemon = True

            logging.info(f"Starting metrics server")
            self.server_thread.start()
            logging.info(f"Metrics server started")

        else:
            logging.error(f"Tried to start the metrics server twice")
            raise Exception(f"Server already started: {self.server}")

    @staticmethod
    def shutdown():
        self = MetricsHandler()
        logging.debug(f"Shutting down the metrics server")

        try:
            self.server.shutdown()
        except Exception as e:
            logging.error(f"Couldn't shutdown the metrics server: {e}")
            raise e

    @staticmethod
    def get_metrics():
        self = MetricsHandler()
        return self.metrics

    @staticmethod
    def get_metric(metric_name):
        self = MetricsHandler()
        return self.metrics[metric_name]

    @staticmethod
    def __get_metric_obj(metric_name):
        self = MetricsHandler()

        if metric_name not in self.metrics:
            self.metrics[metric_name] = Metric(metric_name=metric_name)

        return self.metrics[metric_name]

    @staticmethod
    def inc(metric_name, increment, *args, **kwargs):
        """Increments metric by given number

        :param metric_name: Metric name to manipulate
        :type metric_name: str
        :param increment: How much the metric should be incremented by
        :type increment: int
        :param **args: Ignored
        :type **args: any
        :param **kwargs: Additional labels for the metric
        :type **kwargs: dict[str]

        :return: None
        :rtype: None
        """

        self = MetricsHandler()

        metric = self.__get_metric_obj(metric_name=metric_name)
        metric.inc(increment=increment, **kwargs)

    @staticmethod
    def set(metric_name, value, *args, **kwargs):
        """Sets metric value to a given number

        :param metric_name: Metric name to manipulate
        :type metric_name: str
        :param value: New value for the metric to set
        :type value: int
        :param **args: Ignored
        :type **args: any
        :param **kwargs: Additional labels for the metric
        :type **kwargs: dict[str]

        :return: None
        :rtype: None
        """

        self = MetricsHandler()

        metric = self.__get_metric_obj(metric_name=metric_name)
        metric.set(value=value, **kwargs)

    @staticmethod
    def init(metric_name, metric_type, description=None):
        self = MetricsHandler()

        metric = self.__get_metric_obj(metric_name=metric_name)
        metric.set_help(description)
        metric.set_type(metric_type)


class ReqHandlerMetrics(BaseHTTPRequestHandler):

    MetricsHandler.init("http_get_requests", "counter", "Number GET requests accepted")
    MetricsHandler.init("http_get_metrics", "counter", "Number times the metrics endpoint was called")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        MetricsHandler.inc("http_get_requests", 1)

        if self.path == "/":
            MetricsHandler.inc("http_get_index", 1)
            header = """<html><head><title>pyp8s Exporter</title></head><body><p><a href="/metrics">Metrics</a></p></body></html>\n"""
            self.wfile.write(bytes(header, "utf-8"))

        elif self.path == "/metrics":
            MetricsHandler.inc("http_get_metrics", 1)

            for metric_name, metric_item in MetricsHandler.get_metrics().items():

                help_header = f"""# HELP {metric_name} {metric_item.get_help()}\n"""
                self.wfile.write(bytes(help_header, "utf-8"))

                type_header = f"""# TYPE {metric_name} {metric_item.get_type()}\n"""
                self.wfile.write(bytes(type_header, "utf-8"))

                for _, labelset in metric_item.get_labelsets().items():
                    metric_value = labelset['value']
                    metric_labels_formatted_joined = ",".join(labelset['labels_formatted'])

                    metric_line = f"""{metric_name}{{{metric_labels_formatted_joined}}} {metric_value}\n"""
                    self.wfile.write(bytes(metric_line, "utf-8"))


        else:
            response = {"error": True, "message": "Bad request, bad"}
            self.wfile.write(json.dumps(response))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == '__main__':

    logging.root.handlers = []
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s level=%(levelname)s function=%(name)s.%(funcName)s %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    MetricsHandler.init("calls", "counter", "Number of calls I've received")
    MetricsHandler.init("doorbells", "counter", "Number of doorbells I've answered")
    MetricsHandler.init("yawns", "counter", "Quite self-explanatory")

    MetricsHandler.inc("calls", 1)
    MetricsHandler.inc("calls", 1, who="telemarketers", when="morning")
    MetricsHandler.inc("calls", 1, who="collectors", when="all_day")
    MetricsHandler.inc("calls", 1, who="collectors", when="all_day")
    MetricsHandler.inc("calls", 1, who="collectors", when="all_day")
    MetricsHandler.inc("calls", 1, who="collectors", when="all_day")

    MetricsHandler.inc("doorbells", 1)
    MetricsHandler.inc("doorbells", 2, also_knoked="yes")
    MetricsHandler.inc("doorbells", 8, also_knoked="no")
    MetricsHandler.inc("doorbells", 3, also_knoked="yes")

    MetricsHandler.inc("yawns", 8, satisfying="yes")
    MetricsHandler.inc("yawns", 1, satisfying="no", loud="yes")
    MetricsHandler.inc("yawns", 1, satisfying="yes", loud="yes")
    MetricsHandler.inc("yawns", 1, satisfying="meh",  loud="no")

    MetricsHandler.set("busy", 13)

    small_hack = {
        "from": "Glasgow",
        "if": "fi",
    }

    MetricsHandler.set("busy", 200, **small_hack)
    MetricsHandler.set("busy", 4, **{"for": "the", "gods": "sake", "please": "stop"})

    logging.info(f"Metrics: {MetricsHandler.get_metrics()}")

    MetricsHandler.serve(listen_address="127.0.0.1", listen_port=9000)
    logging.debug("Waiting before shutdown")
    time.sleep(20)
    MetricsHandler.shutdown()
