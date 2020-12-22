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
import pandas as pd
from pytz import timezone, UTC
from .trading_calendar import TradingCalendar

# All holidays are defined as ad-hoc holidays for each year since there is
# currently no support for Hebrew calendar holiday rules in pandas.


class XTAEExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for TASE Stock Exchange.

    Open/close times are continuous trading times valid Mon-Thu for Shares
    Group A. Trading schedule differs on Sundays.

    Open Time: 9:59 AM, Asia/Tel_Aviv (randomly between 9:59 and 10:00).
    Close Time: 5:14 PM, Asia/Tel_Aviv (randomly between 5:14 and 5:15).

    Regularly-Observed Holidays (not necessarily in order):
    - Purim
    - Passover_I_Eve
    - Passover_I
    - Passover_II_Eve
    - Passover_II
    - Independence_Day
    - Yom_HaZikaron
    - Shavuot_Eve
    - Shavuot
    - Tisha_beAv
    - Jewish_New_Year_Eve
    - Jewish_New_Year_I
    - Jewish_New_Year_II
    - Yom_Kippur_Eve
    - Yom_Kippur
    - Sukkoth_Eve
    - Sukkoth
    - Simchat_Tora_Eve
    - Simchat_Tora

    Note these dates are only checked against 2019-2023.

    https://info.tase.co.il/eng/about_tase/corporate/pages/vacation_schedule.aspx

    Daylight Saving Time in Israel comes into effect on the Friday before the
    last Sunday in March, and lasts until the last Sunday in October. During the
    Daylight Saving time period the clock will be UTC+3, and UTC+2 for the rest
    of the year.
    """  # noqa
    start_date = pd.Timestamp('2019-01-01', tz=UTC)

    name = 'XTAE'

    tz = timezone('Asia/Tel_Aviv')

    open_times = (
        (None, time(10, 0)),
    )

    close_times = (
        (None, time(17, 15)),
    )

    @property
    def adhoc_holidays(self):
        return [
            # 2019
            # Purim
            pd.Timestamp('2019-03-21', tz='Asia/Jerusalem'),
            # Election Day
            pd.Timestamp('2019-04-09', tz='Asia/Jerusalem'),
            # Passover II Eve
            pd.Timestamp('2019-04-25', tz='Asia/Jerusalem'),
            # Passover II
            pd.Timestamp('2019-04-26', tz='Asia/Jerusalem'),
            # Memorial Day
            pd.Timestamp('2019-05-08', tz='Asia/Jerusalem'),
            # Independence Day
            pd.Timestamp('2019-05-09', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot)
            pd.Timestamp('2019-06-09', tz='Asia/Jerusalem'),
            # Fast Day
            pd.Timestamp('2019-08-11', tz='Asia/Jerusalem'),
            # Election Day
            pd.Timestamp('2019-09-17', tz='Asia/Jerusalem'),
            # Jewish New Year Eve
            pd.Timestamp('2019-09-29', tz='Asia/Jerusalem'),
            # Jewish New Year I
            pd.Timestamp('2019-09-30', tz='Asia/Jerusalem'),
            # Jewish New Year II
            pd.Timestamp('2019-10-01', tz='Asia/Jerusalem'),
            # Yom Kiuppur Eve
            pd.Timestamp('2019-10-08', tz='Asia/Jerusalem'),
            # Yom Kippur
            pd.Timestamp('2019-10-09', tz='Asia/Jerusalem'),
            # Feast of Tabernacles (Sukkoth) Eve
            pd.Timestamp('2019-10-13', tz='Asia/Jerusalem'),
            # Feast of Tabernacles
            pd.Timestamp('2019-10-14', tz='Asia/Jerusalem'),
            # Rejoicing of the Law (Simchat Tora) Eve
            pd.Timestamp('2019-10-20', tz='Asia/Jerusalem'),
            # Rejoicing of the Law
            pd.Timestamp('2019-10-21', tz='Asia/Jerusalem'),
            # 2020
            # Election Day
            pd.Timestamp('2020-03-02', tz='Asia/Jerusalem'),
            # Purim
            pd.Timestamp('2020-03-10', tz='Asia/Jerusalem'),
            # Passover I Eve
            pd.Timestamp('2020-04-08', tz='Asia/Jerusalem'),
            # Passover I
            pd.Timestamp('2020-04-09', tz='Asia/Jerusalem'),
            # Passover II Eve
            pd.Timestamp('2020-04-14', tz='Asia/Jerusalem'),
            # Passover II
            pd.Timestamp('2020-04-15', tz='Asia/Jerusalem'),
            # Memorial Day
            pd.Timestamp('2020-04-28', tz='Asia/Jerusalem'),
            # Independence Day
            pd.Timestamp('2020-04-29', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot) Eve
            pd.Timestamp('2020-05-28', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot)
            pd.Timestamp('2020-05-29', tz='Asia/Jerusalem'),
            # Fast Day
            pd.Timestamp('2020-07-30', tz='Asia/Jerusalem'),
            # Jewesh New Year II
            pd.Timestamp('2020-09-20', tz='Asia/Jerusalem'),
            # Yom Kippur Eve
            pd.Timestamp('2020-09-27', tz='Asia/Jerusalem'),
            # Yom Kippur
            pd.Timestamp('2020-09-28', tz='Asia/Jerusalem'),
            # 2021
            # Purim
            pd.Timestamp('2021-02-26', tz='Asia/Jerusalem'),
            # Passover I
            pd.Timestamp('2021-03-28', tz='Asia/Jerusalem'),
            # Passover II Eve
            pd.Timestamp('2021-04-02', tz='Asia/Jerusalem'),
            # Memorial Day
            pd.Timestamp('2021-04-14', tz='Asia/Jerusalem'),
            # Independence Day
            pd.Timestamp('2021-04-15', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot) Eve
            pd.Timestamp('2021-05-16', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot)
            pd.Timestamp('2021-05-17', tz='Asia/Jerusalem'),
            # Fast Day
            pd.Timestamp('2021-07-18', tz='Asia/Jerusalem'),
            # Jewesh New Year Eve
            pd.Timestamp('2021-09-06', tz='Asia/Jerusalem'),
            # Jewesh New Year I
            pd.Timestamp('2021-09-07', tz='Asia/Jerusalem'),
            # Jewesh New Year II
            pd.Timestamp('2021-09-08', tz='Asia/Jerusalem'),
            # Yom Kippur Eve
            pd.Timestamp('2021-09-15', tz='Asia/Jerusalem'),
            # Yom Kippur
            pd.Timestamp('2021-09-16', tz='Asia/Jerusalem'),
            # Feast of Tabernacles (Sukkoth) Eve
            pd.Timestamp('2021-09-20', tz='Asia/Jerusalem'),
            # Feast of Tabernacles (Sukkoth)
            pd.Timestamp('2021-09-21', tz='Asia/Jerusalem'),
            # Recoicing of the Law (Simchat Tora) Eve
            pd.Timestamp('2021-09-27', tz='Asia/Jerusalem'),
            # Recoicing of the Law (Simchat Tora)
            pd.Timestamp('2021-09-28', tz='Asia/Jerusalem'),
            # 2022
            # Purim
            pd.Timestamp('2022-03-17', tz='Asia/Jerusalem'),
            # Shushan Purim
            pd.Timestamp('2022-03-18', tz='Asia/Jerusalem'),
            # Passover Eve
            pd.Timestamp('2022-04-15', tz='Asia/Jerusalem'),
            # Passover II Eve
            pd.Timestamp('2022-04-21', tz='Asia/Jerusalem'),
            # Passover II
            pd.Timestamp('2022-04-22', tz='Asia/Jerusalem'),
            # Memorial Day (moved up)
            pd.Timestamp('2022-05-04', tz='Asia/Jerusalem'),
            # Independence Day
            pd.Timestamp('2022-05-05', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot)
            pd.Timestamp('2022-06-05', tz='Asia/Jerusalem'),
            # Fast Day (postponed)
            pd.Timestamp('2022-08-07', tz='Asia/Jerusalem'),
            # Jewish New Year Eve
            pd.Timestamp('2022-09-25', tz='Asia/Jerusalem'),
            # Jewish New Year I
            pd.Timestamp('2022-09-26', tz='Asia/Jerusalem'),
            # Jewish New Year II
            pd.Timestamp('2022-09-27', tz='Asia/Jerusalem'),
            # Yom Kippur Eve
            pd.Timestamp('2022-10-04', tz='Asia/Jerusalem'),
            # Yom Kippur
            pd.Timestamp('2022-10-05', tz='Asia/Jerusalem'),
            # Feast of Tabernacles (Sukkoth) Eve
            pd.Timestamp('2022-10-09', tz='Asia/Jerusalem'),
            # Feast of Tabernacles (Sukkoth)
            pd.Timestamp('2022-10-10', tz='Asia/Jerusalem'),
            # Rejoicing of the Law (Simchat Tora) Eve
            pd.Timestamp('2022-10-16', tz='Asia/Jerusalem'),
            # Rejoicing of the Law (Simchat Tora)
            pd.Timestamp('2022-10-17', tz='Asia/Jerusalem'),
            # 2023
            # Purim
            pd.Timestamp('2023-03-07', tz='Asia/Jerusalem'),
            # Shushan Purim
            pd.Timestamp('2023-03-08', tz='Asia/Jerusalem'),
            # Passover Eve
            pd.Timestamp('2023-04-05', tz='Asia/Jerusalem'),
            # Passover
            pd.Timestamp('2023-04-06', tz='Asia/Jerusalem'),
            # Passover II Eve
            pd.Timestamp('2023-04-11', tz='Asia/Jerusalem'),
            # Passover II
            pd.Timestamp('2023-04-12', tz='Asia/Jerusalem'),
            # Memorial Day
            pd.Timestamp('2023-04-25', tz='Asia/Jerusalem'),
            # Independence Day
            pd.Timestamp('2023-04-26', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot) Eve
            pd.Timestamp('2023-05-25', tz='Asia/Jerusalem'),
            # Pentecost (Shavuot)
            pd.Timestamp('2023-05-26', tz='Asia/Jerusalem'),
            # Fast Day
            pd.Timestamp('2023-07-27', tz='Asia/Jerusalem'),
            # Jewish New Year Eve
            pd.Timestamp('2023-09-15', tz='Asia/Jerusalem'),
            # Jewish New Year II
            pd.Timestamp('2023-09-17', tz='Asia/Jerusalem'),
            # Yom Kippur Eve
            pd.Timestamp('2023-09-24', tz='Asia/Jerusalem'),
            # Yom Kippur
            pd.Timestamp('2023-09-25', tz='Asia/Jerusalem'),
            # Feast of Tabernacles (Sukkoth) Eve
            pd.Timestamp('2023-09-29', tz='Asia/Jerusalem'),
            # Rejoicing of the Law (Simchat Tora) Eve
            pd.Timestamp('2023-10-06', tz='Asia/Jerusalem'),
        ]

    @property
    def weekmask(self):
        return '1111001'
