from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xhel import XHELExchangeCalendar


class XHELCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xhel'
    calendar_class = XHELExchangeCalendar

    # The XHEL is open from 10:00 am to 6:30 pm.
    MAX_SESSION_HOURS = 8.5

    HAVE_EARLY_CLOSES = False

    def test_all_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2018-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2017-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2018-03-30', tz=UTC),  # Good Friday
            pd.Timestamp('2018-04-02', tz=UTC),  # Easter Monday
            pd.Timestamp('2018-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2018-05-10', tz=UTC),  # Ascension Day
            pd.Timestamp('2018-06-22', tz=UTC),  # Midsummer Eve
            pd.Timestamp('2018-12-06', tz=UTC),  # Finland Independence Day
            pd.Timestamp('2018-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2018-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2018-12-26', tz=UTC),  # Boxing Day
            pd.Timestamp('2018-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

        # The market holiday for Midsummer Eve should fall on the Friday after
        # June 18. In 2010, June 18 was a Friday so the market holiday should
        # be on June 25.
        self.assertIn(pd.Timestamp('2010-06-18', tz=UTC), all_sessions)
        self.assertNotIn(pd.Timestamp('2010-06-25', tz=UTC), all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Holidays falling on a weekend should not be made up during the week.
        expected_sessions = [
            # In 2018, the Epiphany fell on a Saturday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2018-01-05', tz=UTC),
            pd.Timestamp('2018-01-08', tz=UTC),

            # In 2010, Labour Day fell on a Saturday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2010-04-30', tz=UTC),
            pd.Timestamp('2010-05-03', tz=UTC),

            # In 2015, Finland Independence Day fell on a Sunday, so the market
            # should be open on both the prior Friday and the following Monday.
            pd.Timestamp('2015-12-04', tz=UTC),
            pd.Timestamp('2015-12-07', tz=UTC),

            # In 2010, Christmas fell on a Saturday, meaning Boxing Day fell on
            # a Sunday. The market should thus be open on the following Monday.
            pd.Timestamp('2010-12-27', tz=UTC),

            # In 2017, New Year's Day fell on a Sunday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)

        # In 2017, June 18 fell on a Sunday, so the following Friday should be
        # a holiday.
        self.assertNotIn(pd.Timestamp('2017-06-23', tz=UTC), all_sessions)
