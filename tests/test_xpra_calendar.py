from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xpra import XPRAExchangeCalendar


class XPRACalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xpra'
    calendar_class = XPRAExchangeCalendar

    # The XPRA is open from 9:00 to 4:20PM
    MAX_SESSION_HOURS = 7.34

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2018-03-26', '2018-10-29']

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-04-22', tz=UTC),  # Easter Monday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-05-08', tz=UTC),  # Liberation Day
            pd.Timestamp('2019-07-05', tz=UTC),  # St. Cyril/Methodius Day
            pd.Timestamp('2018-07-06', tz=UTC),  # Jan Hus Day
            pd.Timestamp('2018-09-28', tz=UTC),  # Czech Statehood Day
            pd.Timestamp('2019-10-28', tz=UTC),  # Independence Day
            pd.Timestamp('2017-11-17', tz=UTC),  # Freedom/Democracy Day
            pd.Timestamp('2019-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-26', tz=UTC),  # Second Day of Christmas
            pd.Timestamp('2019-12-31', tz=UTC),  # Exchange Holiday
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
            # Labour Day on Sunday, May 1st
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Liberation Day on Sunday, May 8th
            pd.Timestamp('2016-05-06', tz=UTC),
            pd.Timestamp('2016-05-09', tz=UTC),
            # Saints Cyril and Methodius Day on Saturday, Jul 5th
            pd.Timestamp('2014-07-04', tz=UTC),
            pd.Timestamp('2014-07-07', tz=UTC),
            # Jan Hus Day on Saturday, Jul 6th
            #   Note: 7/5/2019 is a holiday
            pd.Timestamp('2019-07-04', tz=UTC),
            pd.Timestamp('2019-07-08', tz=UTC),
            # Czech Statehood Day on Saturday, Sept 28th
            pd.Timestamp('2019-09-27', tz=UTC),
            pd.Timestamp('2019-09-30', tz=UTC),
            # Independence Day on Sunday, Oct 28th
            pd.Timestamp('2018-10-26', tz=UTC),
            pd.Timestamp('2018-10-29', tz=UTC),
            # Struggle for Freedom and Democracy Day on Sunday, Nov 17
            pd.Timestamp('2019-11-15', tz=UTC),
            pd.Timestamp('2019-11-18', tz=UTC),
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
            # Exchange Holiday on Saturday, Dec 31
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_good_friday(self):
        all_sessions = self.calendar.all_sessions

        # Good Friday is a holiday from 2013-present (inclusive),
        # so this test ensures Good Friday prior to 2013 is a valid
        # session, and in 2013 and beyond is a holiday.
        expected_sessions = [
            # Good Friday in 2010
            pd.Timestamp('2010-04-02', tz=UTC),
            # Good Friday in 2011
            pd.Timestamp('2011-04-22', tz=UTC),
            # Good Friday in 2012
            pd.Timestamp('2012-04-06', tz=UTC),
        ]

        expected_holidays = [
            # Good Friday in 2013
            pd.Timestamp('2013-03-29', tz=UTC),
            # Good Friday in 2014
            pd.Timestamp('2014-04-18', tz=UTC),
            # Good Friday in 2015
            pd.Timestamp('2015-04-03', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_adhoc_holidays(self):
        all_sessions = self.calendar.all_sessions

        # 3 adhoc holidays to test
        expected_holidays = [
            # Extreme Flooding
            pd.Timestamp('2002-08-14', tz=UTC),
            # Restoration of the Czech Independence Day
            pd.Timestamp('2004-01-02', tz=UTC),
            pd.Timestamp('2005-01-03', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
