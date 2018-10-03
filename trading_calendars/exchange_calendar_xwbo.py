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

from pandas.tseries.holiday import Holiday, GoodFriday, EasterMonday
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

Epiphany = epiphany()

AscensionDay = ascension_day()
WhitMonday = whit_monday()
CorpusChristi = corpus_christi()

LabourDay = european_labour_day()

AssumptionDay = assumption_day()

NationalHoliday = Holiday('National Holiday', month=10, day=26)

AllSaintsDay = all_saints_day()

ImmaculateConception = immaculate_conception()

ChristmasEve = christmas_eve()
Christmas = christmas()

SaintStephensDay = Holiday("Saint Stephen's Day", month=12, day=26)

NewYearsEve = new_years_eve()


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
    @property
    def name(self):
        return 'XWBO'

    @property
    def tz(self):
        return timezone('Europe/Vienna')

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
            NewYearsEve,
        ])
