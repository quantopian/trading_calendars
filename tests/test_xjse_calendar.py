from unittest import TestCase

import pandas as pd
from pytz import UTC
from nose_parameterized import parameterized

from .test_trading_calendar import NoDSTExchangeCalendarTestBase
from trading_calendars.trading_calendar import WEEKENDS
from trading_calendars.exchange_calendar_xjse import XJSEExchangeCalendar


class XJSECalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xjse'
    calendar_class = XJSEExchangeCalendar

    # The JSE is open from 09:00 to 17:00.
    MAX_SESSION_HOURS = 8

    HAVE_EARLY_CLOSES = False

    def test_no_weekend_sessions(self):
        for session in self.calendar.all_sessions:
            self.assertNotIn(session.dayofweek, WEEKENDS, session)
            self.assertTrue(self.calendar.is_session(session), session)

    @parameterized.expand([
        ('2019-01-01', '2019-12-31', [
            '2019-01-01',  # New Year's Day
            '2019-03-21',  # Human Rights Day
            '2019-04-19',  # Good Friday
            '2019-04-22',  # Family Day
            '2019-04-27',  # Freedom Day (falls on Saturday, not made up)
            '2019-05-01',  # Workers' Day
            '2019-05-08',  # Election Day (ad-hoc)
            '2019-06-16',  # Youth Day
            '2019-06-17',  # Youth Day (Monday make-up)
            '2019-08-09',  # National Women's Day
            '2019-09-24',  # Heritage Day
            '2019-12-16',  # Day of Reconciliation
            '2019-12-25',  # Christmas
            '2019-12-26',  # Day of Goodwill
        ]),
        ('2018-01-01', '2018-12-31', [
            '2018-01-01',  # New Year's Day
            '2018-03-21',  # Human Rights Day
            '2018-03-30',  # Good Friday
            '2018-04-02',  # Family Day
            '2018-04-27',  # Freedom Day
            '2018-05-01',  # Workers' Day
            '2018-06-16',  # Youth Day (falls on Saturday, not made up)
            '2018-08-09',  # National Women's Day
            '2018-09-24',  # Heritage Day
            '2018-12-16',  # Day of Reconciliation
            '2018-12-17',  # Day of Reconciliation (Monday make-up)
            '2018-12-25',  # Christmas
            '2018-12-26',  # Day of Goodwill
        ]),
        ('2016-01-01', '2016-12-31', [
            '2016-01-01',  # New Year's Day
            '2016-03-21',  # Human Rights Day
            '2016-03-25',  # Good Friday
            '2016-03-28',  # Family Day
            '2016-04-27',  # Freedom Day
            '2016-05-01',  # Workers' Day
            '2016-05-02',  # Workers' Day (Monday make-up)
            '2016-06-16',  # Youth Day
            '2016-08-03',  # Election Day
            '2016-08-09',  # National Women's Day
            '2016-09-24',  # Heritage Day (falls on Saturday, not made up)
            '2016-12-16',  # Day of Reconciliation
            '2016-12-25',  # Christmas
            '2016-12-26',  # Christmas (Monday make-up)
            '2016-12-27',  # Day of Goodwill (Ad-hoc make-up observance)
        ]),
    ])
    def test_holidays_in_date_range(self, start, end, holiday_dates):
        holidays = {pd.Timestamp(d, tz=UTC) for d in holiday_dates}
        date_range = pd.date_range(start=start, end=end, tz='UTC')

        for holiday in holidays:
            self.assertIn(holiday, date_range)
            self.assertFalse(self.calendar.is_session(holiday), holiday)

        for session in self.calendar.all_sessions:
            self.assertNotIn(session, holidays)

        # Make sure we caught all the holidays.
        for day in date_range:
            is_holiday = day in holidays
            is_weekend = day.dayofweek in WEEKENDS
            should_be_session = not is_holiday and not is_weekend
            is_session = self.calendar.is_session(day)
            self.assertEqual(should_be_session, is_session, day)
