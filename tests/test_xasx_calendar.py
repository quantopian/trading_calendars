from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xasx import XASXExchangeCalendar


class XASXCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xasx'
    calendar_class = XASXExchangeCalendar

    # The XASX is open from 10:00 am to 4:00 pm.
    MAX_SESSION_HOURS = 6

    def test_normal_year(self):
        expected_holidays = [
            pd.Timestamp('2018-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2018-01-26', tz=UTC),  # Australia Day
            pd.Timestamp('2018-03-30', tz=UTC),  # Good Friday
            pd.Timestamp('2018-04-02', tz=UTC),  # Easter Monday
            pd.Timestamp('2018-04-25', tz=UTC),  # Anzac Day
            pd.Timestamp('2018-06-11', tz=UTC),  # Queen's Birthday
            pd.Timestamp('2018-12-25', tz=UTC),  # Christmas
            pd.Timestamp('2018-12-26', tz=UTC),  # Boxing Day
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        early_closes = [
            pd.Timestamp('2018-12-24', tz=UTC),  # Day before Christmas
            pd.Timestamp('2018-12-31', tz=UTC),  # Day before New Year's
        ]

        for early_close_session_label in early_closes:
            self.assertIn(
                early_close_session_label,
                self.calendar.early_closes,
            )

    def test_holidays_fall_on_weekend(self):
        """
        Holidays falling on a weekend should be made up on the next weekday.

        Anzac Day is observed on the following Monday only when falling
        on a Sunday. In years where Anzac Day falls on a Saturday, there
        is no make-up.

        Christmas/Boxing Day are special cases, whereby if Christmas is a
        Saturday and Boxing Day is a Sunday, the next Monday and Tuesday will
        be holidays. If Christmas is a Sunday and Boxing Day is a Monday then
        Monday and Tuesday will still both be holidays.
        """
        expected_holidays = [
            # New Year's Day on a Sunday, observed on Monday.
            pd.Timestamp('2017-01-02', tz=UTC),
            # Australia Day on a Sunday, observed on Monday (2010 and after).
            pd.Timestamp('2014-01-27', tz=UTC),
            # Anzac Day on a Sunday, observed on Monday.
            pd.Timestamp('2010-04-26', tz=UTC),
            # Christmas on a Sunday, Boxing Day on Monday.
            pd.Timestamp('2016-12-26', tz=UTC),
            pd.Timestamp('2016-12-27', tz=UTC),
            # Christmas on a Saturday, Boxing Day on Sunday.
            pd.Timestamp('2010-12-27', tz=UTC),
            pd.Timestamp('2010-12-28', tz=UTC),
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        expected_sessions = [
            # Anzac Day on a Saturday, does not have a make-up.
            pd.Timestamp('2015-04-27', tz=UTC),
            # Anzac Day on a Saturday, does not have a make-up (prior
            # to 2010).
            pd.Timestamp('2004-04-26', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)

    def test_half_days(self):
        half_days = [
            # In 2018, the last trading days before Christmas and New Year's
            # are on Mondays, so they should be half days.
            pd.Timestamp('2018-12-24', tz='Australia/Sydney'),
            pd.Timestamp('2018-12-31', tz='Australia/Sydney'),
            # In 2017, Christmas and New Year's fell on Mondays, so the last
            # trading days before them were Fridays, which should be half days.
            pd.Timestamp('2017-12-22', tz='Australia/Sydney'),
            pd.Timestamp('2017-12-29', tz='Australia/Sydney'),
            # In 2016, Christmas and New Year's fell on Sundays, so the last
            # trading days before them were Fridays, which should be half days.
            pd.Timestamp('2016-12-23', tz='Australia/Sydney'),
            pd.Timestamp('2016-12-30', tz='Australia/Sydney'),
            # 2010 is the first year we expect the half day rules to take
            # effect.
            pd.Timestamp('2010-12-24', tz='Australia/Sydney'),
            pd.Timestamp('2010-12-31', tz='Australia/Sydney'),
        ]
        full_days = [
            # In 2009 the half day rules should not be in effect yet.
            pd.Timestamp('2009-12-24', tz='Australia/Sydney'),
            pd.Timestamp('2009-12-31', tz='Australia/Sydney'),
        ]

        for half_day in half_days:
            half_day_close_time = self.calendar.next_close(half_day)
            self.assertEqual(
                half_day_close_time.tz_convert('Australia/Sydney'),
                half_day + pd.Timedelta(hours=14, minutes=10),
            )
        for full_day in full_days:
            full_day_close_time = self.calendar.next_close(full_day)
            self.assertEqual(
                full_day_close_time.tz_convert('Australia/Sydney'),
                full_day + pd.Timedelta(hours=16),
            )
