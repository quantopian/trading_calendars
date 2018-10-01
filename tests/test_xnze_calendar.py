from unittest import TestCase

import pandas as pd

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xnze import XNZEExchangeCalendar


class XNZECalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xnze'
    calendar_class = XNZEExchangeCalendar

    # The New Zealand Exchange is open from 10:00 am to 4:45 pm.
    MAX_SESSION_HOURS = 6.75

    def test_normal_year(self):
        expected_holidays_2014 = [
            pd.Timestamp('2014-01-01', tz='UTC'),  # New Year's Day
            pd.Timestamp('2014-01-02', tz='UTC'),  # Day after New Year's Day
            pd.Timestamp('2014-02-06', tz='UTC'),  # Waitangi Day
            pd.Timestamp('2014-04-18', tz='UTC'),  # Good Friday
            pd.Timestamp('2014-04-21', tz='UTC'),  # Easter Monday
            pd.Timestamp('2014-04-25', tz='UTC'),  # Anzac Day
            pd.Timestamp('2014-06-02', tz='UTC'),  # Queen's Birthday
            pd.Timestamp('2014-10-27', tz='UTC'),  # Labour Day
            pd.Timestamp('2014-12-25', tz='UTC'),  # Christmas
            pd.Timestamp('2014-12-26', tz='UTC'),  # Boxing Day
        ]

        for session_label in expected_holidays_2014:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        early_closes_2014 = [
            # Business day prior to Christmas
            pd.Timestamp('2014-12-24', tz='UTC'),
            # Business day prior to New Year's Day
            pd.Timestamp('2014-12-31', tz='UTC'),
        ]

        for early_close_session_label in early_closes_2014:
            self.assertIn(
                early_close_session_label,
                self.calendar.early_closes,
            )

    def test_christmas_and_boxing_day_special_cases(self):
        #    December 2010
        # Su Mo Tu We Th Fr Sa
        #           1  2  3  4
        #  5  6  7  8  9 10 11
        # 12 13 14 15 16 17 18
        # 19 20 21 22 23 24 25
        # 26 27 28 29 30 31
        #
        # Prior to 2011, the trading day before Christmas is a full
        # trading day.
        self.assertTrue(
            self.calendar.is_session(pd.Timestamp('2010-12-24', tz='UTC'))
        )
        self.assertEqual(
            self.calendar.session_close(
                pd.Timestamp('2010-12-24', tz='UTC')
            ),
            pd.Timestamp('2010-12-24 16:45', tz='NZ'),
        )

        # Saturday, but also Christmas Day.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-12-25', tz='UTC'))
        )
        # Sunday, but also Boxing Day.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-12-26', tz='UTC'))
        )
        # Since both Christmas and Boxing Day fell on the weekend, 2
        # additional holidays are observed.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-12-27', tz='UTC'))
        )
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-12-28', tz='UTC'))
        )

        #    December 2011
        # Su Mo Tu We Th Fr Sa
        #              1  2  3
        #  4  5  6  7  8  9 10
        # 11 12 13 14 15 16 17
        # 18 19 20 21 22 23 24
        # 25 26 27 28 29 30 31
        #
        # Friday the 23rd is the trading day before Christmas, so it's a
        # half day (beginning in 2011.)
        self.assertTrue(
            self.calendar.is_session(pd.Timestamp('2011-12-23', tz='UTC'))
        )
        self.assertEqual(
            self.calendar.session_close(
                pd.Timestamp('2011-12-23', tz='UTC')
            ),
            pd.Timestamp('2011-12-23 12:45', tz='NZ'),
        )

        # Saturday.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2011-12-24', tz='UTC'))
        )
        # Sunday, but also Christmas Day.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2011-12-25', tz='UTC'))
        )
        # Boxing Day.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2011-12-26', tz='UTC'))
        )
        # Since Christmas was on a Sunday, an additional holiday is
        # observed the day after Boxing Day.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2011-12-27', tz='UTC'))
        )

    def test_weekend_to_monday_holidays(self):
        #    February 2010
        # Su Mo Tu We Th Fr Sa
        #     1  2  3  4  5  6
        #  7  8  9 10 11 12 13
        # 14 15 16 17 18 19 20
        # 21 22 23 24 25 26 27
        # 28
        #
        # 2010-02-06 falls on a Saturday, so Waitangi Day is observed the
        # following Monday.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-02-08', tz='UTC'))
        )

        #      April 2010
        # Su Mo Tu We Th Fr Sa
        #              1  2  3
        #  4  5  6  7  8  9 10
        # 11 12 13 14 15 16 17
        # 18 19 20 21 22 23 24
        # 25 26 27 28 29 30
        #
        # 2010-04-25 falls on a Sunday, so Anzac Day is observed the
        # following Monday.
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-04-26', tz='UTC'))
        )
