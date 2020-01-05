from unittest import TestCase

from .test_trading_calendar import NoDSTExchangeCalendarTestBase
from .test_utils import T

from trading_calendars.exchange_calendar_xkrx import XKRXExchangeCalendar


class XKRXCalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xkrx'
    calendar_class = XKRXExchangeCalendar

    # Korea exchange is open from 9am to 3:30pm
    MAX_SESSION_HOURS = 6.5
    HAVE_EARLY_CLOSES = False

    def test_normal_year(self):
        expected_holidays_2017 = [
            T("2017-01-27"),
            T("2017-01-30"),
            T("2017-03-01"),
            T("2017-05-01"),
            T("2017-05-03"),
            T("2017-05-05"),
            T("2017-05-09"),
            T("2017-06-06"),
            T("2017-08-15"),
            T("2017-10-02"),
            T("2017-10-03"),
            T("2017-10-04"),
            T("2017-10-05"),
            T("2017-10-06"),
            T("2017-10-09"),
            T("2017-12-25"),
            T("2017-12-29"),
        ]

        for session_label in expected_holidays_2017:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_constrain_construction_dates(self):
        # the XKRX calendar currently goes from 1986 to 2020, inclusive.
        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('1985-12-31'), T('2005-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XKRX holidays are only recorded back to 1986,'
                ' cannot instantiate the XKRX calendar back to 1985.'
            )
        )

        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('2005-01-01'), T('2021-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XKRX holidays are only recorded to 2020,'
                ' cannot instantiate the XKRX calendar for 2021.'
            )
        )

    def test_holidays_fall_on_weekend(self):
        # Holidays below falling on a weekend should
        # not be made up during the week.
        expected_holidays = [
            # Memorial Day on Sunday
            T('2010-06-06'),
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        expected_sessions = [
            # National Foundation Day on a Saturday, so check
            # Friday and Monday surrounding it
            T('2015-10-02'),
            T('2015-10-05'),
            # Christmas Day on a Saturday
            # Same as Foundation Day idea
            T('2010-12-24'),
            T('2010-12-27'),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)

        # Holidays below falling on a weekend should
        # be made up during the week.
        expected_holidays = [
            # Chuseok (Korean Thanksgiving) falls on Sunday through Wednesday
            # but Wednesday (below) the exchange is closed; meant to give
            # people an extra day off rather than letting the Sunday count
            T('2014-09-10'),
            # Chuseok (Korean Thanksgiving) falls on Saturday through Tuesday
            # but Tuesday (below) the exchange is closed; meant to give
            # people an extra day off rather than letting the Saturday count
            T('2015-09-29'),
            # Chuseok again; similar reasoning as above
            T('2017-10-06'),
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_hangeul_day_2013_onwards(self):

        expected_hangeul_day = T('2013-10-09')
        unexpected_hangeul_day = T('2012-10-09')

        self.assertTrue(expected_hangeul_day not in self.calendar.all_sessions)
        self.assertTrue(
            unexpected_hangeul_day in self.calendar.all_sessions
        )
