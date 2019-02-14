from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xmil import XMILExchangeCalendar


class XMILCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xmil'
    calendar_class = XMILExchangeCalendar

    # The XMIL is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    HAVE_EARLY_CLOSES = False

    def test_normal_year(self):
        expected_holidays = [
            pd.Timestamp('2018-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2018-03-30', tz=UTC),  # Good Friday
            pd.Timestamp('2018-04-02', tz=UTC),  # Easter Monday
            pd.Timestamp('2018-05-01', tz=UTC),  # Labor Day
            pd.Timestamp('2018-08-15', tz=UTC),  # Ferragosto
            pd.Timestamp('2018-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2018-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2018-12-26', tz=UTC),  # Boxing Day
            pd.Timestamp('2018-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_holidays_fall_on_weekend(self):
        # Holidays falling on a weekend should not be made up during the week.
        expected_sessions = [
            # In 2017 New Year's Day fell on a Sunday, so the Friday before and
            # the Monday after should both be open.
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
            # In 2015 Ferragosto fell on a Saturday, so the Friday before and
            # the Monday after should both be open.
            pd.Timestamp('2015-08-14', tz=UTC),
            pd.Timestamp('2015-08-17', tz=UTC),
            # In 2010 Labour Day fell on a Saturday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2010-04-30', tz=UTC),
            pd.Timestamp('2010-05-03', tz=UTC),
            # Christmas also fell on a Saturday, meaning Boxing Day fell on a
            # Sunday. The market should be closed on Christmas Eve (Friday) but
            # still be open on both the prior Thursday and the next Monday.
            pd.Timestamp('2010-12-23', tz=UTC),
            pd.Timestamp('2010-12-27', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)
