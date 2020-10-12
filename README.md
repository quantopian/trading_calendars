# trading_calendars

[![CI](https://github.com/quantopian/trading_calendars/workflows/CI/badge.svg)](https://github.com/quantopian/trading_calendars/actions?query=workflow%3ACI)
[![PyPI version](https://img.shields.io/pypi/v/trading-calendars.svg)](https://pypi.org/project/trading-calendars/)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/trading-calendars.svg)](https://anaconda.org/conda-forge/trading-calendars)

A Python library of exchange calendars, frequently used with [Zipline](https://github.com/quantopian/zipline).


## Installation

```bash
$ pip install trading-calendars
```

## Quick Start

```python
import trading_calendars as tc
import pandas as pd
import pytz
```

Get all registered calendars with `get_calendar_names`:

```python
>>> tc.get_calendar_names()[:5]
['XPHS', 'FWB', 'CFE', 'CMES', 'XSGO']
```

Get a calendar with `get_calendar`:

```python
>>> xnys = tc.get_calendar("XNYS")
```

Working with sessions:

```python
>>> xnys.is_session(pd.Timestamp("2020-01-01"))
False

>>> xnys.next_open(pd.Timestamp("2020-01-01"))
Timestamp('2020-01-02 14:31:00+0000', tz='UTC')

>>> pd.Timestamp("2020-01-01", tz=pytz.UTC)+xnys.day
Timestamp('2020-01-02 00:00:00+0000', tz='UTC')

>>> xnys.previous_close(pd.Timestamp("2020-01-01"))
Timestamp('2019-12-31 21:00:00+0000', tz='UTC')

>>> xnys.sessions_in_range(
>>>     pd.Timestamp("2020-01-01", tz=pytz.UTC),
>>>     pd.Timestamp("2020-01-10", tz=pytz.UTC)
>>> )
DatetimeIndex(['2020-01-02 00:00:00+00:00', '2020-01-03 00:00:00+00:00',
                '2020-01-06 00:00:00+00:00', '2020-01-07 00:00:00+00:00',
                '2020-01-08 00:00:00+00:00', '2020-01-09 00:00:00+00:00',
                '2020-01-10 00:00:00+00:00'],
                dtype='datetime64[ns, UTC]', freq='C')

>>> xnys.sessions_window(
>>>     pd.Timestamp("2020-01-02", tz=pytz.UTC),
>>>     7
>>> )
DatetimeIndex(['2020-01-02 00:00:00+00:00', '2020-01-03 00:00:00+00:00',
                '2020-01-06 00:00:00+00:00', '2020-01-07 00:00:00+00:00',
                '2020-01-08 00:00:00+00:00', '2020-01-09 00:00:00+00:00',
                '2020-01-10 00:00:00+00:00', '2020-01-13 00:00:00+00:00'],
                dtype='datetime64[ns, UTC]', freq='C')
```

**NOTE**: see the [TradingCalendar class](https://github.com/quantopian/trading_calendars/blob/master/trading_calendars/trading_calendar.py) for more advanced usage.

Trading calendars also supports command line usage, printing a unix-cal like calendar indicating which days are trading sessions or holidays.

```bash
tcal XNYS 2020
```
                                            2020
            January                        February                        March
    Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa
                [ 1]  2   3 [ 4]                           [ 1]
    [ 5]  6   7   8   9  10 [11]   [ 2]  3   4   5   6   7 [ 8]   [ 1]  2   3   4   5   6 [ 7]
    [12] 13  14  15  16  17 [18]   [ 9] 10  11  12  13  14 [15]   [ 8]  9  10  11  12  13 [14]
    [19][20] 21  22  23  24 [25]   [16][17] 18  19  20  21 [22]   [15] 16  17  18  19  20 [21]
    [26] 27  28  29  30  31        [23] 24  25  26  27  28 [29]   [22] 23  24  25  26  27 [28]
                                                                [29] 30  31

            April                           May                            June
    Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa
                1   2   3 [ 4]                         1 [ 2]         1   2   3   4   5 [ 6]
    [ 5]  6   7   8   9 [10][11]   [ 3]  4   5   6   7   8 [ 9]   [ 7]  8   9  10  11  12 [13]
    [12] 13  14  15  16  17 [18]   [10] 11  12  13  14  15 [16]   [14] 15  16  17  18  19 [20]
    [19] 20  21  22  23  24 [25]   [17] 18  19  20  21  22 [23]   [21] 22  23  24  25  26 [27]
    [26] 27  28  29  30            [24][25] 26  27  28  29 [30]   [28] 29  30
                                   [31]

                July                          August                       September
    Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa
                1   2 [ 3][ 4]                           [ 1]             1   2   3   4 [ 5]
    [ 5]  6   7   8   9  10 [11]   [ 2]  3   4   5   6   7 [ 8]   [ 6][ 7]  8   9  10  11 [12]
    [12] 13  14  15  16  17 [18]   [ 9] 10  11  12  13  14 [15]   [13] 14  15  16  17  18 [19]
    [19] 20  21  22  23  24 [25]   [16] 17  18  19  20  21 [22]   [20] 21  22  23  24  25 [26]
    [26] 27  28  29  30  31        [23] 24  25  26  27  28 [29]   [27] 28  29  30
                                   [30] 31

            October                        November                       December
    Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa     Su  Mo  Tu  We  Th  Fr  Sa
                    1   2 [ 3]                                            1   2   3   4 [ 5]
    [ 4]  5   6   7   8   9 [10]   [ 1]  2   3   4   5   6 [ 7]   [ 6]  7   8   9  10  11 [12]
    [11] 12  13  14  15  16 [17]   [ 8]  9  10  11  12  13 [14]   [13] 14  15  16  17  18 [19]
    [18] 19  20  21  22  23 [24]   [15] 16  17  18  19  20 [21]   [20] 21  22  23  24 [25][26]
    [25] 26  27  28  29  30 [31]   [22] 23  24  25 [26] 27 [28]   [27] 28  29  30  31
                                   [29] 30

```bash
tcal XNYS 1 2020
```

            January 2020
    Su  Mo  Tu  We  Th  Fr  Sa
                [ 1]  2   3 [ 4]
    [ 5]  6   7   8   9  10 [11]
    [12] 13  14  15  16  17 [18]
    [19][20] 21  22  23  24 [25]
    [26] 27  28  29  30  31

## Frequently Asked Questions

### Why are open times one minute late?

Due to its historical use in the [Zipline](https://github.com/quantopian/zipline) backtesting system, `trading_calendars` will only indicate a market is open upon the completion of the first minute bar in a day. Zipline uses minute bars labeled with the end of the bar, e.g. 9:31AM for 9:30-9:31AM. As an example, on a regular trading day for NYSE:

- 9:30:00 is treated as closed.
- 9:30:01 is treated as closed.
- 9:31:00 is the first time treated as open.
- 16:00:00 is treated as open
- 16:00:01 is treated as closed

This may change in the future.


## Calendar Support

| Exchange                        | ISO Code | Country        | Version Added | Exchange Website (English)                                   |
| ------------------------------- | -------- | -------------- | ------------- | ------------------------------------------------------------ |
| New York Stock Exchange         | XNYS     | USA            | 1.0           | https://www.nyse.com/index                                   |
| CBOE Futures                    | XCBF     | USA            | 1.0           | https://markets.cboe.com/us/futures/overview/                |
| Chicago Mercantile Exchange     | CMES     | USA            | 1.0           | https://www.cmegroup.com/                                    |
| ICE US                          | IEPA     | USA            | 1.0           | https://www.theice.com/index                                 |
| Toronto Stock Exchange          | XTSE     | Canada         | 1.0           | https://www.tsx.com/                                         |
| BMF Bovespa                     | BVMF     | Brazil         | 1.0           | http://www.b3.com.br/en_us/                                  |
| London Stock Exchange           | XLON     | England        | 1.0           | https://www.londonstockexchange.com/home/homepage.htm        |
| Euronext Amsterdam              | XAMS     | Netherlands    | 1.2           | https://www.euronext.com/en/regulation/amsterdam             |
| Euronext Brussels               | XBRU     | Belgium        | 1.2           | https://www.euronext.com/en/regulation/brussels              |
| Euronext Lisbon                 | XLIS     | Portugal       | 1.2           | https://www.euronext.com/en/regulation/lisbon                |
| Euronext Paris                  | XPAR     | France         | 1.2           | https://www.euronext.com/en/regulation/paris                 |
| Frankfurt Stock Exchange        | XFRA     | Germany        | 1.2           | http://en.boerse-frankfurt.de/                               |
| SIX Swiss Exchange              | XSWX     | Switzerland    | 1.2           | https://www.six-group.com/exchanges/index.html               |
| Tokyo Stock Exchange            | XTKS     | Japan          | 1.2           | https://www.jpx.co.jp/english/                               |
| Austrialian Securities Exchange | XASX     | Australia      | 1.3           | https://www.asx.com.au/                                      |
| Bolsa de Madrid                 | XMAD     | Spain          | 1.3           | http://www.bolsamadrid.es/ing/aspx/Portada/Portada.aspx      |
| Borsa Italiana                  | XMIL     | Italy          | 1.3           | https://www.borsaitaliana.it/homepage/homepage.en.htm        |
| New Zealand Exchange            | XNZE     | New Zealand    | 1.3           | https://www.nzx.com/                                         |
| Wiener Borse                    | XWBO     | Austria        | 1.3           | https://www.wienerborse.at/en/                               |
| Hong Kong Stock Exchange        | XHKG     | Hong Kong      | 1.3           | https://www.hkex.com.hk/?sc_lang=en                          |
| Copenhagen Stock Exchange       | XCSE     | Denmark        | 1.4           | http://www.nasdaqomxnordic.com/                              |
| Helsinki Stock Exchange         | XHEL     | Finland        | 1.4           | http://www.nasdaqomxnordic.com/                              |
| Stockholm Stock Exchange        | XSTO     | Sweden         | 1.4           | http://www.nasdaqomxnordic.com/                              |
| Oslo Stock Exchange             | XOSL     | Norway         | 1.4           | https://www.oslobors.no/ob_eng/                              |
| Irish Stock Exchange            | XDUB     | Ireland        | 1.4           | http://www.ise.ie/                                           |
| Bombay Stock Exchange           | XBOM     | India          | 1.5           | https://www.bseindia.com                                     |
| Singapore Exchange              | XSES     | Singapore      | 1.5           | https://www.sgx.com                                          |
| Shanghai Stock Exchange         | XSHG     | China          | 1.5           | http://english.sse.com.cn                                    |
| Korea Exchange                  | XKRX     | South Korea    | 1.6           | http://global.krx.co.kr                                      |
| Iceland Stock Exchange          | XICE     | Iceland        | 1.7           | http://www.nasdaqomxnordic.com/                              |
| Poland Stock Exchange           | XWAR     | Poland         | 1.9           | http://www.gpw.pl                                            |
| Santiago Stock Exchange         | XSGO     | Chile          | 1.9           | http://inter.bolsadesantiago.com/sitios/en/Paginas/home.aspx |
| Colombia Securities Exchange    | XBOG     | Colombia       | 1.9           | https://www.bvc.com.co/nueva/index_en.html                   |
| Mexican Stock Exchange          | XMEX     | Mexico         | 1.9           | https://www.bmv.com.mx                                       |
| Lima Stock Exchange             | XLIM     | Peru           | 1.9           | https://www.bvl.com.pe                                       |
| Prague Stock Exchange           | XPRA     | Czech Republic | 1.9           | https://www.pse.cz/en/                                       |
| Budapest Stock Exchange         | XBUD     | Hungary        | 1.10          | https://bse.hu/                                              |
| Athens Stock Exchange           | ASEX     | Greece         | 1.10          | http://www.helex.gr/                                         |
| Istanbul Stock Exchange         | XIST     | Turkey         | 1.10          | https://www.borsaistanbul.com/en/                            |
| Johannesburg Stock Exchange     | XJSE     | South Africa   | 1.10          | https://www.jse.co.za/z                                      |
| Malaysia Stock Exchange         | XKLS     | Malaysia       | 1.11          | http://www.bursamalaysia.com/market/                         |
| Moscow Exchange                 | XMOS     | Russia         | 1.11          | https://www.moex.com/en/                                     |
| Philippine Stock Exchange       | XPHS     | Philippines    | 1.11          | https://www.pse.com.ph/stockMarket/home.html                 |
| Stock Exchange of Thailand      | XBKK     | Thailand       | 1.11          | https://www.set.or.th/set/mainpage.do?language=en&country=US |
| Indonesia Stock Exchange        | XIDX     | Indonesia      | 1.11          | https://www.idx.co.id/                                       |
| Taiwan Stock Exchange Corp.     | XTAI     | Taiwan         | 1.11          | https://www.twse.com.tw/en/                                  |
| Buenos Aires Stock Exchange     | XBUE     | Argentina      | 1.11          | https://www.bcba.sba.com.ar/                                 |
| Pakistan Stock Exchange         | XKAR     | Pakistan       | 1.11          | https://www.psx.com.pk/                                      |

> Note that exchange calendars are defined by their [ISO-10383](https://www.iso20022.org/10383/iso-10383-market-identifier-codes) market identifier code.
