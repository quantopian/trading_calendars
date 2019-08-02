from unittest import TestCase

from .test_trading_calendar import ExchangeCalendarTestBase
from .test_utils import T
from trading_calendars.exchange_calendar_xnse import XNSExchangeCalendar


class XNSECalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xnse'
    calendar_class = XNSExchangeCalendar

    # BSE is open from 9:15 am to 3:30 pm
    MAX_SESSION_HOURS = 6.25

    HAVE_EARLY_CLOSES = False

    def test_normal_year(self):
        expected_holidays_2019 = [
            T('2019-01-26'),
            T('2019-02-13'),
            T('2019-02-14'),
            T('2019-03-02'),
            T('2019-03-04'),
            T('2019-03-21'),
            T('2019-03-29'),
            T('2019-04-04'),
            T('2019-04-13'),
            T('2019-04-14'),
            T('2019-04-17'),
            T('2019-04-19'),
            T('2019-04-29'),
            T('2019-05-01'),
            T('2019-06-05'),
            T('2019-08-12'),
            T('2019-08-15'),
            T('2019-09-02'),
            T('2019-09-10'),
            T('2019-10-02'),
            T('2019-10-08'),
            T('2019-10-27'),
            T('2019-10-28'),
            T('2019-11-12'),
            T('2019-12-25'),
        ]

        for session_label in expected_holidays_2019:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_constrain_construction_dates(self):
        # the XNSE calendar currently goes from 1997 to 2020, inclusive.
        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('1996-12-31'), T('1998-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XNSE holidays are only recorded back to 1997,'
                ' cannot instantiate the XNSE calendar back to 1996.'
            )
        )

        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('1998-01-01'), T('2021-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XNSE holidays are only recorded to 2020,'
                ' cannot instantiate the XNSE calendar for 2021.'
            )
        )
