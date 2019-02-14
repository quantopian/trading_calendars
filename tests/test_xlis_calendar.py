from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import EuronextCalendarTestBase
from trading_calendars.exchange_calendar_xlis import XLISExchangeCalendar


class XLISCalendarTestCase(EuronextCalendarTestBase, TestCase):

    answer_key_filename = 'xlis'
    calendar_class = XLISExchangeCalendar

    # The XLIS is open from 8:00 am to 4:30 pm.
    MAX_SESSION_HOURS = 8.5
    TIMEDELTA_TO_NORMAL_CLOSE = pd.Timedelta(hours=16, minutes=30)

    TZ = 'Europe/Lisbon'

    def test_old_holidays(self):
        """
        Test the before and after of holidays that are no longer observed.
        """
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2002-02-12', tz=UTC),  # Carnival
            pd.Timestamp('2002-05-30', tz=UTC),  # Corpus Christi Day
            pd.Timestamp('2002-04-25', tz=UTC),  # Liberty Day
            pd.Timestamp('2002-06-10', tz=UTC),  # Portugal Day
            pd.Timestamp('2001-06-13', tz=UTC),  # Saint Anthony's Day
            pd.Timestamp('2002-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2001-10-05', tz=UTC),  # Republic Day
            pd.Timestamp('2002-11-01', tz=UTC),  # All Saints Day
            pd.Timestamp('2000-12-01', tz=UTC),  # Independence Day
            pd.Timestamp('2000-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2002-12-24', tz=UTC),  # Christmas Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

        expected_sessions = [
            pd.Timestamp('2003-03-04', tz=UTC),  # Carnival
            pd.Timestamp('2003-06-16', tz=UTC),  # Corpus Christi Day
            pd.Timestamp('2003-04-25', tz=UTC),  # Liberty Day
            pd.Timestamp('2003-06-10', tz=UTC),  # Portugal Day
            pd.Timestamp('2002-06-13', tz=UTC),  # Saint Anthony's Day
            pd.Timestamp('2003-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2004-10-05', tz=UTC),  # Republic Day
            pd.Timestamp('2004-11-01', tz=UTC),  # All Saints Day
            pd.Timestamp('2003-12-01', tz=UTC),  # Independence Day
            pd.Timestamp('2003-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2003-12-24', tz=UTC),  # Christmas Eve
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)
