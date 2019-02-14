from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xsto import XSTOExchangeCalendar


class XSTOCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xsto'
    calendar_class = XSTOExchangeCalendar

    # The XSTO is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    def test_all_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2018-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2017-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2018-03-30', tz=UTC),  # Good Friday
            pd.Timestamp('2018-04-02', tz=UTC),  # Easter Monday
            pd.Timestamp('2018-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2018-05-10', tz=UTC),  # Ascension Day
            pd.Timestamp('2018-06-06', tz=UTC),  # National Day
            pd.Timestamp('2018-06-22', tz=UTC),  # Midsummer Eve
            pd.Timestamp('2018-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2018-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2018-12-26', tz=UTC),  # Boxing Day
            pd.Timestamp('2018-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, all_sessions)

        # The market holiday for Midsummer Eve should fall on the Friday after
        # June 18. In 2010, June 18 was a Friday so the market holiday should
        # fall on June 25.
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

            # In 2015, National Day fell on a Saturday, so the market should be
            # open on both the prior Friday and the following Monday.
            pd.Timestamp('2015-06-05', tz=UTC),
            pd.Timestamp('2015-06-08', tz=UTC),

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

        # In 2017, June 18 fell on a Sunday, so the following Friday should be
        # a holiday.
        self.assertNotIn(pd.Timestamp('2017-06-23', tz=UTC), all_sessions)

    def test_old_holidays(self):
        """
        Test the before and after of holidays that are no longer observed.
        """
        all_sessions = self.calendar.all_sessions

        # Whit Monday is no longer a holiday starting in 2005.
        self.assertNotIn(pd.Timestamp('2004-05-31', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2005-05-16', tz=UTC), all_sessions)

    def test_early_closes(self):
        # The session label and close time for expected early closes.
        expected_early_closes = [
            # Day before Epiphany.
            (
                pd.Timestamp('2018-01-05', tz=UTC),
                pd.Timestamp('2018-01-05 13:00', tz='Europe/Stockholm'),
            ),
            # Maundy Thursday.
            (
                pd.Timestamp('2018-03-29', tz=UTC),
                pd.Timestamp('2018-03-29 13:00', tz='Europe/Stockholm'),
            ),
            # Day before Labour Day.
            (
                pd.Timestamp('2018-04-30', tz=UTC),
                pd.Timestamp('2018-04-30 13:00', tz='Europe/Stockholm'),
            ),
            # Day before Ascension Day.
            (
                pd.Timestamp('2018-05-09', tz=UTC),
                pd.Timestamp('2018-05-09 13:00', tz='Europe/Stockholm'),
            ),
            # All Saints' Eve.
            (
                pd.Timestamp('2018-11-02', tz=UTC),
                pd.Timestamp('2018-11-02 13:00', tz='Europe/Stockholm'),
            ),
            (
                pd.Timestamp('2015-10-30', tz=UTC),
                pd.Timestamp('2015-10-30 13:00', tz='Europe/Stockholm'),
            ),
            (
                pd.Timestamp('2010-11-05', tz=UTC),
                pd.Timestamp('2010-11-05 13:00', tz='Europe/Stockholm'),
            ),
        ]

        for session, expected_close in expected_early_closes:
            self.assertEqual(
                self.calendar.session_close(session),
                expected_close,
            )
