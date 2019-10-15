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

from datetime import time, timedelta
from itertools import chain

import numpy as np
import pandas as pd
from pandas.tseries.holiday import (
    EasterMonday,
    GoodFriday,
    Holiday,
    sunday_to_monday,
)
from pytz import timezone
import toolz

from .trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY,
)
from .common_holidays import (
    boxing_day,
    chinese_buddhas_birthday_dates,
    chinese_lunar_new_year_dates,
    christmas,
    christmas_eve,
    mid_autumn_festival_dates,
    double_ninth_festival_dates,
    dragon_boat_festival_dates,
    chinese_national_day,
    new_years_day,
    new_years_eve,
    qingming_festival_dates,
    weekend_christmas,
)
from .utils.pandas_utils import vectorized_sunday_to_monday

# Useful resources for making changes to this file:
# # /etc/lunisolar
# http://www.math.nus.edu.sg/aslaksen/calendar/cal.pdf
# https://www.hko.gov.hk/gts/time/calendarinfo.htm
#   - the almanacs on this page are also useful

weekdays = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY)


labor_day = Holiday(
    'Labor Day',
    month=5,
    day=1,
    observance=sunday_to_monday,
)

establishment_day = Holiday(
    'Hong Kong Special Administrative Region Establishment Day',
    month=7,
    day=1,
    observance=sunday_to_monday,
)

day_after_mid_autumn_festival_dates = mid_autumn_festival_dates + timedelta(1)


def boxing_day_obs(dt):
    if dt.weekday in (MONDAY, TUESDAY):
        return dt + pd.Timedelta(days=1)
    return dt


class XHKGExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Hong Kong Stock Exchange (XHKG).

    Open Time: 9:31 AM, Asia/Hong_Kong
    Close Time: 4:00 PM, Asia/Hong_Kong

    Regularly-Observed Holidays:
    - New Years Day (observed on monday when Jan 1 is a Sunday)
    - Lunar New Year and the following 2 days. If the 3rd day of the lunar year
      is a Sunday, then the next Monday is a holiday.
    - Ching Ming Festival
    - Good Friday
    - Easter Monday
    - Buddhas Birthday
    - Dragon Boat Festival
    - Chinese National Day (observed on monday when Oct 1 is a Sunday)
    - Day Following Mid-Autumn Festival
    - Chung Yeung Festival
    - Christmas (observed on nearest weekday to December 25)
    - Day after Christmas is observed

    Regularly-Observed Early Closes:
    - Lunar New Year's Eve
    - Christmas Eve
    - New Year's Eve


    Additional Irregularities:
    - Closes frequently for severe weather.
    """
    name = 'XHKG'
    tz = timezone('Asia/Hong_Kong')

    open_times = (
        (None, time(10, 1)),
        (pd.Timestamp('2011-03-07'), time(9, 31)),
    )
    close_times = (
        (None, time(16)),
    )
    regular_early_close_times = (
        (None, time(12, 30)),
        (pd.Timestamp('2011-03-07'), time(12, 00)),
    )

    def __init__(self, *args, **kwargs):
        super(XHKGExchangeCalendar, self).__init__(*args, **kwargs)

        lunisolar_holidays = (
            chinese_buddhas_birthday_dates,
            chinese_lunar_new_year_dates,
            day_after_mid_autumn_festival_dates,
            double_ninth_festival_dates,
            dragon_boat_festival_dates,
            qingming_festival_dates,
        )
        earliest_precomputed_year = max(map(np.min, lunisolar_holidays)).year
        if earliest_precomputed_year > self.first_trading_session.year:
            raise ValueError(
                'the lunisolar holidays have only been computed back to {},'
                ' cannot instantiate the XHKG calendar back to {}'.format(
                    earliest_precomputed_year,
                    self.first_trading_session.year,
                ),
            )

        latest_precomputed_year = min(map(np.max, lunisolar_holidays)).year
        if latest_precomputed_year < self.last_trading_session.year:
            raise ValueError(
                'the lunisolar holidays have only been computed through {},'
                ' cannot instantiate the XHKG calendar in {}'.format(
                    latest_precomputed_year,
                    self.last_trading_session.year,
                ),
            )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            new_years_day(observance=sunday_to_monday),
            GoodFriday,
            EasterMonday,
            labor_day,
            establishment_day,
            chinese_national_day(observance=sunday_to_monday),
            christmas(),
            weekend_christmas(),
            boxing_day(observance=boxing_day_obs)
        ])

    @property
    def adhoc_holidays(self):
        lunar_new_years_eve = (
            chinese_lunar_new_year_dates - pd.Timedelta(days=1)
        )[
            (chinese_lunar_new_year_dates.weekday == SATURDAY) &
            (chinese_lunar_new_year_dates.year < 2013)
        ]

        lunar_new_year_2 = chinese_lunar_new_year_dates + pd.Timedelta(days=1)
        lunar_new_year_3 = chinese_lunar_new_year_dates + pd.Timedelta(days=2)
        lunar_new_year_4 = (
            chinese_lunar_new_year_dates + pd.Timedelta(days=3)
        )[
            # According to the new arrangement under the General Holidays and
            # Employment Legislation (Substitution of Holidays)(Amendment)
            # Ordinance 2011, when either Lunar New Year's Day, the second day
            # of Lunar New Year or the third day of Lunar New Year falls on a
            # Sunday, the fourth day of Lunar New Year is designated as a
            # statutory and general holiday in substitution.
            (
                (chinese_lunar_new_year_dates.weekday == SUNDAY) |
                (lunar_new_year_2.weekday == SUNDAY) |
                (lunar_new_year_3.weekday == SUNDAY)
            ) &
            (chinese_lunar_new_year_dates.year >= 2013)
        ]

        qingming_festival = vectorized_sunday_to_monday(
            qingming_festival_dates,
        ).values
        years = qingming_festival.astype('M8[Y]')
        easter_monday = EasterMonday.dates(years[0], years[-1] + 1)
        # qingming gets observed one day later if easter monday is on the same
        # day
        qingming_festival[qingming_festival == easter_monday] += (
            np.timedelta64(1, 'D')
        )

        # if the day after the mid autumn festival is October first, which
        # conflicts with national day, then national day is observed on the
        # second, though we don't encode that in the regular holiday, so
        # instead we pretend that the mid autumn festival would be delayed.
        mid_autumn_festival = day_after_mid_autumn_festival_dates.values
        mid_autumn_festival[
            (day_after_mid_autumn_festival_dates.month == 10) &
            (day_after_mid_autumn_festival_dates.day == 1)
        ] += np.timedelta64(1, 'D')

        return list(chain(
            lunar_new_years_eve,
            chinese_lunar_new_year_dates,
            lunar_new_year_2,
            lunar_new_year_3,
            lunar_new_year_4,

            qingming_festival,
            vectorized_sunday_to_monday(chinese_buddhas_birthday_dates),
            vectorized_sunday_to_monday(dragon_boat_festival_dates),
            mid_autumn_festival,
            vectorized_sunday_to_monday(double_ninth_festival_dates),

            # severe weather closure (typhoons)
            [
                '2008-08-06',
                '2008-08-22',
                '2011-09-29',
                '2013-08-14',
                '2016-08-02',
                '2016-10-21',
                '2017-08-23',
            ],

            # special holiday:
            # https://www.info.gov.hk/gia/general/201507/09/P201507080716.htm
            ['2015-09-03'],
        ))

    @property
    def special_closes(self):
        return [
            (
                time,
                HolidayCalendar([
                    new_years_eve(
                        start_date=start,
                        end_date=end,
                        days_of_week=weekdays,
                    ),
                    christmas_eve(
                        start_date=start,
                        end_date=end,
                        days_of_week=weekdays
                    ),
                ]),
            )
            for (start, time), (end, _) in toolz.sliding_window(
                2,
                toolz.concatv(self.regular_early_close_times, [(None, None)]),
            )
        ]

    @property
    def special_closes_adhoc(self):
        lunar_new_years_eve = (
            chinese_lunar_new_year_dates - pd.Timedelta(days=1)
        )[
            np.in1d(
                chinese_lunar_new_year_dates.weekday,
                [TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY],
            ) & (chinese_lunar_new_year_dates.year >= 2013)
        ].values

        def selection(arr, start, end):
            predicates = []
            if start is not None:
                predicates.append(start.asm8 <= arr)
            if end is not None:
                predicates.append(arr < end.asm8)

            if not predicates:
                return arr

            return arr[np.all(predicates, axis=0)]

        return [
            (time, selection(lunar_new_years_eve, start, end))
            for (start, time), (end, _) in toolz.sliding_window(
                2,
                toolz.concatv(self.regular_early_close_times, [(None, None)]),
            )
        ]
