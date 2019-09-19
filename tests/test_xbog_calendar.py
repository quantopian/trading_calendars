from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xbog import XBOGExchangeCalendar


class XBOGCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xbog'
    calendar_class = XBOGExchangeCalendar

    # The XBOG is open from 9:30AM to 4:00PM
    MAX_SESSION_HOURS = 6.5

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2018-03-12', '2018-11-06']

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-01-07', tz=UTC),  # Epiphany
            pd.Timestamp('2019-03-25', tz=UTC),  # St. Joseph's Day
            pd.Timestamp('2019-04-18', tz=UTC),  # Maundy Thursday
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-06-03', tz=UTC),  # Ascension Day
            pd.Timestamp('2019-06-24', tz=UTC),  # Corpus Christi
            pd.Timestamp('2019-07-01', tz=UTC),  # Sacred Heart
            pd.Timestamp('2018-07-02', tz=UTC),  # St. Peter and St. Paul Day
            pd.Timestamp('2018-07-20', tz=UTC),  # Colombian Independence Day
            pd.Timestamp('2019-08-07', tz=UTC),  # Battle of Boyaca
            pd.Timestamp('2019-08-19', tz=UTC),  # Assumption Day
            pd.Timestamp('2019-10-14', tz=UTC),  # Dia de la Raza
            pd.Timestamp('2019-11-04', tz=UTC),  # All Saint's Day
            pd.Timestamp('2019-11-11', tz=UTC),  # Cartagena Independence Day
            pd.Timestamp('2017-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-31', tz=UTC),  # Last Trading Day
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Some (not all) holidays that fall on a weekend should not be made
        # up, so ensure surrounding days are open market
        expected_sessions = [
            # New Years Day on Sunday, Jan 1st
            #   Note: 2011-12-30 is also a holiday due to Last Trading Day
            pd.Timestamp('2011-12-29', tz=UTC),
            pd.Timestamp('2012-01-02', tz=UTC),
            # Labour Day on Sunday, May 1st
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Colombia Independence Day on Saturday, Jul 20
            pd.Timestamp('2019-07-19', tz=UTC),
            pd.Timestamp('2019-07-22', tz=UTC),
            # Battle of Boyaca on Sunday, Aug 7
            pd.Timestamp('2016-08-05', tz=UTC),
            pd.Timestamp('2016-08-08', tz=UTC),
            # Immaculate Conception on Sunday, Dec 8th.
            pd.Timestamp('2019-12-06', tz=UTC),
            pd.Timestamp('2019-12-09', tz=UTC),
            # Christmas on a Sunday
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-26', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_monday_holidays(self):
        all_sessions = self.calendar.all_sessions

        # This calendar has many holidays that are observed on the closest
        # future Monday, so for each of these holidays ensure that, if it
        # falls on a non-Monday, the non-Monday is not a holiday and the
        # next Monday is a holiday.
        expected_sessions = [
            # Epiphany on Friday, Jan 6
            pd.Timestamp('2017-01-06', tz=UTC),
            # St. Joseph's Day on Tuesday, Mar 19
            pd.Timestamp('2019-03-19', tz=UTC),
            # St. Peter and St. Paul Day on Friday, Jun 29
            pd.Timestamp('2018-06-29', tz=UTC),
            # Assumption Day on Wednesday, Aug 15
            pd.Timestamp('2018-08-15', tz=UTC),
            # Dia de la Raza on Friday, Oct 12
            pd.Timestamp('2018-10-12', tz=UTC),
            # All Saint's Day on Thursday, Nov 1
            pd.Timestamp('2018-11-01', tz=UTC),
            # Cartagena Independence Day on Friday, Nov 11
            pd.Timestamp('2016-11-11', tz=UTC),
        ]

        expected_holidays = [
            # Epiphany moved to Monday, Jan 9
            pd.Timestamp('2017-01-09', tz=UTC),
            # St. Joseph's Day moved to Monday, Mar 25
            pd.Timestamp('2019-03-25', tz=UTC),
            # St. Peter and St. Paul Day moved to Monday, Jul 2
            pd.Timestamp('2018-07-02', tz=UTC),
            # Assumption Day moved to Monday, Aug 20
            pd.Timestamp('2018-08-20', tz=UTC),
            # Dia de la Raza moved to Monday, Oct 15
            pd.Timestamp('2018-10-15', tz=UTC),
            # All Saint's Day moved to Monday, Nov 5
            pd.Timestamp('2018-11-05', tz=UTC),
            # Cartagena Independence Day moved to Monday, Nov 14
            pd.Timestamp('2016-11-14', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_last_trading_day_holiday(self):
        all_sessions = self.calendar.all_sessions

        # The last trading day of the year is a holiday for XBOG
        expected_holidays = [
            # 2019 - last trading day is the 31st
            pd.Timestamp('2019-12-31', tz=UTC),
            # 2018 - last trading day is the 31st
            pd.Timestamp('2018-12-31', tz=UTC),
            # 2017 - last trading day is the 29th
            pd.Timestamp('2017-12-29', tz=UTC),
            # 2016 - last trading day is the 30th
            pd.Timestamp('2016-12-30', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
