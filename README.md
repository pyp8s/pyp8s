# py-p8s-metrics

Customisable prometheus exporter for your python application.

Currently not that much customisable, though.

## Usage

MetricsHandler implements a singleton.

```python
from py_p8s_metrics import MetricsHandler as meh

if __name__ == '__main__':
	meh.serve(listen_address="0.0.0.0", listen_port=8081)
	meh.set_metrics_name("myMetric")
	meh.inc("significantMetricKind", 1)
	meh.inc("significantMetricKind", 1)
	meh.set("otherMetricKind", 9000)
```

```
curl 127.0.0.1:8081/metrics
# TYPE myMetric counter
myMetric{kind="significantMetricKind"} 2
myMetric{kind="otherMetricKind"} 9000
```

## Test environment

```bash
python3.10 -m virtualenv --prompt="py3.10 pyp8s" .virtualenv
source .virtualenv/bin/activate
```

## Reporting bugs

Please, use GitHub issues.

## Requesting new functionality

Please, use GitHub issues.
