from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.exchange_calendar_xbkk import XBKKExchangeCalendar

from .test_trading_calendar import NoDSTExchangeCalendarTestBase


class XBKKCalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xbkk'
    calendar_class = XBKKExchangeCalendar

    # The XBKK is open from 10:00AM to 4:30PM.
    MAX_SESSION_HOURS = 6.5

    HAVE_EARLY_CLOSES = False

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-02-19', tz=UTC),  # Makha Bucha
            pd.Timestamp('2018-04-06', tz=UTC),  # Chakri Memorial Day
            pd.Timestamp('2016-04-13', tz=UTC),  # Songkran Festival
            pd.Timestamp('2016-04-14', tz=UTC),  # Songkran Festival
            pd.Timestamp('2016-04-15', tz=UTC),  # Songkran Festival
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2016-05-05', tz=UTC),  # Coronation Day
            pd.Timestamp('2019-05-20', tz=UTC),  # Vesak
            pd.Timestamp('2019-06-03', tz=UTC),  # Queen's Birthday
            pd.Timestamp('2019-07-16', tz=UTC),  # Asanha Bucha
            pd.Timestamp('2017-07-28', tz=UTC),  # King's Birthday
            pd.Timestamp('2019-08-12', tz=UTC),  # Queen Mother's Birthday
            pd.Timestamp('2017-10-13', tz=UTC),  # Passing of King Bhumibol
            pd.Timestamp('2019-10-23', tz=UTC),  # Chulalongkorn Day
            pd.Timestamp('2019-12-05', tz=UTC),  # King Bhumibol's Birthday
            pd.Timestamp('2019-12-10', tz=UTC),  # Thailand Constitution Day
            pd.Timestamp('2019-12-31', tz=UTC),  # New Year's Eve
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Most holidays falling on a weekend should be observed the following
        # Monday.
        expected_holidays = [
            # New Year's Eve on a Saturday and New Year's Day on a Sunday. In
            # this case both holidays are made up, so the following Monday and
            # Tuesday should both be holidays.
            pd.Timestamp('2017-01-02', tz=UTC),
            pd.Timestamp('2017-01-03', tz=UTC),
            # New Year's Day on a Saturday.
            pd.Timestamp('2011-01-03', tz=UTC),
            # Chakri Memorial Day (April 6th) on a Saturday.
            pd.Timestamp('2019-04-08', tz=UTC),
            # Songkran Festival Days 2 and 3 (April 14th and 15th) on a
            # Saturday and Sunday. In this case, unlike the New Year's case,
            # only the Monday is a make up holiday, not the Tuesday.
            pd.Timestamp('2018-04-16', tz=UTC),
            # Labour Day (May 1st) on a Sunday.
            pd.Timestamp('2016-05-02', tz=UTC),
            # Coronation Day (May 5th) on a Sunday.
            pd.Timestamp('2019-05-06', tz=UTC),
            # Coronation Day (May 4th) on a Sunday.
            pd.Timestamp('2014-05-05', tz=UTC),
            # King's Birthday (July 28th) on a Sunday.
            pd.Timestamp('2019-07-29', tz=UTC),
            # Queen Mother's Birthday (August 12th) on a Sunday.
            pd.Timestamp('2018-08-13', tz=UTC),
            # The Passing of King Bhumibol (October 13th) on a Sunday.
            pd.Timestamp('2019-10-14', tz=UTC),
            # Chulalongkorn Day (October 23rd) on a Sunday.
            pd.Timestamp('2016-10-24', tz=UTC),
            # King Bhumibol's Birthday (December 5th) on a Saturday.
            pd.Timestamp('2015-12-07', tz=UTC),
            # Thailand Constitution Day (December 10th) on a Sunday.
            pd.Timestamp('2017-12-11', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

        # Some holidays have exceptions to the observe-next-non-holiday rule.
        expected_sessions = [
            # Test that when Songkran Festival Days 2 and 3 (April 14th and
            # 15th) fall on a Saturday and Sunday, only the next Monday is a
            # holiday. Tuesday the 17th should be a trading day.
            pd.Timestamp('2018-04-17', tz=UTC),
            # When the last day of Songkran Festival (April 15th) falls on a
            # Saturday it should not be made up on Monday.
            pd.Timestamp('2017-04-17', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_bridge_days(self):
        all_sessions = self.calendar.all_sessions

        # A "bridge day" is either a Monday or Friday that is made into a
        # holiday to fill in the gap between a Tuesday or Thursday holiday,
        # respectively.
        expected_holidays = [
            # In 2015, New Year's Day was a Thursday, so the Friday after it
            # was made into a holiday.
            pd.Timestamp('2015-01-02', tz=UTC),
            # In 2013, New Year's Eve was a Tuesday, so the Monday before it
            # was made into a holiday.
            pd.Timestamp('2013-12-30', tz=UTC),
            # In 2016, Asanha Bucha fell on Tuesday July 19th, so the Monday
            # before it was made into a holiday.
            pd.Timestamp('2016-07-18', tz=UTC),
            # In 2010, The Queen's Birthday fell on Thursday August 12th, so
            # the Friday after it was made into a holiday.
            pd.Timestamp('2010-08-13', tz=UTC),
            # In 2016, Coronation Day fell on Thursday May 5th, so the Friday
            # after it was made into a holiday.
            pd.Timestamp('2016-05-06', tz=UTC),
            # In 2011, Vesak Day fell on Tuesday May 17th, so the Monday before
            # it was made into a holiday.
            pd.Timestamp('2011-05-16', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
