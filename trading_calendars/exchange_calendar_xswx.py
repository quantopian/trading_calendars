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
    Easter,
    EasterMonday,
    GoodFriday,
    Holiday,
)
from pandas.tseries.offsets import Day
from pytz import timezone

from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
)

# Regular Holidays
# ----------------
SIXNewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
)

BerchtoldsDay = Holiday(
    "Berchtold's Day",
    month=1,
    day=2,
)

LabourDay = Holiday(
    "Labour Day",
    month=5,
    day=1,
)

AscensionDay = Holiday(
    "Ascension Day",
    month=1,
    day=1,
    offset=[Easter(), Day(39)],
)

WhitMonday = Holiday(
    "Whit Monday",
    month=1,
    day=1,
    offset=[Easter(), Day(50)],
)

SwissNationalDay = Holiday(
    "Swiss National Day",
    month=8,
    day=1
)

ChristmasEve = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
)

Christmas = Holiday(
    "Christmas",
    month=12,
    day=25,
)

BoxingDay = Holiday(
    "Boxing Day",
    month=12,
    day=26,
)

NewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
)


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

    @property
    def name(self):
        return "XSWX"

    @property
    def tz(self):
        return timezone('Europe/Zurich')

    @property
    def open_time(self):
        return time(9, 1)

    @property
    def close_time(self):
        return time(17, 30)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            SIXNewYearsDay,
            BerchtoldsDay,
            EasterMonday,
            GoodFriday,
            LabourDay,
            AscensionDay,
            WhitMonday,
            SwissNationalDay,
            ChristmasEve,
            Christmas,
            BoxingDay,
            NewYearsEve,
        ])
