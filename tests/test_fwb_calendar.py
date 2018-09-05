from unittest import TestCase
import pandas as pd

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_fwb import FWBExchangeCalendar


class FWBCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'fwb'
    calendar_class = FWBExchangeCalendar

    # The FWB is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    def test_whit_monday(self):
        # Whit Monday should be a trading in 2009 but not in 2010
        self.assertIn(
            pd.Timestamp('2009-06-01', tz='UTC'),
            self.calendar.all_sessions
        )

        self.assertNotIn(
            pd.Timestamp('2010-05-24', tz='UTC'),
            self.calendar.all_sessions
        )

    def test_2012(self):
        expected_holidays_2012 = [
            # New Year's Day fell on a Sunday, so it is not a holiday this year
            pd.Timestamp("2012-04-06", tz='UTC'),  # Good Friday
            pd.Timestamp("2012-04-09", tz='UTC'),  # Easter Monday
            pd.Timestamp("2012-05-01", tz='UTC'),  # Labour Day
            pd.Timestamp("2012-05-28", tz='UTC'),  # Whit Monday
            # German Unity Day started being celebrated in 2014
            pd.Timestamp("2012-12-24", tz='UTC'),  # Christmas Eve
            pd.Timestamp("2012-12-25", tz='UTC'),  # Christmas
            pd.Timestamp("2012-12-26", tz='UTC'),  # Boxing Day
            pd.Timestamp("2012-12-31", tz='UTC'),  # New Year's Eve
        ]

        for session_label in expected_holidays_2012:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        early_closes_2012 = [
            pd.Timestamp("2012-12-28", tz='UTC'),  # Last working day of 2012
        ]

        for early_close_session_label in early_closes_2012:
            self.assertIn(early_close_session_label,
                          self.calendar.early_closes)

    def test_half_days(self):
        half_days = [
            # In 2011, NYE was on a Sat, so Fri is a half day
            pd.Timestamp('2011-12-30', tz='CET'),
            # In 2012, NYE was on a Mon, so the preceding Fri is a half day
            pd.Timestamp('2012-12-28', tz='CET'),
        ]

        for half_day in half_days:
            half_day_close_time = self.calendar.next_close(half_day)
            self.assertEqual(
                half_day_close_time,
                half_day + pd.Timedelta(hours=12, minutes=30)
            )

    def test_start_end(self):
        """
        Check TradingCalendar with defined start/end dates.
        """
        start = pd.Timestamp('2010-1-3', tz='UTC')
        end = pd.Timestamp('2010-1-10', tz='UTC')
        calendar = FWBExchangeCalendar(start=start, end=end)
        expected_first = pd.Timestamp('2010-1-4', tz='UTC')
        expected_last = pd.Timestamp('2010-1-8', tz='UTC')

        self.assertTrue(calendar.first_trading_session == expected_first)
        self.assertTrue(calendar.last_trading_session == expected_last)
