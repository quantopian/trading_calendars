# -*- coding: utf-8 -*-
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
from pandas.tseries.offsets import (
    LastWeekOfMonth,
    WeekOfMonth,
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
    christmas,
    christmas_eve,
    new_years_day,
    new_years_eve,
    weekend_christmas,
)
from .lunisolar_holidays import (
    chinese_buddhas_birthday_dates,
    chinese_lunar_new_year_dates,
    mid_autumn_festival_dates,
    double_ninth_festival_dates,
    dragon_boat_festival_dates,
    qingming_festival_dates
)
from .utils.pandas_utils import vectorized_sunday_to_monday

# Useful resources for making changes to this file:
# # /etc/lunisolar
# http://www.math.nus.edu.sg/aslaksen/calendar/cal.pdf
# https://www.hko.gov.hk/gts/time/calendarinfo.htm
#   - the almanacs on this page are also useful

weekdays = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY)


def process_queen_birthday(dt):
    # before 1983
    if dt.year in [1974, 1981]:
        return dt + pd.DateOffset(weekday=6)
    elif dt.year < 1983:
        return sunday_to_monday(dt)
    # after 1983
    wom = WeekOfMonth(week=2, weekday=0)
    if dt.year in [1983, 1988, 1993, 1994]:
        wom = WeekOfMonth(week=1, weekday=0)
    if dt.year in [1985]:
        wom = WeekOfMonth(week=3, weekday=0)
    return dt + wom


LabourDay = Holiday(
    name="Labour Day",  # 劳动节
    month=5,
    day=1,
    observance=sunday_to_monday,
    start_date=pd.Timestamp('1999-05-01')
)

HKRegionEstablishmentDay = Holiday(
    name="Hong Kong Special Region Establishment Day",
    month=7,
    day=1,
    observance=sunday_to_monday,
    start_date=pd.Timestamp('1997-07-01')
)

NationalDay = Holiday(
    name="National Day",
    month=10,
    day=1,
    observance=sunday_to_monday,
    start_date=pd.Timestamp('1997-07-01')
)

QueenBirthday = Holiday(
    name="Queen's Birthday",  # 英女王生日 6月
    month=6,
    day=10,
    observance=process_queen_birthday,
    start_date=pd.Timestamp('1983-01-01'),
    end_date=pd.Timestamp('1997-06-01')
)

QueenBirthday2 = Holiday(
    name="Queen's Birthday",  # 英女王生日 4月
    month=4,
    day=21,
    observance=process_queen_birthday,
    start_date=pd.Timestamp('1926-04-21'),
    end_date=pd.Timestamp('1983-01-01')
)

CommemoratingAlliedVictory = Holiday(
    name="Commemorating the allied victory",  # 重光纪念日 8月最后一个星期一
    month=8,
    day=20,
    offset=LastWeekOfMonth(weekday=0),
    start_date=pd.Timestamp('1945-08-30'),
    end_date=pd.Timestamp('1997-07-01')
)

IDontKnow = Holiday(
    name="I dont know these days, please tell me",  # 8月第一个星期一
    month=7,
    day=31,
    offset=WeekOfMonth(week=0, weekday=0),
    start_date=pd.Timestamp('1960-08-01'),
    end_date=pd.Timestamp('1983-01-01')
)


day_after_mid_autumn_festival_dates = mid_autumn_festival_dates + timedelta(1)

HKAdhocClosures = [
    # I dont know these days
    pd.Timestamp('1970-07-01', tz='UTC'),
    pd.Timestamp('1971-07-01', tz='UTC'),
    pd.Timestamp('1973-07-02', tz='UTC'),
    pd.Timestamp('1974-07-01', tz='UTC'),
    pd.Timestamp('1975-07-01', tz='UTC'),
    pd.Timestamp('1976-07-01', tz='UTC'),
    pd.Timestamp('1977-07-01', tz='UTC'),
    pd.Timestamp('1979-07-02', tz='UTC'),
    pd.Timestamp('1980-07-01', tz='UTC'),
    pd.Timestamp('1981-07-01', tz='UTC'),
    pd.Timestamp('1982-07-01', tz='UTC'),
    pd.Timestamp('1971-03-22', tz='UTC'),
    pd.Timestamp('1971-12-06', tz='UTC'),
    pd.Timestamp('1971-12-20', tz='UTC'),
    pd.Timestamp('1975-07-28', tz='UTC'),
    pd.Timestamp('1985-07-29', tz='UTC'),

    # Weather related closures
    pd.Timestamp('1970-07-16', tz='UTC'),  # 台风Ruby7003
    pd.Timestamp('1970-09-14', tz='UTC'),  # 台风Georgia7011
    pd.Timestamp('1971-07-22', tz='UTC'),  # 台风Lucy7114
    pd.Timestamp('1971-08-31', tz='UTC'),  # 重光纪念日?
    pd.Timestamp('1973-04-16', tz='UTC'),  # 股灾休市?
    pd.Timestamp('1973-07-17', tz='UTC'),  # 台风Dot7304
    pd.Timestamp('1974-04-25', tz='UTC'),  # 英国女王生日
    pd.Timestamp('1975-10-14', tz='UTC'),  # 台风Elsie7514
    pd.Timestamp('1978-07-26', tz='UTC'),  # 台风Agnes7807
    pd.Timestamp('1978-07-27', tz='UTC'),
    pd.Timestamp('1979-01-26', tz='UTC'),  # 春节补假
    pd.Timestamp('1979-08-02', tz='UTC'),  # 台风Hope7908
    pd.Timestamp('1980-05-21', tz='UTC'),  # 台风Georgia8004
    pd.Timestamp('1980-07-22', tz='UTC'),  # 台风Joy8007
    pd.Timestamp('1981-04-27', tz='UTC'),  # 英国女王生日
    pd.Timestamp('1981-07-06', tz='UTC'),  # 台风Lynn8106
    pd.Timestamp('1981-07-07', tz='UTC'),
    pd.Timestamp('1981-07-29', tz='UTC'),  # 查理斯王子与戴安娜婚礼
    pd.Timestamp('1983-09-09', tz='UTC'),  # 台风Ellen8309
    pd.Timestamp('1985-06-24', tz='UTC'),  # 台风Hal8504
    pd.Timestamp('1986-04-01', tz='UTC'),  # 复活节星期一翌日
    pd.Timestamp('1986-10-22', tz='UTC'),  # 英女王伊丽莎白二世访港
    pd.Timestamp('1987-10-20', tz='UTC'),  # 黑色星期一后,休市4天
    pd.Timestamp('1987-10-21', tz='UTC'),
    pd.Timestamp('1987-10-22', tz='UTC'),
    pd.Timestamp('1987-10-23', tz='UTC'),
    pd.Timestamp('1988-04-05', tz='UTC'),  # 清明节翌日
    # Timestamp('1988-06-13', tz='UTC'),  # 英国女王生日
    pd.Timestamp('1991-06-18', tz='UTC'),  # 英国女王生日翌日
    pd.Timestamp('1992-07-22', tz='UTC'),  # 台风Cary9207
    # pd.Timestamp('1993-06-14', tz='UTC'),  # 英国女王生日
    pd.Timestamp('1993-09-17', tz='UTC'),  # 台风Becky9316
    pd.Timestamp('1994-06-14', tz='UTC'),  # 英国女王生日翌日,端午节翌日
    pd.Timestamp('1997-06-30', tz='UTC'),  # 英国女王生日
    pd.Timestamp('1997-07-02', tz='UTC'),  # 香港回归纪念日翌日
    pd.Timestamp('1997-08-18', tz='UTC'),  # 抗战胜利纪念日
    pd.Timestamp('1997-10-02', tz='UTC'),  # 国庆节翌日
    pd.Timestamp('1998-08-17', tz='UTC'),  # 抗战胜利纪念日
    pd.Timestamp('1998-10-02', tz='UTC'),  # 国庆节翌日
    pd.Timestamp('1999-04-06', tz='UTC'),  # 清明节翌日
    pd.Timestamp('1999-09-16', tz='UTC'),  # 台风约克
    pd.Timestamp('1999-12-31', tz='UTC'),  # 千年虫
    pd.Timestamp('2001-07-06', tz='UTC'),  # 台风尤特0104
    pd.Timestamp('2001-07-25', tz='UTC'),  # 台风玉兔0107
    # pd.Timestamp(2008-06-25', tz='UTC'),  # 台风风神0806,上午休市
    pd.Timestamp('2008-08-06', tz='UTC'),  # 台风北冕0809
    pd.Timestamp('2008-08-22', tz='UTC'),  # 台风鹦鹉0810
    # pd.Timestamp(2009-09-15', tz='UTC'),  # 台风巨爵0915,上午休市
    pd.Timestamp('2010-04-06', tz='UTC'),  # 清明节翌日
    pd.Timestamp('2011-09-29', tz='UTC'),  # 台风纳沙1117
    # pd.Timestamp(2012-07-24', tz='UTC'),  # 台风韦森特1208,上午休市
    pd.Timestamp('2012-10-02', tz='UTC'),  # 中秋节补假
    # pd.Timestamp(2013-05-22', tz='UTC'),  # 暴雨,上午休市
    pd.Timestamp('2013-08-14', tz='UTC'),  # 台风尤特1311
    # pd.Timestamp(2013-09-23', tz='UTC'),  # 台风天兔1319,上午休市
    # pd.Timestamp(2014-09-16', tz='UTC'),  # 台风海鸥1415,上午休市
    pd.Timestamp('2015-04-07', tz='UTC'),  # 复活节+清明节补假
    # pd.Timestamp(2015-07-09', tz='UTC'),  # 台风莲花1520,期货夜盘休市
    pd.Timestamp('2015-09-03', tz='UTC'),  # 抗战70周年纪念
    # pd.Timestamp(2016-08-01', tz='UTC'),  # 台风妮妲1604,期货夜盘20:55收市
    pd.Timestamp('2016-08-02', tz='UTC'),  # 台风妮妲1604
    pd.Timestamp('2016-10-21', tz='UTC'),  # 台风海马1622
    # pd.Timestamp(2017-06-12', tz='UTC'),  # 台风苗柏1702,期货夜盘17:35休市
    pd.Timestamp('2017-08-23', tz='UTC'),  # 台风天鸽1713
]


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
            LabourDay,
            HKRegionEstablishmentDay,
            CommemoratingAlliedVictory,
            IDontKnow,
            NationalDay,
            QueenBirthday,
            QueenBirthday2,
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
            HKAdhocClosures,
        ))

    @property
    def special_closes(self):
        return [
            # HK changed their early close time
            (
                time(12, 30), HolidayCalendar([
                    new_years_eve(
                        # Market was close for Y2K instead of closing early
                        end_date=pd.Timestamp('1999-12-01'),
                        days_of_week=weekdays,
                    ),
                    new_years_eve(
                        start_date=pd.Timestamp('2000-12-01'),
                        end_date=pd.Timestamp('2011-03-07'),
                        days_of_week=weekdays,
                    ),
                    christmas_eve(
                        end_date=pd.Timestamp('2011-03-07'),
                        days_of_week=weekdays
                    )])
            ),
            (
                time(12, 00), HolidayCalendar([
                    new_years_eve(
                        start_date=pd.Timestamp('2011-03-07'),
                        days_of_week=weekdays,
                    ),
                    christmas_eve(
                        start_date=pd.Timestamp('2011-03-07'),
                        days_of_week=weekdays
                    )])
            ),
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
