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
    previous_friday,
)
from pytz import timezone

from .common_holidays import (
    new_years_day,
    epiphany,
    ascension_day,
    whit_monday,
    corpus_christi,
    european_labour_day,
    assumption_day,
    all_saints_day,
    immaculate_conception,
    christmas_eve,
    christmas,
    new_years_eve,
)
from .trading_calendar import HolidayCalendar, TradingCalendar

NewYearsDay = new_years_day()

Epiphany = epiphany(end_date='2019')

AscensionDay = ascension_day(end_date='2019')
WhitMonday = whit_monday()
CorpusChristi = corpus_christi(end_date='2019')

LabourDay = european_labour_day()

AssumptionDay = assumption_day(end_date='2019')

NationalHoliday = Holiday('National Holiday', month=10, day=26)

AllSaintsDay = all_saints_day(end_date='2019')

ImmaculateConception = immaculate_conception(end_date='2019')

ChristmasEve = christmas_eve()
Christmas = christmas()

SaintStephensDay = Holiday("Saint Stephen's Day", month=12, day=26)

# Prior to 2016, when New Year's Eve fell on the weekend, it was observed
# on the preceding Friday. In 2016 and after, it is not made up.
NewYearsEveThrough2015 = new_years_eve(
    observance=previous_friday,
    end_date='2016',
)
NewYearsEve2016Onwards = new_years_eve(start_date='2016')


class XWBOExchangeCalendar(TradingCalendar):
    """
    Calendar for the Wiener Borse AG exchange in Vienna, Austria.

    Open Time: 9:00 AM, CET (Central European Time)
    Close Time: 5:30 PM, CET (Central European Time)

    Regularly-Observed Holidays:
      - New Year's Day
      - Epiphany
      - Good Friday
      - Easter Monday
      - Ascension Day
      - Whit Monday
      - Corpus Christi
      - Labour Day
      - Assumption Day
      - National Holiday
      - All Saints Day
      - Immaculate Conception
      - Christmas Eve
      - Christmas Day
      - St. Stephen's Day
      - New Year's Eve

    Early Closes:
      - None
    """
    name = 'XWBO'

    tz = timezone('Europe/Vienna')

    open_times = (
        (None, time(9, 1)),
    )

    close_times = (
        (None, time(17, 30)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            Epiphany,
            GoodFriday,
            EasterMonday,
            AscensionDay,
            WhitMonday,
            CorpusChristi,
            LabourDay,
            AssumptionDay,
            NationalHoliday,
            AllSaintsDay,
            ImmaculateConception,
            ChristmasEve,
            Christmas,
            SaintStephensDay,
            NewYearsEveThrough2015,
            NewYearsEve2016Onwards,
        ])
