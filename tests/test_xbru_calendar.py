from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import EuronextCalendarTestBase
from trading_calendars.exchange_calendar_xbru import XBRUExchangeCalendar


class XBRUCalendarTestCase(EuronextCalendarTestBase, TestCase):

    answer_key_filename = 'xbru'
    calendar_class = XBRUExchangeCalendar

    # The XBRU is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5
    TIMEDELTA_TO_NORMAL_CLOSE = pd.Timedelta(hours=17, minutes=30)

    TZ = 'Europe/Brussels'

    def test_old_holidays(self):
        """
        Test the before and after of holidays that are no longer observed.
        """
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2000-06-01', tz=UTC),  # Ascension Day
            pd.Timestamp('2001-06-04', tz=UTC),  # Whit Monday
            pd.Timestamp('2000-07-21', tz=UTC),  # Belgium Independence Day
            pd.Timestamp('2001-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

        expected_sessions = [
            pd.Timestamp('2001-05-24', tz=UTC),  # Ascension Day
            pd.Timestamp('2002-05-20', tz=UTC),  # Whit Monday
            pd.Timestamp('2003-07-21', tz=UTC),  # Belgium Independence Day
            pd.Timestamp('2002-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)
