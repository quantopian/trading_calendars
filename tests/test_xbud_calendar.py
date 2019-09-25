from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.trading_calendar import (
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
)
from trading_calendars.exchange_calendar_xbud import XBUDExchangeCalendar


class XBUDCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xbud'
    calendar_class = XBUDExchangeCalendar

    # The XBUD is open from 9:00 to 5:00PM
    MAX_SESSION_HOURS = 8

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2018-03-26', '2018-10-29']

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-03-15', tz=UTC),  # National Holiday
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-04-22', tz=UTC),  # Easter Monday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-06-10', tz=UTC),  # Whit Monday
            pd.Timestamp('2019-08-20', tz=UTC),  # St. Stephen's Day
            pd.Timestamp('2019-10-23', tz=UTC),  # National Holiday
            pd.Timestamp('2019-11-01', tz=UTC),  # All Saint's Day
            pd.Timestamp('2019-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-26', tz=UTC),  # Second Day of Christmas
            pd.Timestamp('2019-12-31', tz=UTC),  # New Year's Eve
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
            # National Holiday on Sunday, March 15th
            pd.Timestamp('2015-03-13', tz=UTC),
            pd.Timestamp('2015-03-16', tz=UTC),
            # Labour Day on Sunday, May 1st
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # St. Stephen's Day on Saturday, August 20th
            pd.Timestamp('2016-08-19', tz=UTC),
            pd.Timestamp('2016-08-22', tz=UTC),
            # National Holiday on Sunday, Oct 23rd
            pd.Timestamp('2016-10-21', tz=UTC),
            pd.Timestamp('2016-10-24', tz=UTC),
            # All Saint's Day on Sunday, Nov 1
            pd.Timestamp('2015-10-30', tz=UTC),
            pd.Timestamp('2015-11-02', tz=UTC),
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
            # New Year's Eve on Saturday, Dec 31
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_four_day_weekends(self):
        all_sessions = self.calendar.all_sessions

        # For most holidays, falling on a Tuesday or Thursday adds
        # a holiday on Monday or Friday, respectively, creating a four
        # day weekend.  This test makes sure the extra day gets added
        expected_holidays = [
            # New Years Day on Thursday, Jan 1
            pd.Timestamp('2015-01-01', tz=UTC),
            pd.Timestamp('2015-01-02', tz=UTC),
            # National Holiday on Tuesday, March 15
            pd.Timestamp('2016-03-15', tz=UTC),
            pd.Timestamp('2016-03-14', tz=UTC),
            # Labour Day on Tuesday, May 1
            pd.Timestamp('2018-05-01', tz=UTC),
            pd.Timestamp('2018-04-30', tz=UTC),
            # St. Stephen's Day on Thursday, Aug 20
            pd.Timestamp('2015-08-20', tz=UTC),
            pd.Timestamp('2015-08-21', tz=UTC),
            # National Holiday on Thursday, Oct 23
            pd.Timestamp('2014-10-23', tz=UTC),
            pd.Timestamp('2014-10-24', tz=UTC),
            # All Saint's Day on Tuesday, Nov 1
            pd.Timestamp('2016-11-01', tz=UTC),
            pd.Timestamp('2016-10-31', tz=UTC),
            # Second Day of Christmas on Thursday, Dec 26
            pd.Timestamp('2019-12-26', tz=UTC),
            pd.Timestamp('2019-12-27', tz=UTC),
        ]

        # Christmas Eve and New Years Eve do not use four day weekend
        # rule.  This test makes sure the Monday before each is a
        # trading day.
        expected_sessions = [
            # Dec 23 Mondays
            pd.Timestamp('2002-12-23', tz=UTC),
            pd.Timestamp('2013-12-23', tz=UTC),
            pd.Timestamp('2019-12-23', tz=UTC),
            # Dec 30 Mondays
            pd.Timestamp('2002-12-30', tz=UTC),
            pd.Timestamp('2013-12-30', tz=UTC),
            pd.Timestamp('2019-12-30', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_new_years_eve(self):
        """
        New Year's Eve became a holiday in 2011.  Before that it was not
        a holiday unless it fell on a Monday (because of New Year's Day
        four day weekend rule)
        """
        all_sessions = self.calendar.all_sessions
        session_days = (TUESDAY, WEDNESDAY, THURSDAY, FRIDAY)

        for year in range(2000, 2011):
            ts = pd.Timestamp('{}-12-31'.format(year), tz=UTC)
            if ts.weekday() in session_days:
                self.assertIn(ts, all_sessions)

        for year in range(2011, 2020):
            self.assertNotIn(
                pd.Timestamp('{}-12-31'.format(year), tz=UTC),
                all_sessions
            )

    def test_second_day_of_christmas(self):
        """
        2002-12-27 is not observed as a holiday, even though it falls
        on the Friday after a holiday (Second Day of Christmas).
        All following Dec 27 that fall on a Friday are holidays.
        """
        all_sessions = self.calendar.all_sessions

        # Trading day in 2002
        self.assertIn(pd.Timestamp('2002-12-27', tz=UTC), all_sessions)

        # Holiday in 2013, 2019
        self.assertNotIn(pd.Timestamp('2013-12-27', tz=UTC), all_sessions)
        self.assertNotIn(pd.Timestamp('2019-12-27', tz=UTC), all_sessions)
