from unittest import TestCase
import pandas as pd

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xtae import XTAEExchangeCalendar


class XTAECalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xtae'
    calendar_class = XTAEExchangeCalendar

    # The XLON exchange is open from 10:00 am to 17:14 pm.
    MAX_SESSION_HOURS = 7.25

    def test_2019(self):
        expected_holidays_2019 = [
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
        ]

        for session_label in expected_holidays_2019:
            self.assertNotIn(session_label, self.calendar.all_sessions)
