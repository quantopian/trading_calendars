# trading_calendars
A Python library of securities exchange calendars meant to be used with [Zipline](https://github.com/quantopian/zipline).

## Usage
```python
from trading_calendars import get_calendar

# US Stock Exchanges (includes NASDAQ)
nyse_calendar = get_calendar('NYSE')
# London Stock Exchange
lse_calendar = get_calendar('LSE')
# Toronto Stock Exchange
tsx_calendar = get_calendar('TSX')

# US Futures
us_futures_calendar = get_calendar('us_futures')
# Chicago Mercantile Exchange
cme_calendar = get_calendar('CME')
# Intercontinental Exchange
ice_calendar = get_calendar('ICE')
# CBOE Futures Exchange
cfe_calendar = get_calendar('CFE')
# Brazilian Mercantile and Futures Exchange
bmf_calendar = get_calendar('BMF')
```
