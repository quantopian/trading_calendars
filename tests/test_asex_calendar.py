from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_asex import ASEXExchangeCalendar


class ASEXCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'asex'
    calendar_class = ASEXExchangeCalendar

    # The ASEX is open from 10:00 to 5:20PM on its longest trading day
    MAX_SESSION_HOURS = 7.33

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2018-03-26', '2018-10-29']

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2017-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2019-03-11', tz=UTC),  # Orthodox Ash Monday
            pd.Timestamp('2019-03-25', tz=UTC),  # National Holiday
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-04-22', tz=UTC),  # Easter Monday
            pd.Timestamp('2019-04-26', tz=UTC),  # Orthodox Good Friday
            pd.Timestamp('2019-04-29', tz=UTC),  # Orthodox Easter Monday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-06-17', tz=UTC),  # Orthodox Whit Monday
            pd.Timestamp('2019-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2019-10-28', tz=UTC),  # National Holiday
            pd.Timestamp('2019-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-26', tz=UTC),  # Second Day of Christmas
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # All holidays that fall on a weekend should not be made
        # up, so ensure surrounding days are open market
        expected_sessions = [
            # New Years Day on Sunday, Jan 1st
            pd.Timestamp('2011-12-30', tz=UTC),
            pd.Timestamp('2012-01-02', tz=UTC),
            # Epiphany on Sunday, Jan 6th
            pd.Timestamp('2019-01-04', tz=UTC),
            pd.Timestamp('2019-01-07', tz=UTC),
            # National Holiday on Sunday, Mar 25th
            pd.Timestamp('2018-03-23', tz=UTC),
            pd.Timestamp('2018-03-26', tz=UTC),
            # Labour Day on Sunday, May 1st
            pd.Timestamp('2011-04-29', tz=UTC),
            pd.Timestamp('2011-05-02', tz=UTC),
            # Assumption Day on Saturday, Aug 15th
            pd.Timestamp('2015-08-14', tz=UTC),
            pd.Timestamp('2015-08-17', tz=UTC),
            # National Holiday on Saturday, Oct 28
            pd.Timestamp('2015-10-27', tz=UTC),
            pd.Timestamp('2015-10-30', tz=UTC),
            # Christmas Eve on a Sunday
            #   Note: 25th, 26th both holidays
            pd.Timestamp('2017-12-22', tz=UTC),
            pd.Timestamp('2017-12-27', tz=UTC),
            # Christmas on a Sunday
            #   Note: 26th a holiday
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-27', tz=UTC),
            # 2nd Day of Christmas on Saturday, Dec 26
            #   Note: 25th, 24th both holidays
            pd.Timestamp('2015-12-23', tz=UTC),
            pd.Timestamp('2015-12-28', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_orthodox_easter(self):
        """
        The Athens Stock Exchange observes Orthodox (or Eastern) Easter,
        as well as Western Easter.  All holidays that are tethered to
        Easter (i.e. Whit Monday, Good Friday, etc.), are relative to
        Orthodox Easter.  This test checks that Orthodox Easter and all
        related holidays are correct.
        """
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            # Some Orthodox Easter dates
            pd.Timestamp('2005-05-01', tz=UTC),
            pd.Timestamp('2006-04-23', tz=UTC),
            pd.Timestamp('2009-04-19', tz=UTC),
            pd.Timestamp('2013-05-05', tz=UTC),
            pd.Timestamp('2015-04-12', tz=UTC),
            pd.Timestamp('2018-04-08', tz=UTC),
            # Some Orthodox Good Friday dates
            pd.Timestamp('2002-05-03', tz=UTC),
            pd.Timestamp('2005-04-29', tz=UTC),
            pd.Timestamp('2008-04-25', tz=UTC),
            pd.Timestamp('2009-04-17', tz=UTC),
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2017-04-14', tz=UTC),
            # Some Orthodox Whit Monday dates
            pd.Timestamp('2002-06-24', tz=UTC),
            pd.Timestamp('2005-06-20', tz=UTC),
            pd.Timestamp('2006-06-12', tz=UTC),
            pd.Timestamp('2008-06-16', tz=UTC),
            pd.Timestamp('2013-06-24', tz=UTC),
            pd.Timestamp('2016-06-20', tz=UTC),
            # Some Orthodox Ash Monday dates
            pd.Timestamp('2002-03-18', tz=UTC),
            pd.Timestamp('2005-03-14', tz=UTC),
            pd.Timestamp('2007-02-19', tz=UTC),
            pd.Timestamp('2011-03-07', tz=UTC),
            pd.Timestamp('2014-03-03', tz=UTC),
            pd.Timestamp('2018-02-19', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_debt_crisis_closure(self):
        """
        In 2015, the debt crisis in Greece closed the markets for about
        a month.  This test makes sure there were no trading days during
        that time.
        """
        all_sessions = self.calendar.all_sessions
        closed_dates = pd.date_range('2015-06-29', '2015-07-31')

        for date in closed_dates:
            self.assertNotIn(date, all_sessions)

    def test_adhoc_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2002-05-07', tz=UTC),  # Market Holiday
            pd.Timestamp('2004-08-13', tz=UTC),  # Assumption Day makeup
            pd.Timestamp('2008-03-04', tz=UTC),  # Worker strikes
            pd.Timestamp('2008-03-05', tz=UTC),  # Worker strikes
            pd.Timestamp('2013-05-07', tz=UTC),  # May Day strikes
            pd.Timestamp('2014-12-31', tz=UTC),  # New Year's Eve
            pd.Timestamp('2016-05-03', tz=UTC),  # Labour Day makeup
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_close_time_change(self):
        """
        On Sept 29, 2008, the ASEX decided to push its close time back
        from 5:00PM to 5:20PM to close the time gap with Wall Street.
        """
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2006-09-29', tz=UTC)),
            pd.Timestamp('2006-09-29 17:00', tz='Europe/Athens'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2008-09-26', tz=UTC)),
            pd.Timestamp('2008-09-26 17:00', tz='Europe/Athens'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2008-09-29', tz=UTC)),
            pd.Timestamp('2008-09-29 17:20', tz='Europe/Athens'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2008-09-30', tz=UTC)),
            pd.Timestamp('2008-09-30 17:20', tz='Europe/Athens'),
        )
