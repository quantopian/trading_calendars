from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import NoDSTExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xtai import XTAIExchangeCalendar


class XTAICalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xtai'
    calendar_class = XTAIExchangeCalendar

    # The XTAI is open from 9:00AM to 1:30PM
    MAX_SESSION_HOURS = 4.5

    HAVE_EARLY_CLOSES = False

    # A holiday falls on one of the default dates for these test
    # values, so overwrite here.
    MINUTE_INDEX_TO_SESSION_LABELS_START = pd.Timestamp('2011-01-06')
    MINUTE_INDEX_TO_SESSION_LABELS_END = pd.Timestamp('2011-04-06')

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-02-04', tz=UTC),  # Chinese New Year's Eve
            pd.Timestamp('2019-02-05', tz=UTC),  # Chinese New Year
            pd.Timestamp('2019-02-28', tz=UTC),  # Peace Memorial Day
            pd.Timestamp('2019-04-04', tz=UTC),  # Women and Children's Day
            pd.Timestamp('2019-04-05', tz=UTC),  # Tomb Sweeping Day
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-06-07', tz=UTC),  # Dragon Boat Festival
            pd.Timestamp('2019-09-13', tz=UTC),  # Mid-Autumn Festival
            pd.Timestamp('2019-10-10', tz=UTC),  # National Day
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Holidays falling on weekends are made up, so verify appropriate
        # Friday/Monday is a holiday.
        expected_holidays = [
            # New Year's Day on Sunday, Jan 1st.
            pd.Timestamp('2017-01-02', tz=UTC),
            # Chinese New Year on Saturday, Jan 28th.
            pd.Timestamp('2017-01-27', tz=UTC),
            # Peace Memorial Day on Sunday, Feb 28th.
            pd.Timestamp('2016-02-29', tz=UTC),
            # Women and Children's Day on Saturday, Apr 4th.
            pd.Timestamp('2015-04-03', tz=UTC),
            # Tomb Sweeping Day on Sunday, Apr 5th.
            pd.Timestamp('2015-04-06', tz=UTC),
            # Labour Day on Sunday, May 1st.
            pd.Timestamp('2016-05-02', tz=UTC),
            # Dragon Boat Festival on Saturday, Jun 20th.
            pd.Timestamp('2015-06-19', tz=UTC),
            # Mid-Autumn Festival on Sunday, Sep 27th.
            pd.Timestamp('2015-09-28', tz=UTC),
            # National Day on Saturday, Oct 10th.
            pd.Timestamp('2015-10-09', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

        # Also verify that, for example, if the holiday fell on a
        # Sunday the previous Friday is a trading session.
        expected_sessions = [
            # New Year's Day on Sunday, Jan 1st.
            pd.Timestamp('2016-12-30', tz=UTC),
            # Peace Memorial Day on Sunday, Feb 28th.
            pd.Timestamp('2016-02-26', tz=UTC),
            # Tomb Sweeping Day on Saturday, Apr 5th.
            pd.Timestamp('2014-04-07', tz=UTC),
            # Labour Day on Sunday, May 1st.
            pd.Timestamp('2016-04-29', tz=UTC),
            # Dragon Boat Festival on Saturday, Jun 20th.
            pd.Timestamp('2015-06-22', tz=UTC),
            # Mid-Autumn Festival on Sunday, Sep 27th.
            pd.Timestamp('2015-09-25', tz=UTC),
            # National Day on Saturday, Oct 10th.
            pd.Timestamp('2015-10-12', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_four_day_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Verify that a holiday is added between Tuesdays/Thursdays and
        # the weekend to make a four day weekend.
        expected_holidays = [
            # New Year's Day on Thursday, Jan 1st.
            pd.Timestamp('2015-01-02', tz=UTC),
            # Peace Memorial day on Tuesday, Feb 28th.
            pd.Timestamp('2017-02-27', tz=UTC),
            # Women and Children's Day on Tuesday, Apr 4th.
            pd.Timestamp('2017-04-03', tz=UTC),
            # National Day on Thursday, Oct 10th.
            pd.Timestamp('2019-10-11', tz=UTC),
            # Tomb Sweeping Day on Thursday, Apr 5th.
            pd.Timestamp('2018-04-06', tz=UTC),
            # Dragon Boat Festival on Tuesday, May 30th.
            pd.Timestamp('2017-05-29', tz=UTC),
            # Mid-Autumn Festival on Thursday, Sep 15th.
            pd.Timestamp('2016-09-16', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
