# trading_calendars

![CI](https://github.com/quantopian/trading_calendars/workflows/CI/badge.svg)

A Python library of exchange calendars meant to be used with [Zipline](https://github.com/quantopian/zipline).

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

## Installation

``` bash
$ pip install trading-calendars
```

## Usage

``` python
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
