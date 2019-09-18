from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.exchange_calendar_xmex import XMEXExchangeCalendar

from .test_trading_calendar import ExchangeCalendarTestBase


class XMEXCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xmex'
    calendar_class = XMEXExchangeCalendar

    # The XMEX is open from 8:30AM to 3:00PM.
    MAX_SESSION_HOURS = 6.5

    # In 2019 in Mexico City, daylight savings began on April 7th and ended on
    # October 27th.
    DAYLIGHT_SAVINGS_DATES = ['2019-04-08', '2019-10-28']

    HAVE_EARLY_CLOSES = False

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-02-04', tz=UTC),  # Constitution Day
            pd.Timestamp('2019-03-18', tz=UTC),  # Juarez's Birthday
            pd.Timestamp('2019-04-18', tz=UTC),  # Maundy Thursday
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-09-16', tz=UTC),  # Independence Day
            pd.Timestamp('2018-11-02', tz=UTC),  # All Souls' Day
            pd.Timestamp('2019-11-18', tz=UTC),  # Revolution Day
            pd.Timestamp('2019-12-12', tz=UTC),  # Banking Holiday
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # All holidays falling on a weekend should not be made up, so verify
        # that the surrounding Fridays/Mondays are trading days.
        expected_sessions = [
            # New Year's Day on a Sunday.
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
            # Constitution Day (February 5th) on a Sunday, prior to 2007.
            pd.Timestamp('2006-02-03', tz=UTC),
            pd.Timestamp('2006-02-06', tz=UTC),
            # Juarez's Birthday (March 21st) on a Sunday, prior to 2007.
            pd.Timestamp('2004-03-19', tz=UTC),
            pd.Timestamp('2004-03-22', tz=UTC),
            # Labour Day (May 1st) on a Sunday.
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Independence Day (September 16th) on a Sunday.
            pd.Timestamp('2018-09-14', tz=UTC),
            pd.Timestamp('2018-09-17', tz=UTC),
            # All Souls' Day (November 2nd) on a Saturday.
            pd.Timestamp('2019-11-01', tz=UTC),
            pd.Timestamp('2019-11-04', tz=UTC),
            # Revolution Day (November 20th) on a Sunday, prior to 2007.
            pd.Timestamp('2005-11-18', tz=UTC),
            pd.Timestamp('2005-11-21', tz=UTC),
            # Banking Holiday (December 12th) on a Saturday.
            pd.Timestamp('2015-12-11', tz=UTC),
            pd.Timestamp('2015-12-14', tz=UTC),
            # Christmas on a Sunday.
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-26', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_adhoc_holidays(self):
        # Bicentennial Celebration.
        self.assertNotIn(
            pd.Timestamp('2010-09-17', tz=UTC),
            self.calendar.all_sessions,
        )

    def test_rule_changes(self):
        all_sessions = self.calendar.all_sessions

        # Prior to 2007 Constitution Day was observed strictly on February 5th.
        # From 2007 onward it is always the first Monday of February.
        #
        # In 2006, February 5th was a Sunday, so Monday the 6th should be a
        # trading day.
        self.assertIn(pd.Timestamp('2006-02-06', tz=UTC), all_sessions)
        # In 2004, February 5th was a Thursday, so that day should be a holiday
        # and Monday the 2nd should be a trading day.
        self.assertIn(pd.Timestamp('2004-02-02', tz=UTC), all_sessions)
        self.assertNotIn(pd.Timestamp('2004-02-05', tz=UTC), all_sessions)
        # In 2008, February 5th is a Tuesday, so now that should not be a
        # holiday and instead Monday the 4th should be.
        self.assertNotIn(pd.Timestamp('2008-02-04', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2008-02-05', tz=UTC), all_sessions)

        # Prior to 2007 Juarez's Birthday was observed strictly on March 21st.
        # From 2007 onward it is always the third Monday of March.
        #
        # In 2006, March 21st was a Tuesday, so that day should be a holiday
        # and Monday the 20th should be a trading day.
        self.assertIn(pd.Timestamp('2006-03-20', tz=UTC), all_sessions)
        self.assertNotIn(pd.Timestamp('2006-03-21', tz=UTC), all_sessions)
        # In 2007, March 21st was a Wednesday, so that day should no longer be
        # a holiday and instead Monday the 19th should be.
        self.assertNotIn(pd.Timestamp('2007-03-19', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2007-03-21', tz=UTC), all_sessions)

        # Prior to 2007 Revolution Day was observed strictly on November 20th.
        # From 2007 onward it is always the third Monday of November.
        #
        # In 2003, November 20th was a Thursday, so that day should be a
        # holiday and Monday the 17th should be a trading day.
        self.assertIn(pd.Timestamp('2003-11-17', tz=UTC), all_sessions)
        self.assertNotIn(pd.Timestamp('2003-11-20', tz=UTC), all_sessions)
        # In 2007, November 20th was a Tuesday, so that day should no longer be
        # a holiday and instead Monday the 19th should be.
        self.assertNotIn(pd.Timestamp('2007-11-19', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2007-11-20', tz=UTC), all_sessions)

    def test_all_souls_day(self):
        """
        All Souls' Day did not become a market holiday until 2006.
        """
        all_sessions = self.calendar.all_sessions

        self.assertIn(pd.Timestamp('2005-11-02', tz=UTC), all_sessions)
        self.assertNotIn(pd.Timestamp('2006-11-02', tz=UTC), all_sessions)
