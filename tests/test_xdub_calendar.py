from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xdub import XDUBExchangeCalendar


class XDUBCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xdub'
    calendar_class = XDUBExchangeCalendar

    # The XDUB is open from 8:00 am to 4:28 pm.
    MAX_SESSION_HOURS = 8.467

    def test_normal_year(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2018-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2018-03-30', tz=UTC),  # Good Friday
            pd.Timestamp('2018-04-02', tz=UTC),  # Easter Monday
            pd.Timestamp('2018-05-07', tz=UTC),  # May Bank Holiday
            pd.Timestamp('2018-06-04', tz=UTC),  # June Bank Holiday
            pd.Timestamp('2018-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2018-12-26', tz=UTC),  # Boxing Day
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Holidays falling on a weekend should be made up on the next trading
        # day.
        expected_holidays = [
            # In 2017 New Year's Day fell on a Sunday, so the following Monday
            # should be a holiday.
            pd.Timestamp('2017-01-02', tz=UTC),

            # In 2010 Christmas fell on a Saturday, meaning Boxing Day fell on
            # a Sunday. The following Monday and Tuesday should both be
            # holidays.
            pd.Timestamp('2010-12-27', tz=UTC),
            pd.Timestamp('2010-12-28', tz=UTC),

            # In 2016 Christmas fell on a Sunday, but again the following
            # Monday and Tuesday should both be holidays.
            pd.Timestamp('2016-12-26', tz=UTC),
            pd.Timestamp('2016-12-27', tz=UTC),
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

    def test_old_holidays(self):
        """
        Test the before and after of holidays that are no longer observed.
        """
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('1996-03-18', tz=UTC),  # St. Patrick's Day Observed
            pd.Timestamp('2000-03-17', tz=UTC),  # St. Patrick's Day
            pd.Timestamp('2009-05-01', tz=UTC),  # Labour Day
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

        expected_sessions = [
            pd.Timestamp('2001-03-19', tz=UTC),  # St. Patrick's Day Observed
            pd.Timestamp('2003-03-17', tz=UTC),  # St. Patrick's Day
            pd.Timestamp('2012-05-01', tz=UTC),  # Labour Day
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_ad_hoc_holidays(self):
        # March 2, 2018 was closed due to sever weather.
        self.assertNotIn(
            pd.Timestamp('2018-03-02', tz=UTC),
            self.calendar.all_sessions,
        )

    def test_early_closes(self):
        # The session label and close time for expected early closes.
        expected_early_closes = [
            # Christmas Eve on a weekday.
            (
                pd.Timestamp('2010-12-24', tz=UTC),
                pd.Timestamp('2010-12-24 12:28', tz='Europe/Dublin'),
            ),
            (
                pd.Timestamp('2018-12-24', tz=UTC),
                pd.Timestamp('2018-12-24 12:28', tz='Europe/Dublin'),
            ),
            # If Christmas Eve falls on a weekend the last trading day before
            # Christmas should be a trading day.
            (
                pd.Timestamp('2017-12-22', tz=UTC),
                pd.Timestamp('2017-12-22 12:28', tz='Europe/Dublin'),
            ),
            # New Year's Eve on a weekday.
            (
                pd.Timestamp('2010-12-31', tz=UTC),
                pd.Timestamp('2010-12-31 12:28', tz='Europe/Dublin'),
            ),
            (
                pd.Timestamp('2018-12-31', tz=UTC),
                pd.Timestamp('2018-12-31 12:28', tz='Europe/Dublin'),
            ),
            # If New Year's Eve falls on a weekend the last trading day of the
            # year should be a half day.
            (
                pd.Timestamp('2017-12-29', tz=UTC),
                pd.Timestamp('2017-12-29 12:28', tz='Europe/Dublin'),
            ),
            # March 1, 2018 was a half day due to severe weather.
            (
                pd.Timestamp('2018-03-01', tz=UTC),
                pd.Timestamp('2018-03-01 12:28', tz='Europe/Dublin'),
            ),
        ]

        for session, expected_close in expected_early_closes:
            self.assertEqual(
                self.calendar.session_close(session),
                expected_close,
            )

        expected_full_days = [
            # Prior to 2010 Christmas Eve and New Year's Eve were full days.
            (
                pd.Timestamp('2009-12-24', tz=UTC),
                pd.Timestamp('2009-12-24 16:28', tz='Europe/Dublin'),
            ),
            (
                pd.Timestamp('2009-12-31', tz=UTC),
                pd.Timestamp('2009-12-31 16:28', tz='Europe/Dublin'),
            ),
            # March 1st on any other year should be a normal day.
            (
                pd.Timestamp('2017-03-01', tz=UTC),
                pd.Timestamp('2017-03-01 16:28', tz='Europe/Dublin'),
            ),
        ]

        for session, expected_close in expected_full_days:
            self.assertEqual(
                self.calendar.session_close(session),
                expected_close,
            )
