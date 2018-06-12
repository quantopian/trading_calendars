# trading_calendars
A Python library of securities exchange calendars meant to be used with [Zipline](https://github.com/quantopian/zipline).

## Installation
With pip:
```
pip install trading-calendars
```
With conda:
```
conda install trading-calendars
```

## Usage
```python
from trading_calendars import get_calendar
nyse_calendar = get_calendar('NYSE')
```
