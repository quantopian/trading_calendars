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
    DateOffset,
    EasterMonday,
    GoodFriday,
    Holiday,
    MO,
    previous_workday,
    weekend_to_monday,
)
from pytz import timezone

from .common_holidays import (
    new_years_day,
    christmas,
    weekend_christmas,
    boxing_day,
    weekend_boxing_day,
)

from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar
)

# Regular Holidays
# ----------------
NewYearsDay = new_years_day()

DayAfterNewYearsDay = Holiday(
    "Day after New Year's Day",
    month=1,
    day=2,
)

WaitangiDay = Holiday(
    "Waitangi Day",
    month=2,
    day=6,
    observance=weekend_to_monday,
)

AnzacDay = Holiday(
    "Anzac Day",
    month=4,
    day=25,
    observance=weekend_to_monday,
)

QueensBirthday = Holiday(
    "Queen's Birthday",
    month=6,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)

LabourDay = Holiday(
    "Labour Day",
    month=10,
    day=1,
    offset=DateOffset(weekday=MO(4)),
)

Christmas = christmas()

WeekendChristmas = weekend_christmas()

BoxingDay = boxing_day()

WeekendBoxingDay = weekend_boxing_day()


# Early Closes
# ------------
BusinessDayPriorToChristmasDay = Holiday(
    "Business Day prior to Christmas Day",
    month=12,
    day=25,
    observance=previous_workday,
    start_date="2011-01-01",
)

BusinessDayPriorToNewYearsDay = Holiday(
    "Business Day prior to New Year's Day",
    month=1,
    day=1,
    observance=previous_workday,
    start_date="2011-01-01",
)


class XNZEExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the New Zealand Exchange (NZX).

    Open Time: 10:00 AM, NZ
    Close Time: 4:45 PM, NZ

    Regularly-Observed Holidays:
    - New Year's Day
    - Day after New Year's Day
    - Waitangi Day
    - Anzac Day
    - Queen's Birthday
    - Labour Day
    - Christmas
    - Boxing Day

    Early Closes:
    - Business Day prior to Christmas Day
    - Business Day prior to New Year's Day
    """
    regular_early_close = time(12, 45)

    @property
    def name(self):
        return "XNZE"

    @property
    def tz(self):
        return timezone('NZ')

    @property
    def open_time(self):
        return time(10, 1)

    @property
    def close_time(self):
        return time(16, 45)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            DayAfterNewYearsDay,
            WaitangiDay,
            GoodFriday,
            EasterMonday,
            QueensBirthday,
            LabourDay,
            AnzacDay,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay,
        ])

    @property
    def special_closes(self):
        return [
            (
                self.regular_early_close,
                HolidayCalendar([
                    BusinessDayPriorToChristmasDay,
                    BusinessDayPriorToNewYearsDay
                ])
            )
        ]
