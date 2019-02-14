from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from .test_utils import T
from trading_calendars.exchange_calendar_xshg import XSHGExchangeCalendar


class XSHGCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xshg'
    calendar_class = XSHGExchangeCalendar

    # Shanghai stock exchange is open from 9:30 am to 3pm
    # (for now, ignoring lunch break)
    MAX_SESSION_HOURS = 5.5

    HAVE_EARLY_CLOSES = False

    MINUTE_INDEX_TO_SESSION_LABELS_END = pd.Timestamp('2011-04-07', tz=UTC)

    def test_normal_year(self):
        expected_holidays_2017 = [
            T("2017-01-02"),
            T("2017-01-27"),
            T("2017-01-30"),
            T("2017-01-31"),
            T("2017-02-01"),
            T("2017-02-02"),
            T("2017-04-03"),
            T("2017-04-04"),
            T("2017-05-01"),
            T("2017-05-29"),
            T("2017-05-30"),
            T("2017-10-02"),
            T("2017-10-03"),
            T("2017-10-04"),
            T("2017-10-05"),
            T("2017-10-06"),
        ]

        for session_label in expected_holidays_2017:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_constrain_construction_dates(self):
        # the XSHG calendar currently goes from 1999 to 2025, inclusive.
        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('1998-12-31'), T('2005-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XSHG holidays are only recorded back to 1999,'
                ' cannot instantiate the XSHG calendar back to 1998.'
            )
        )

        with self.assertRaises(ValueError) as e:
            self.calendar_class(T('2005-01-01'), T('2026-01-01'))

        self.assertEqual(
            str(e.exception),
            (
                'The XSHG holidays are only recorded to 2025,'
                ' cannot instantiate the XSHG calendar for 2026.'
            )
        )
