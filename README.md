# trading_calendars
A Python library of securities exchange calendars meant to be used with [Zipline](https://github.com/quantopian/zipline).

Note that exchange calendars are defined by their [ISO-10383 market identifier code](https://www.iso20022.org/10383/iso-10383-market-identifier-codes).

## Usage
```python
from trading_calendars import get_calendar

# US Stock Exchanges (includes NASDAQ)
us_calendar = get_calendar('XNYS')
# London Stock Exchange
london_calendar = get_calendar('XLON')
# Toronto Stock Exchange
toronto_calendar = get_calendar('XTSE')
# Tokyo Stock Exchange
tokyo_calendar = get_calendar('XTKS')
# Frankfurt Stock Exchange
frankfurt_calendar = get_calendar('XFRA')

# US Futures
us_futures_calendar = get_calendar('us_futures')
# Chicago Mercantile Exchange
cme_calendar = get_calendar('CMES')
# Intercontinental Exchange
ice_calendar = get_calendar('IEPA')
# CBOE Futures Exchange
cfe_calendar = get_calendar('XCBF')
# Brazilian Mercantile and Futures Exchange
bmf_calendar = get_calendar('BVMF')
```
