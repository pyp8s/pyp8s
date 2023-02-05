#!/usr/bin/env python3
# pylint: disable=line-too-long, missing-function-docstring, logging-fstring-interpolation
# pylint: disable=too-many-locals, broad-except, too-many-arguments, raise-missing-from
# pylint: disable=import-error
"""

  Prometheus metrics server and collector
  ===================================================

  Starts HTTP server and serves Prometheus metrics

  GitHub repository:
  https://github.com/***

  Community support:
  https://github.com/***/issues

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


VERSION = (1, 0, 1)
__version__ = ".".join(map(str, VERSION))


class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class MetricsHandler(metaclass=Singleton):

  def __init__(self):
    self.uuid = str(uuid.uuid4())
    self.server = None
    self.metrics = {}


  @staticmethod
  def serve(listen_address="0.0.0.0", listen_port=19001):
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} Starting the metrics server on {listen_address} port {listen_port}")

    self.server = ThreadedHTTPServer((listen_address, listen_port), ReqHandlerMetrics)
    self.server_thread = threading.Thread(target=self.server.serve_forever)

    self.server_thread.daemon = True

    logging.info(f"UUID={self.uuid} Starting metrics server")
    self.server_thread.start()
    logging.info(f"UUID={self.uuid} Metrics server started")


  @staticmethod
  def shutdown():
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} Shutting down the metrics server")
    return self.server.shutdown()


  @staticmethod
  def get_metrics():
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} Returning metrics")
    return self.metrics


  @staticmethod
  def set_metrics_name(metrics_name):
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} Setting metrics name to '{metric_name}'")
    self.metrics_name = metric_name


  @staticmethod
  def get_metrics_name():
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} Returning metrics name: '{metric_name}'")
    return self.metrics_name


  @staticmethod
  def inc(metric_name, increment):
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} incrementing {metric_name} for {increment}")

    if metric_name in self.metrics:
      self.metrics[metric_name] += increment
    else:
      self.metrics[metric_name] = increment


  @staticmethod
  def set(metric_name, value):
    self = MetricsHandler()
    logging.debug(f"UUID={self.uuid} incrementing {metric_name} for {increment}")

    self.metrics[metric_name] = value


class ReqHandlerMetrics(BaseHTTPRequestHandler):

    def do_GET(self):
      self.send_response(200)
      self.end_headers()

      MetricsHandler.inc("http_get_requests", 1)

      if self.path == "/":
        MetricsHandler.inc("http_get_index", 1)
        header = """<html><head><title>Node Exporter</title></head><body><p><a href="/metrics">Metrics</a></p></body></html>"""
        self.wfile.write(bytes(header, "utf-8"))

      elif self.path == "/metrics":
        MetricsHandler.inc("http_get_metrics", 1)
        metric_header = f"""# TYPE {MetricsHandler.get_metrics_name()} counter\n"""
        self.wfile.write(bytes(metric_header, "utf-8"))

        for metric_key, metric_value in MetricsHandler.get_metrics().items():
            metric_line = f"""{MetricsHandler.get_metrics_name()}{{kind="{metric_key}"}} {metric_value}\n"""
            self.wfile.write(bytes(metric_line, "utf-8"))

      else:
        response = {"error": True, "message": "Bad request, bad"}
        self.wfile.write(json.dumps(response))

      return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == '__main__':

  logging.root.handlers = []
  logging.basicConfig(
      level=logging.DEBUG,
      format="%(asctime)s function=%(name)s.%(funcName)s level=%(levelname)s %(message)s",
      handlers=[
          logging.StreamHandler()
      ]
  )


  MetricsHandler.inc("calls", 1)
  MetricsHandler.inc("calls", 20)
  MetricsHandler.inc("calls", 1000)
  MetricsHandler.inc("calls", 1)

  MetricsHandler.serve()
  logging.debug("Waiting before shutdown")
  time.sleep(20)
  MetricsHandler.shutdown()
