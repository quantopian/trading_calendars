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
    EasterMonday
)
from pytz import timezone
from .common_holidays import (
    new_years_day,
    european_labour_day,
    corpus_christi,
    all_saints_day,
    boxing_day,
    christmas,
    christmas_eve,
    new_years_eve
)
from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar
)

May3ConstitutionDay = Holiday(
    "Celabration of declaration of the Constitution of 3 May",
    month=5,
    day=3
)
ArmedForcesDay = Holiday(
    "Armed Forces Day",
    month=8,
    day=15
)
IndependenceDay = Holiday(
    "National Independence Day",
    month=11,
    day=11
)


class XWARExchangeCalendar(TradingCalendar):
    """
        Exchange calendar for the Warsaw Stock Exchange (WSE).

        Open Time: 9:00 AM, CET
        Close Time: 5:30 PM, CET

        Regularly-Observed Holidays:
        - New Years Day
        - Good Friday
        - Easter Monday
        - Labour Day
        - May 3 Constitution Day
        - Corpus Christi
        - Armed Forces Day
        - All Saints Day
        - Independence Day
        - Christmas Eve
        - Christmas Day
        - Boxing Day
        - New Years Eve
        """
    name = 'XWAR'

    tz = timezone('CET')

    open_times = (
        (None, time(8, 30)),
    )

    close_times = (
        (None, time(17, 5)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            new_years_day,
            GoodFriday,
            EasterMonday,
            european_labour_day,
            May3ConstitutionDay,
            corpus_christi,
            ArmedForcesDay,
            all_saints_day,
            IndependenceDay,
            boxing_day,
            christmas,
            christmas_eve,
            new_years_eve
        ])
