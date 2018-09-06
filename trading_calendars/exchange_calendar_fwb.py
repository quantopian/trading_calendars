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
    previous_workday
)
from pandas.tseries.offsets import Day
from pytz import timezone

from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar
)

# Regular Holidays
# ----------------
FWBNewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
)

LabourDay = Holiday(
    "Labour Day",
    month=5,
    day=1
)

WhitMonday = Holiday(
    "Whit Monday",
    month=1,
    day=1,
    offset=[Easter(), Day(50)],
    start_date='2010-01-01'
)

DayOfGermanUnity = Holiday(
    "Day of German Unity",
    month=10,
    day=3,
    start_date='2014-01-01'
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

# Early Closes
# ------------
# The last weekday before Dec 31 is an early close starting in 2010.
LastWorkingDay = Holiday(
    "Last Working Day of Year Early Close",
    month=12,
    day=31,
    start_date='2010-01-01',
    observance=previous_workday,
)


class FWBExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Frankfurt Stock Exchange.

    Open Time: 9:00 AM, CET
    Close Time: 5:30 PM, CET

    Regularly-Observed Holidays:
    - New Years Day
    - Good Friday
    - Easter Monday
    - Whit Monday
    - Labour Day
    - Day of German Unity
    - Christmas Eve
    - Christmas Day
    - Boxing Day

    Early Closes:
    - Last working day before Dec. 31
    """
    # TODO: verify the early close time
    regular_early_close = time(12, 30)

    @property
    def name(self):
        return "FWB"

    @property
    def tz(self):
        return timezone('CET')

    @property
    def open_time(self):
        return time(9, 1)

    @property
    def close_time(self):
        return time(17, 30)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            FWBNewYearsDay,
            GoodFriday,
            EasterMonday,
            LabourDay,
            WhitMonday,
            DayOfGermanUnity,
            ChristmasEve,
            Christmas,
            BoxingDay,
            NewYearsEve,
        ])

    @property
    def special_closes(self):
        return [
            (self.regular_early_close, HolidayCalendar([
                LastWorkingDay,
            ]))
        ]
