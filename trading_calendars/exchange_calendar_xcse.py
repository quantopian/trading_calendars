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
    Easter,
    EasterMonday,
)
from pandas.tseries.offsets import Day
from pytz import timezone

from .common_holidays import (
    new_years_day,
    maundy_thursday,
    ascension_day,
    whit_monday,
    christmas_eve,
    christmas,
    boxing_day,
    new_years_eve,
)
from .trading_calendar import HolidayCalendar, TradingCalendar

NewYearsDay = new_years_day()

MaundyThursday = maundy_thursday()
GeneralPrayerDay = Holiday(
    'General Prayer Day',
    month=1,
    day=1,
    offset=[Easter(), Day(26)],
)
AscensionDay = ascension_day()
BankHoliday = Holiday(
    'Bank Holiday',
    month=1,
    day=1,
    offset=[Easter(), Day(40)],
    start_date='2009',
)
WhitMonday = whit_monday()

ConstitutionDay = Holiday('Constitution Day', month=6, day=5)

ChristmasEve = christmas_eve()
Christmas = christmas()
BoxingDay = boxing_day()

NewYearsEve = new_years_eve()


class XCSEExchangeCalendar(TradingCalendar):
    """
    Calendar for the Copenhagen Stock Exchange in Denmark.

    Open Time: 9:00 AM, CET (Central European Time)
    Close Time: 5:00 PM, CET (Central European Time)

    Regularly-Observed Holidays:
      - New Year's Day
      - Maundy Thursday
      - Good Friday
      - Easter Monday
      - General Prayer Day
      - Ascension Day
      - Bank Holiday
      - Whit Monday
      - Constitution Day
      - Christmas Eve
      - Christmas Day
      - Boxing Day
      - New Year's Eve

    Early Closes:
      - None
    """
    name = 'XCSE'
    tz = timezone('Europe/Copenhagen')
    open_times = (
        (None, time(9, 1)),
    )
    close_times = (
        (None, time(17)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsDay,
            MaundyThursday,
            GoodFriday,
            EasterMonday,
            GeneralPrayerDay,
            AscensionDay,
            BankHoliday,
            WhitMonday,
            ConstitutionDay,
            ChristmasEve,
            Christmas,
            BoxingDay,
            NewYearsEve,
        ])
