from unittest import TestCase

from .test_trading_calendar import ExchangeCalendarTestBase
from .test_utils import T
from trading_calendars.exchange_calendar_xbom import XBOMExchangeCalendar


class XBOMCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xbom'
    calendar_class = XBOMExchangeCalendar

    # BSE is open from 9:15 am to 3:30 pm
    MAX_SESSION_HOURS = 6.25

    HAVE_EARLY_CLOSES = False

    def test_normal_year(self):
        expected_holidays_2017 = [
            T('2017-01-26'),
            T('2017-02-24'),
            T('2017-03-13'),
            T('2017-04-04'),
            T('2017-04-14'),
            T('2017-05-01'),
            T('2017-06-26'),
            T('2017-08-15'),
            T('2017-08-25'),
            T('2017-10-02'),
            T('2017-10-20'),
            T('2017-12-25'),
        ]

        for session_label in expected_holidays_2017:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_constrain_construction_dates(self):
        # the XBOM calendar currently goes from 1997 to 2020, inclusive.
        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('1996-12-31'), T('1998-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XBOM holidays are only recorded back to 1997,'
                ' cannot instantiate the XBOM calendar back to 1996.'
            )
        )

        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('1998-01-01'), T('2021-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XBOM holidays are only recorded to 2020,'
                ' cannot instantiate the XBOM calendar for 2021.'
            )
        )
