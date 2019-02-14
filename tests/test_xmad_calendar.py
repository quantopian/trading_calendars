from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xmad import XMADExchangeCalendar


class XMADCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xmad'
    calendar_class = XMADExchangeCalendar

    # The XMAD is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2018-03-12', '2018-11-05']

    def test_normal_year(self):
        expected_holidays = [
            pd.Timestamp('2014-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2014-04-18', tz=UTC),  # Good Friday
            pd.Timestamp('2014-04-21', tz=UTC),  # Easter Monday
            pd.Timestamp('2014-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2014-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2014-12-26', tz=UTC),  # Boxing Day
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_holidays_fall_on_weekend(self):
        # In general, holidays falling on a weekend should not be made up
        # during the week.
        expected_sessions = [
            # In 2010, Labour Day fell on a Saturday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2010-04-30', tz=UTC),
            pd.Timestamp('2010-05-03', tz=UTC),

            # Christmas also fell on a Saturday, meaning Boxing Day fell on a
            # Sunday. The market should still be open on the following Monday
            # (note that Christmas Eve was observed as a holiday through 2010,
            # so the market is closed on the previous Friday).
            pd.Timestamp('2010-12-27', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)

        # Assumption day is the only day that should be observed on a Monday
        # when falling on a weekend. In 2004 the 15th was on a Sunday, so the
        # 16th should be a holiday.
        self.assertNotIn(
            pd.Timestamp('2004-08-16', tz=UTC),
            self.calendar.all_sessions,
        )

    def test_old_holidays(self):
        """
        Test the before and after of holidays that are no longer observed.
        """
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2006-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2003-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2004-10-12', tz=UTC),  # National Day
            pd.Timestamp('2004-11-01', tz=UTC),  # All Saints Day
            pd.Timestamp('2004-12-06', tz=UTC),  # Constitution Day
            pd.Timestamp('2004-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2010-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2010-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

        expected_sessions = [
            pd.Timestamp('2009-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2005-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2005-10-12', tz=UTC),  # National Day
            pd.Timestamp('2005-11-01', tz=UTC),  # All Saints Day
            pd.Timestamp('2005-12-06', tz=UTC),  # Constitution Day
            pd.Timestamp('2005-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2012-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2012-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_early_closes(self):
        # The session label and close time for expected early closes.
        expected_early_closes = [
            # Christmas Eve
            (
                pd.Timestamp('2012-12-24', tz=UTC),
                pd.Timestamp('2012-12-24 14:00', tz='Europe/Madrid'),
            ),
            # New Year's Eve
            (
                pd.Timestamp('2012-12-31', tz=UTC),
                pd.Timestamp('2012-12-31 14:00', tz='Europe/Madrid'),
            ),
        ]

        for session, expected_close in expected_early_closes:
            self.assertEqual(
                self.calendar.session_close(session),
                expected_close,
            )
