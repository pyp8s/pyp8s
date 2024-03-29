# pyp8s

Customisable prometheus exporter for your python application.

Currently not that much customisable, though.

## Installation

```bash
python3 -m pip install pyp8s
```

## Usage

Examples: [https://github.com/pyp8s/examples](https://github.com/pyp8s/examples)

MetricsHandler implements a singleton.

```python
from pyp8s import MetricsHandler as meh

if __name__ == '__main__':

    meh.serve(listen_address="0.0.0.0", listen_port=8081)

    meh.init("calls", "counter", "Number of calls I've received")
    meh.init("doorbells", "counter", "Number of doorbells I've answered")
    meh.init("yawns", "counter", "Quite self-explanatory")
    meh.init("mood", "gauge", "How do I feel myself from 1 to good enough")
    meh.init("giggles", "counter", "Measurement of the joke power.", init_value=0)

    meh.inc("calls", 1)

    meh.inc("doorbells", 100, can="have", extra="labels", since="2.1.0")
    meh.inc("doorbells", 9000, this="will", be="useful")

    meh.inc("yawns", 8, satisfying="yes")
    meh.inc("yawns", 1, satisfying="no", loud="yes")

    meh.set("mood", 3)
    meh.set("mood", 6)
```

```bash
curl 127.0.0.1:8081/metrics
```

```bash
# HELP http_get_requests Number GET requests accepted
# TYPE http_get_requests counter
http_get_requests{} 1
# HELP http_get_metrics Number times the metrics endpoint was called
# TYPE http_get_metrics counter
http_get_metrics{} 1
# HELP calls Number of calls I've received
# TYPE calls counter
calls{} 1
# HELP doorbells Number of doorbells I've answered
# TYPE doorbells counter
doorbells{can="have",extra="labels",since="2.1.0"} 100
doorbells{this="will",be="useful"} 9000
# HELP yawns Quite self-explanatory
# TYPE yawns counter
yawns{satisfying="yes"} 8
yawns{satisfying="no",loud="yes"} 1
# HELP mood How do I feel myself from 1 to good enough
# TYPE mood gauge
mood{} 6
# HELP giggles Measurement of the joke power.
# TYPE giggles counter
giggles{} 0
```

## Usage without starting a server

When you only need this thing to collect and render metrics:

```python
from pyp8s import MetricsHandler as meh

if __name__ == '__main__':
    meh.init("calls", "counter", "Number of calls I've received")

    print(meh.render())
```

`render()` returns a string object.

## Test environment

```bash
python3.10 -m virtualenv --prompt="py3.10 pyp8s" .virtualenv
source .virtualenv/bin/activate
```

## Reporting bugs

Please, use GitHub issues.

## Requesting new functionality

Please, use GitHub issues.
