from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.exchange_calendar_xmos import XMOSExchangeCalendar

from .test_trading_calendar import ExchangeCalendarTestBase


class XMOSCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xmos'
    calendar_class = XMOSExchangeCalendar

    # The XMOS is open from 10:00AM to 6:45PM.
    MAX_SESSION_HOURS = 8.75

    # In 2009 in Russia, daylight savings began on March 29th and ended on
    # October 25th.
    DAYLIGHT_SAVINGS_DATES = ['2009-03-30', '2009-10-26']

    HAVE_EARLY_CLOSES = False

    # The default `MINUTE_INDEX_TO_SESSION_LABELS_START` is not a session in
    # the XMOS calendar so overwrite that date here.
    MINUTE_INDEX_TO_SESSION_LABELS_START = pd.Timestamp('2019-01-04', tz=UTC)
    MINUTE_INDEX_TO_SESSION_LABELS_END = pd.Timestamp('2019-04-04', tz=UTC)

    # None of the dates in the default range for these are trading days in the
    # XMOS, so overwrite them here.
    TEST_START_END_FIRST = pd.Timestamp('2019-01-13', tz=UTC)
    TEST_START_END_LAST = pd.Timestamp('2019-01-20', tz=UTC)
    TEST_START_END_EXPECTED_FIRST = pd.Timestamp('2019-01-14', tz=UTC)
    TEST_START_END_EXPECTED_LAST = pd.Timestamp('2019-01-18', tz=UTC)

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-01-02', tz=UTC),  # New Year's Holiday
            pd.Timestamp('2019-01-07', tz=UTC),  # Orthodox Christmas
            pd.Timestamp('2018-02-23', tz=UTC),  # Defender of the Fatherland
            pd.Timestamp('2019-03-08', tz=UTC),  # Women's Day
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-05-09', tz=UTC),  # Victory Day
            pd.Timestamp('2019-06-12', tz=UTC),  # Day of Russia
            pd.Timestamp('2019-11-04', tz=UTC),  # Unity Day
            pd.Timestamp('2019-12-31', tz=UTC),  # New Year's Eve
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Most holidays falling on a weekend should be observed the following
        # Monday.
        expected_holidays = [
            # New Year's Day on a Saturday and New Year's Holiday on a Sunday.
            pd.Timestamp('2011-01-03', tz=UTC),
            # Orthodox Christmas (January 7th) on a Sunday.
            pd.Timestamp('2018-01-08', tz=UTC),
            # Defender of the Fatherland Day (February 23rd) on a Saturday.
            pd.Timestamp('2008-02-25', tz=UTC),
            # Women's Day (March 8th) on a Sunday.
            pd.Timestamp('2015-03-09', tz=UTC),
            # Labour Day (May 1st) on a Sunday.
            pd.Timestamp('2016-05-02', tz=UTC),
            # Victory Day (May 9th) on a Saturday.
            pd.Timestamp('2015-05-11', tz=UTC),
            # Day of Russia (June 12th) on a Sunday.
            pd.Timestamp('2016-06-13', tz=UTC),
            # Unity Day (November 4th) on a Sunday.
            pd.Timestamp('2018-11-05', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

        # Some holidays have exceptions to the observe-on-monday rule.
        expected_sessions = [
            # New Year's Holiday on a Saturday, but the following Monday is a
            # trading day.
            pd.Timestamp('2016-01-04', tz=UTC),
            # Orthodox Christmas on a Saturday, but the following Monday is a
            # trading day.
            pd.Timestamp('2017-01-09', tz=UTC),
            # Defender of the Fatherland Day (February 23rd) on a Saturday, but
            # the following Monday is a trading day.
            pd.Timestamp('2019-02-25', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_bridge_days(self):
        all_sessions = self.calendar.all_sessions

        # A "bridge day" is either a Monday or Friday that is made into a
        # holiday to fill in the gap between a Tuesday or Thursday holiday,
        # respectively.
        expected_holidays = [
            # In 2016, Orthodox Christmas fell on a Thursday so the Friday
            # after it is a holiday.
            pd.Timestamp('2016-01-08', tz=UTC),
            # In 2010, Defender of the Fatherland Day fell on a Tuesday, so the
            # Monday before it is a holiday.
            pd.Timestamp('2010-02-22', tz=UTC),
            # In 2012, Women's Day fell on a Thursday, so the Friday after it
            # is a holiday.
            pd.Timestamp('2012-03-09', tz=UTC),
            # In 2012, Labour Day fell on a Tuesday, so the Monday before it is
            # a holiday.
            pd.Timestamp('2012-04-30', tz=UTC),
            # In 2017, Victory Day fell on a Tuesday, so the Monday before it
            # is a holiday.
            pd.Timestamp('2017-05-08', tz=UTC),
            # In 2014, Day of Russia fell on a Thursday, so the Friday after it
            # is a holiday.
            pd.Timestamp('2014-06-13', tz=UTC),
            # in 2010, Unity Day fell on a Thursday, so the Friday after it is
            # a holiday.
            pd.Timestamp('2010-11-05', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
