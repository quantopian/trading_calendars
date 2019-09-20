"""
This script can be used to generate the CSV files used in the exchange calendar
tests. The CSVs include a calendar's sessions, open times, and close times.

This script can be run from the root of the repository with:
    $ python etc/make_trading_calendar_test_csv.py <calendar_iso_code>
"""
from os.path import abspath, dirname, join, normpath
import sys

import pandas as pd

from trading_calendars import get_calendar


cal_name = sys.argv[1]
cal = get_calendar(cal_name.upper())

df = pd.DataFrame(
    list(zip(cal.opens, cal.closes)),
    columns=['market_open', 'market_close'],
    index=cal.closes.index,
)
df.index = df.index.date

destination = normpath(
    join(
        abspath(dirname(__file__)),
        '../tests/resources/{}.csv'.format(cal_name.lower()),
    ),
)
print('Writing test CSV file to {}'.format(destination))

df.to_csv(destination)
