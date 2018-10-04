#
# Copyright 2018 Quantopian, Inc.
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

from datetime import time

from pandas.tseries.holiday import (
    Holiday,
    GoodFriday,
    EasterMonday,
    weekend_to_monday,
)
from pytz import timezone

from .common_holidays import (
    new_years_day,
    european_labour_day,
    christmas_eve,
    christmas,
    boxing_day,
    new_years_eve,
)
from .trading_calendar import HolidayCalendar, TradingCalendar

NewYearsDay = new_years_day()

Epiphany = Holiday(
    'Epiphany',
    month=1,
    day=6,
    end_date='2007',
)

LabourDay = european_labour_day()

AssumptionDay = Holiday(
    'Assumption Day',
    month=8,
    day=15,
    end_date='2005',
    observance=weekend_to_monday,
)

NationalDay = Holiday(
    'National Day',
    month=10,
    day=12,
    end_date='2005',
)

AllSaintsDay = Holiday(
    'All Saints Day',
    month=11,
    day=1,
    end_date='2005',
)

ConstitutionDay = Holiday(
    'Constitution Day',
    month=12,
    day=6,
    end_date='2005',
)

ImmaculateConception = Holiday(
    'Immaculate Conception',
    month=12,
    day=8,
    end_date='2005',
)

ChristmasEve = christmas_eve(end_date='2005')
Christmas = christmas()
BoxingDay = boxing_day()

NewYearsEve = new_years_eve(end_date='2005')


class XMADExchangeCalendar(TradingCalendar):
    """
    Calendar for the Madrid Stock Exchange (Bolsa de Madrid).

    Open Time: 9:00 AM, CET (Central European Time)
    Close Time: 5:30 PM, CET (Central European Time)

    Regularly-Observed Holidays:
      - New Year's Day
      - Good Friday
      - Easter Monday
      - Labour Day
      - Christmas Day
      - Boxing Day

    Holidays No Longer Observed:
      - Epiphany (until 2006, inclusive)
      - Assumption Day (until 2004, inclusive)
      - National Day (until 2004, inclusive)
      - All Saints Day (until 2004, inclusive)
      - Constitution Day (until 2004, inclusive)
      - Immaculate Conception (until 2004, inclusive)
      - Christmas Eve (until 2004, inclusive)
      - New Year's Eve (until 2004, inclusive)

    Early Closes:
      - None
    """
    @property
    def name(self):
        return 'XMAD'

    @property
    def tz(self):
        return timezone('Europe/Madrid')

    @property
    def open_time(self):
        return time(9, 1)

    @property
    def close_time(self):
        return time(17, 30)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            Epiphany,
            GoodFriday,
            EasterMonday,
            LabourDay,
            AssumptionDay,
            NationalDay,
            AllSaintsDay,
            ConstitutionDay,
            ImmaculateConception,
            ChristmasEve,
            Christmas,
            BoxingDay,
            NewYearsEve,
        ])
