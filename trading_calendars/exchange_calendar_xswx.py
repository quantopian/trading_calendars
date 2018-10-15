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
    EasterMonday,
    GoodFriday,
    Holiday,
)
from pytz import timezone

from .common_holidays import (
    new_years_day,
    european_labour_day,
    ascension_day,
    whit_monday,
    christmas_eve,
    christmas,
    boxing_day,
    new_years_eve,
)
from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
)

# Regular Holidays
# ----------------
NewYearsDay = new_years_day()

BerchtoldsDay = Holiday(
    "Berchtold's Day",
    month=1,
    day=2,
)

EuropeanLabourDay = european_labour_day()

AscensionDay = ascension_day()

WhitMonday = whit_monday()

SwissNationalDay = Holiday(
    "Swiss National Day",
    month=8,
    day=1
)

ChristmasEve = christmas_eve()

Christmas = christmas()

BoxingDay = boxing_day()

NewYearsEve = new_years_eve()


class XSWXExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Swiss Exchange (XSWX)

    Open Time: 8:00 AM, CET, CEST in summer
    Close Time: 5:30 PM, CET, CEST in summer

    Regularly-Observed Holidays:
    - New Year's Day
    - Berchtold's Day
    - Good Friday
    - Easter Monday
    - Labour Day
    - Ascension Day
    - Whit Monday
    - Swiss National Day
    - Christmas Eve
    - Christmas Day
    - Boxing Day
    - New Year's Eve
    """

    name = 'XSWX'

    tz = timezone('Europe/Zurich')

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
            BerchtoldsDay,
            EasterMonday,
            GoodFriday,
            EuropeanLabourDay,
            AscensionDay,
            WhitMonday,
            SwissNationalDay,
            ChristmasEve,
            Christmas,
            BoxingDay,
            NewYearsEve,
        ])
