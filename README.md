# py-p8s-metrics

Customisable prometheus exporter for your python application.


## Usage

```python
from py_p8s_metrics import MetricsHandler as meh

if __name__ == '__main__':
	meh.serve()
	meh.set_metrics_name("myMetric")
	meh.inc("significantMetricKind", 9000)
```

## Test environment

```bash
python3.10 -m virtualenv --prompt="py3.10 rmq" .virtualenv
```

## Reporting bugs

Please, use GitHub issues.

## Requesting new functionality

Please, use GitHub issues.
