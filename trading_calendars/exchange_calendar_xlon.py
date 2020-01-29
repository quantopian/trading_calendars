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
from pandas import Timestamp
from pandas.tseries.holiday import (
    DateOffset,
    EasterMonday,
    GoodFriday,
    Holiday,
    MO,
    previous_friday,
    weekend_to_monday,
)
from pytz import timezone
from pytz import UTC

from .common_holidays import (
    new_years_day,
    christmas,
    weekend_christmas,
    boxing_day,
    weekend_boxing_day,
)
from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
)

# Regular Holidays
# ----------------
# New Year's Day
LSENewYearsDay = new_years_day(observance=weekend_to_monday)

# Early May bank holiday (was moved in 2020 to align with VE Day).
MayBankBefore2020 = Holiday(
    "Early May Bank Holiday",
    month=5,
    offset=DateOffset(weekday=MO(1)),
    day=1,
    end_date='2020',
)

MayBankAfter2020 = Holiday(
    "Early May Bank Holiday",
    month=5,
    offset=DateOffset(weekday=MO(1)),
    day=1,
    start_date='2021',
)

# Spring bank holiday is the last Monday in May except:
# - in 2002, it was moved to June 3
# - in 2012, it was moved to June 4
SpringBankBefore2002 = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    end_date="2002-01-01",
)
SpringBank2002To2012 = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    start_date="2003-01-01",
    end_date="2012-01-01",
)
SpringBank2013Onwards = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    start_date="2013-01-01",
)
# Summer bank holiday
SummerBank = Holiday(
    "Summer Bank Holiday",
    month=8,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
)

Christmas = christmas()

WeekendChristmas = weekend_christmas()

BoxingDay = boxing_day()

WeekendBoxingDay = weekend_boxing_day()

# Early Closes
# ------------
# If Christmas Eve falls on a weekday, that day is a half day.
# If it falls on a weekend, the preceding Friday is a half day.
ChristmasEve = Holiday(
    'Christmas Eve Early Close',
    month=12,
    day=24,
    observance=previous_friday,
)
# New Year's eve (or the preceding Friday if it falls on a weekend)
# is a half day.
NewYearsEve = Holiday(
    "New Year's Eve Early Close",
    month=12,
    day=31,
    observance=previous_friday,
)

# Ad Hoc Closes
# -------------
SpringBank2002 = Timestamp("2002-06-03", tz=UTC)
GoldenJubilee = Timestamp("2002-06-04", tz=UTC)
RoyalWedding = Timestamp("2011-04-29", tz=UTC)
SpringBank2012 = Timestamp("2012-06-04", tz=UTC)
DiamondJubilee = Timestamp("2012-06-05", tz=UTC)
VEDay2020 = Timestamp("2020-05-08", tz=UTC)


class XLONExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the London Stock Exchange (XLON).

    Open Time: 8:00 AM, GMT
    Close Time: 4:30 PM, GMT

    Regularly-Observed Holidays:
    - New Years Day (observed on first business day on/after)
    - Good Friday
    - Easter Monday
    - Early May Bank Holiday (first Monday in May)
    - Spring Bank Holiday (last Monday in May)
    - Summer Bank Holiday (last Monday in May)
    - Christmas Day
    - Dec. 27th (if Christmas is on a weekend)
    - Boxing Day
    - Dec. 28th (if Boxing Day is on a weekend)

    Early Closes:
    - Christmas Eve
    - New Year's Eve
    """
    regular_early_close = time(12, 30)

    name = 'XLON'

    tz = timezone('Europe/London')

    open_times = (
        (None, time(8, 1)),
    )

    close_times = (
        (None, time(16, 30)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            LSENewYearsDay,
            GoodFriday,
            EasterMonday,
            MayBankBefore2020,
            MayBankAfter2020,
            SpringBankBefore2002,
            SpringBank2002To2012,
            SpringBank2013Onwards,
            SummerBank,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay
        ])

    @property
    def adhoc_holidays(self):
        return [
            SpringBank2002,
            GoldenJubilee,
            RoyalWedding,
            SpringBank2012,
            DiamondJubilee,
            VEDay2020,
        ]

    @property
    def special_closes(self):
        return [
            (self.regular_early_close, HolidayCalendar([
                ChristmasEve,
                NewYearsEve,
            ]))
        ]
