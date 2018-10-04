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

from dateutil.relativedelta import MO
from pandas import DateOffset
from pandas.tseries.holiday import (
    Holiday,
    GoodFriday,
    EasterMonday,
    previous_friday,
    weekend_to_monday,
)
from pytz import timezone

from .common_holidays import (
    new_years_day,
    anzac_day,
    christmas,
    weekend_christmas,
    boxing_day,
    weekend_boxing_day,
)
from .trading_calendar import HolidayCalendar, TradingCalendar

NewYearsDay = new_years_day(observance=weekend_to_monday)

AustraliaDay = Holiday(
    'Australia Day',
    month=1,
    day=26,
    observance=weekend_to_monday,
)

AnzacDay = anzac_day(observance=weekend_to_monday)

QueensBirthday = Holiday(
    "Queen's Birthday",
    month=6,
    day=1,
    offset=[DateOffset(weekday=MO(2))],
)

LastTradingDayBeforeChristmas = Holiday(
    'Last Trading Day Before Christmas',
    month=12,
    day=24,
    start_date='2010',
    observance=previous_friday,
)
Christmas = christmas()
WeekendChristmas = weekend_christmas()
BoxingDay = boxing_day()
WeekendBoxingDay = weekend_boxing_day()

LastTradingDayOfCalendarYear = Holiday(
    'Last Trading Day Of Calendar Year',
    month=12,
    day=31,
    start_date='2010',
    observance=previous_friday,
)


class XASXExchangeCalendar(TradingCalendar):
    """
    Calendar for the Australian Securities Exchange in Sydney.

    Open Time: 10:00 AM, Australian Eastern Time
    Close Time: 4:00 PM, Australian Eastern Time

    Regularly-Observed Holidays:
      - New Year's Day
      - Australia Day
      - Good Friday
      - Easter Monday
      - Anzac Day
      - Queen's Birthday
      - Christmas Day
      - Boxing Day

    Early Closes:
      - Last trading day before Christmas
      - Last trading day of the calendar year
    """
    regular_early_close = time(14, 10)

    @property
    def name(self):
        return 'XASX'

    @property
    def tz(self):
        return timezone('Australia/Sydney')

    @property
    def open_time(self):
        return time(10, 1)

    @property
    def close_time(self):
        return time(16)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            AustraliaDay,
            GoodFriday,
            EasterMonday,
            AnzacDay,
            QueensBirthday,
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
                    LastTradingDayBeforeChristmas,
                    LastTradingDayOfCalendarYear,
                ]),
            ),
        ]
