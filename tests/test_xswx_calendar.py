from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xswx import XSWXExchangeCalendar


class XSWXCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xswx'
    calendar_class = XSWXExchangeCalendar

    # The XSWX is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    HAVE_EARLY_CLOSES = False

    def test_2012(self):
        expected_holidays_2012 = [
            # New Year's Day isn't observed because it was on a Sunday
            pd.Timestamp("2012-01-02", tz=UTC),  # Berchtold's Day observed
            pd.Timestamp("2012-04-06", tz=UTC),  # Good Friday
            pd.Timestamp("2012-04-09", tz=UTC),  # Easter Monday
            pd.Timestamp("2012-05-01", tz=UTC),  # Labour Day
            pd.Timestamp("2012-05-17", tz=UTC),  # Ascension Day
            pd.Timestamp("2012-05-28", tz=UTC),  # Whit Monday
            pd.Timestamp("2012-08-01", tz=UTC),  # Swiss National Day
            pd.Timestamp("2012-12-24", tz=UTC),  # Christmas Eve
            pd.Timestamp("2012-12-25", tz=UTC),  # Christmas
            pd.Timestamp("2012-12-26", tz=UTC),  # Boxing Day
            pd.Timestamp("2012-12-31", tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays_2012:
            self.assertNotIn(session_label, self.calendar.all_sessions)
