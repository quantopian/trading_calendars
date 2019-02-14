from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xosl import XOSLExchangeCalendar


class XOSLCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xosl'
    calendar_class = XOSLExchangeCalendar

    # The XOSL is open from 9:00 am to 4:30 pm.
    MAX_SESSION_HOURS = 7.5

    def test_all_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2018-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2018-03-29', tz=UTC),  # Maundy Thursday
            pd.Timestamp('2018-03-30', tz=UTC),  # Good Friday
            pd.Timestamp('2018-04-02', tz=UTC),  # Easter Monday
            pd.Timestamp('2018-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2018-05-10', tz=UTC),  # Ascension Day
            pd.Timestamp('2018-05-17', tz=UTC),  # Constitution Day
            pd.Timestamp('2018-05-21', tz=UTC),  # Whit Monday
            pd.Timestamp('2018-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2018-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2018-12-26', tz=UTC),  # Boxing Day
            pd.Timestamp('2018-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Holidays falling on a weekend should not be made up during the week.
        expected_sessions = [
            # In 2010, Labour Day fell on a Saturday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2010-04-30', tz=UTC),
            pd.Timestamp('2010-05-03', tz=UTC),

            # In 2015, Constitution Day fell on a Sunday, so the market should
            # be open on both the prior Friday and the following Monday.
            pd.Timestamp('2015-05-15', tz=UTC),
            pd.Timestamp('2015-05-18', tz=UTC),

            # In 2010, Christmas fell on a Saturday, meaning Boxing Day fell on
            # a Sunday. The market should thus be open on the following Monday.
            pd.Timestamp('2010-12-27', tz=UTC),

            # In 2017, New Year's Day fell on a Sunday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_early_closes(self):
        # Starting in 2011, Holy Wednesday should be a half day.
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2010-03-31', tz=UTC)),
            pd.Timestamp('2010-03-31 16:20', tz='Europe/Oslo'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2011-04-20', tz=UTC)),
            pd.Timestamp('2011-04-20 13:00', tz='Europe/Oslo'),
        )
