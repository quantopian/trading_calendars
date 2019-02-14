from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xfra import XFRAExchangeCalendar


class XFRACalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xfra'
    calendar_class = XFRAExchangeCalendar

    # The FWB is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    def test_whit_monday(self):
        # Whit Monday was not observed prior to 2007.
        self.assertIn(
            pd.Timestamp('2006-06-05', tz=UTC),
            self.calendar.all_sessions,
        )

        # It was observed as a one-off in 2007...
        self.assertNotIn(
            pd.Timestamp('2007-05-28', tz=UTC),
            self.calendar.all_sessions,
        )

        # ...then not again...
        self.assertIn(
            pd.Timestamp('2008-05-12', tz=UTC),
            self.calendar.all_sessions,
        )

        # ...until 2015...
        self.assertNotIn(
            pd.Timestamp('2015-05-25', tz=UTC),
            self.calendar.all_sessions,
        )

        # ...when it became regularly observed.
        self.assertNotIn(
            pd.Timestamp('2016-05-16', tz=UTC),
            self.calendar.all_sessions,
        )

    def test_2012(self):
        expected_holidays_2012 = [
            # New Year's Day fell on a Sunday, so it is not a holiday this year
            pd.Timestamp("2012-04-06", tz=UTC),  # Good Friday
            pd.Timestamp("2012-04-09", tz=UTC),  # Easter Monday
            pd.Timestamp("2012-05-01", tz=UTC),  # Labour Day
            # Whit Monday was observed in 2007, then 2015 and after.
            # German Unity Day started being celebrated in 2014
            pd.Timestamp("2012-12-24", tz=UTC),  # Christmas Eve
            pd.Timestamp("2012-12-25", tz=UTC),  # Christmas
            pd.Timestamp("2012-12-26", tz=UTC),  # Boxing Day
            pd.Timestamp("2012-12-31", tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays_2012:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        early_closes_2012 = [
            pd.Timestamp("2012-12-28", tz=UTC),  # Last working day of 2012
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

    def test_reformation_day(self):
        # Reformation Day was a German national holiday in 2017 only.
        self.assertNotIn(
            pd.Timestamp('2017-10-31', tz=UTC),
            self.calendar.all_sessions,
        )

        # Ensure it is a trading day in the surrounding years.
        self.assertIn(
            pd.Timestamp('2016-10-31', tz=UTC),
            self.calendar.all_sessions,
        )
        self.assertIn(
            pd.Timestamp('2018-10-31', tz=UTC),
            self.calendar.all_sessions,
        )
