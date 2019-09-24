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

from datetime import time
from itertools import chain

import pandas as pd
from pandas.tseries.holiday import GoodFriday, Holiday
from pytz import timezone, UTC

from .common_holidays import (
    new_years_day,
    maundy_thursday,
    european_labour_day,
    saint_peter_and_saint_paul_day,
    all_saints_day,
    immaculate_conception,
    christmas,
    new_years_eve,
)
from .trading_calendar import HolidayCalendar, TradingCalendar


####################
# Regular Holidays #
####################
NewYearsDay = new_years_day()

MaundyThursday = maundy_thursday()

LabourDay = european_labour_day()

SaintPeterAndSaintPaulDay = saint_peter_and_saint_paul_day()

IndependenceDay1 = Holiday('Independence Day', month=7, day=28)
IndependenceDay2 = Holiday('Independence Day', month=7, day=29)

SantaRosa = Holiday('Santa Rosa', month=8, day=30)

BattleOfAngamos = Holiday('Battle of Angamos', month=10, day=8)

AllSaintsDay = all_saints_day()

ImmaculateConception = immaculate_conception()

Christmas = christmas()

NewYearsEve = new_years_eve(end_date='2008')


##################
# Adhoc Holidays #
##################
ExchangeHolidays = [
    pd.Timestamp('2009-01-02', tz=UTC),
    pd.Timestamp('2009-07-27', tz=UTC),
    pd.Timestamp('2015-07-27', tz=UTC),
    pd.Timestamp('2015-10-09', tz=UTC),
]

NationalHolidays = [
    pd.Timestamp('2015-01-02', tz=UTC),
]

ASPASummit = [
    pd.Timestamp('2012-10-01', tz=UTC),
    pd.Timestamp('2012-10-02', tz=UTC),
]

APECSummit = [
    pd.Timestamp('2016-11-17', tz=UTC),
    pd.Timestamp('2016-11-18', tz=UTC),
]

EighthSummitOfTheAmericas = [pd.Timestamp('2018-04-13', tz=UTC)]


class XLIMExchangeCalendar(TradingCalendar):
    """
    Calendar for the Lima Stock Exchange (Bolsa de Valores de Lima) in Peru.

    Open Time: 9:00 AM, Peruvian Time
    Close Time: 4:00 PM, Peruvian Time

    Regularly-Observed Holidays:
      - New Year's Day
      - Maundy Thursday
      - Good Friday
      - Labour Day
      - Saint Paul and Saint Peter Day
      - Independence Day
      - Santa Rosa
      - Battle of Angamos
      - All Saints' Day
      - Immaculate Conception
      - Christmas Day

    Holidays No Longer Observed:
      - New Year's Eve

    Early Closes:
      - None
    """
    name = 'XLIM'
    tz = timezone('America/Lima')

    open_times = (
        (None, time(9, 1)),
    )
    close_times = (
        (None, time(16)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            MaundyThursday,
            GoodFriday,
            LabourDay,
            SaintPeterAndSaintPaulDay,
            IndependenceDay1,
            IndependenceDay2,
            SantaRosa,
            BattleOfAngamos,
            AllSaintsDay,
            ImmaculateConception,
            Christmas,
            NewYearsEve,
        ])

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                ExchangeHolidays,
                NationalHolidays,
                ASPASummit,
                APECSummit,
                EighthSummitOfTheAmericas,
            )
        )
