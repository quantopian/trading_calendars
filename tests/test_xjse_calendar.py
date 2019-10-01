from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.trading_calendar import WEEKENDS
from trading_calendars.exchange_calendar_xjse import XJSEExchangeCalendar


class XJSECalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xjse'
    calendar_class = XJSEExchangeCalendar

    # The JSE is open from 09:00 to 17:00.
    MAX_SESSION_HOURS = 8

    HAVE_EARLY_CLOSES = False

    # Johannesburg does not use daylight savings time: South Africa
    # Standard Time (SAST) is observed all year.
    DAYLIGHT_SAVINGS_DATES = []

    def test_no_weekend_sessions(self):
        for session in self.calendar.all_sessions:
            self.assertNotIn(session.dayofweek, WEEKENDS)
            self.assertTrue(self.calendar.is_session(session))

    def test_2019_holidays(self):
        holidays = {pd.Timestamp(d, tz=UTC) for d in [
            '2019-01-01',  # New Year's Day
            '2019-03-21',  # Human Rights Day
            '2019-04-19',  # Good Friday
            '2019-04-22',  # Family Day
            '2019-04-27',  # Freedom Day  (falls on Saturday, not made up)
            '2019-05-01',  # Workers' Day
            '2019-05-08',  # Election Day (ad-hoc)
            '2019-06-16',  # Youth Day
            '2019-06-17',  # Youth Day (Monday make-up)
            '2019-08-09',  # National Women's Day
            '2019-09-24',  # Heritage Day
            '2019-12-16',  # Day of Reconciliation
            '2019-12-25',  # Christmas
            '2019-12-26',  # Day of Goodwill
        ]}

        year_2019 = pd.date_range(start='2019', end='2019-12-31', tz='UTC')

        for holiday in holidays:
            self.assertIn(holiday, year_2019)
            self.assertFalse(self.calendar.is_session(holiday))

        for session in self.calendar.all_sessions:
            self.assertNotIn(session, holidays)

        # Make sure we caught all the holidays.
        for day in year_2019:
            is_holiday = day in holidays
            is_weekend = day.dayofweek in WEEKENDS
            should_be_session = not is_holiday and not is_weekend
            is_session = self.calendar.is_session(day)
            self.assertEqual(should_be_session, is_session)
