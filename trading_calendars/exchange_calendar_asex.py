#
# Copyright 2019 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import time, timedelta
from dateutil.easter import easter, EASTER_ORTHODOX
from itertools import chain
import pandas as pd
from pandas.tseries.holiday import (
    EasterMonday,
    GoodFriday,
    Holiday,
)
from pytz import timezone, UTC

from .common_holidays import (
    assumption_day,
    christmas,
    christmas_eve,
    epiphany,
    european_labour_day,
    new_years_day,
)
from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
)


def orthodox_easter(start_date='1980', end_date='2021'):
    """
    ASEX observes Orthodox Easter, and has many holidays
    that are relative to Orthodox Easter.  This function gives a
    DatetimeIndex of Orthodox Easter dates from start_date to end_date
    """
    return pd.to_datetime([
        easter(year, method=EASTER_ORTHODOX)
        for year in range(int(start_date), int(end_date))
    ]).tz_localize(UTC)


NewYearsDay = new_years_day()

Epiphany = epiphany()

OrthodoxAshMonday = orthodox_easter() - timedelta(48)

NationalHoliday1 = Holiday(
    'National Holiday 1',
    month=3,
    day=25,
)

OrthodoxGoodFriday = orthodox_easter() - timedelta(2)

OrthodoxEasterMonday = orthodox_easter() + timedelta(1)

LabourDay = european_labour_day()

OrthodoxWhitMonday = orthodox_easter() + timedelta(50)

AssumptionDay = assumption_day()

NationalHoliday2 = Holiday(
    'National Holiday 2',
    month=10,
    day=28,
)

ChristmasEve = christmas_eve(start_date='2009')

ChristmasDay = christmas()

SecondDayOfChristmas = Holiday(
    'Second Day of Christmas',
    month=12,
    day=26,
)


class ASEXExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Athens Stock Exchange (ASEX).

    Open Time: 10:00 AM, EEST
    Close Time: 5:00 PM, EEST (until 2008-09-29)
                5:20 PM, EEST (starting 2008-09-29)

    Regularly-Observed Holidays:
    - New Year's Day
    - Epiphany (Jan 6)
    - Orthodox Ash Monday (48 days before Orthodox Easter Sunday)
    - National Holiday (Mar 25)
    - Good Friday
    - Easter Monday
    - Orthodox Good Friday
    - Orthodox Easter Monday
    - Labour Day (May 1)
    - Orthodox Whit Monday (50 days after Orthodox Easter Sunday)
    - Assumption Day (Aug 15)
    - National Holiday (Oct 28)
    - Christmas Eve
    - Christmas Day
    - Second Day of Christmas (Dec 26)

    Early Closes:
    - None
    """
    name = 'ASEX'

    tz = timezone('Europe/Athens')

    open_times = (
        (None, time(10, 1)),
    )

    close_times = (
        (None, time(17, 00)),
        (pd.Timestamp('2008-09-29'), time(17, 20))
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            Epiphany,
            NationalHoliday1,
            GoodFriday,
            EasterMonday,
            LabourDay,
            AssumptionDay,
            NationalHoliday2,
            ChristmasEve,
            ChristmasDay,
            SecondDayOfChristmas
        ])

    @property
    def adhoc_holidays(self):
        debt_crisis = pd.date_range('2015-06-29', '2015-07-31', freq='B')

        debt_crisis_holidays = [
            pd.Timestamp(str(date), tz=UTC) for date in debt_crisis
        ]

        misc_adhoc_holidays = [
            # In 2002, market closed for unknown reason
            pd.Timestamp('2002-05-07', tz=UTC),
            # In 2004, Assumption Day fell on a sunday, observed on a Friday
            pd.Timestamp('2004-08-13', tz=UTC),
            # In 2008, worker strikes closed the market for 2 days in March
            pd.Timestamp('2008-03-04', tz=UTC),
            pd.Timestamp('2008-03-05', tz=UTC),
            # In 2013, May Day strikes closed the market
            pd.Timestamp('2013-05-07', tz=UTC),
            # In 2014, New Year's Eve was observed as a holiday
            pd.Timestamp('2014-12-31', tz=UTC),
            # In 2016, Labour Day fell on a Sunday, observed on Tuesday
            pd.Timestamp('2016-05-03', tz=UTC),
        ]

        return list(chain(
            debt_crisis_holidays,
            misc_adhoc_holidays,
            # TODO: Investigate making orthodox easter adhocs actual holidays
            OrthodoxGoodFriday,
            OrthodoxEasterMonday,
            OrthodoxWhitMonday,
            OrthodoxAshMonday,
        ))
