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
from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import (
    Holiday,
    GoodFriday,
    EasterMonday,
    previous_friday,
    sunday_to_monday,
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

# Anzac Day was observed on Monday when it fell on a Sunday in
# 2010 but that does not appear to have been the case previously.
# We'll assume that this will be the behavior from now on.
AnzacDayNonMondayized = anzac_day(end_date='2010')
AnzacDay = anzac_day(observance=sunday_to_monday, start_date='2010')

# When Easter Monday and Anzac Day coincided in 2011, Easter Tuesday was
# also observed as a public holiday. Note that this isn't defined as a
# rule, because it will happen next in 2095 (and then in  2163), and
# there isn't a great way to tell how this will be handled at that point.
EasterTuesday2011AdHoc = Timestamp('2011-04-26', tz='UTC')

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

    name = 'XASX'

    tz = timezone('Australia/Sydney')

    open_times = (
        (None, time(10, 1)),
    )

    close_times = (
        (None, time(16)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            AustraliaDay,
            GoodFriday,
            EasterMonday,
            AnzacDayNonMondayized,
            AnzacDay,
            QueensBirthday,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay,
        ])

    @property
    def adhoc_holidays(self):
        return [EasterTuesday2011AdHoc]

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
