from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xwbo import XWBOExchangeCalendar


class XWBOCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xwbo'
    calendar_class = XWBOExchangeCalendar

    # The XWBO is open from 9:00 am to 5:30 pm.
    MAX_SESSION_HOURS = 8.5

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2018-03-12', '2018-11-05']

    def test_normal_holidays(self):
        expected_holidays = [
            pd.Timestamp('2014-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2014-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2014-04-18', tz=UTC),  # Good Friday
            pd.Timestamp('2014-04-21', tz=UTC),  # Easter Monday
            pd.Timestamp('2014-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2014-05-29', tz=UTC),  # Ascension Day
            pd.Timestamp('2014-06-09', tz=UTC),  # Whit Monday
            pd.Timestamp('2014-06-19', tz=UTC),  # Corpus Christi
            pd.Timestamp('2014-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2014-10-26', tz=UTC),  # National Day (Weekend)
            pd.Timestamp('2015-10-26', tz=UTC),  # National Day (Weekday)
            pd.Timestamp('2013-11-01', tz=UTC),  # All Saints Day (Weekday)
            pd.Timestamp('2014-11-01', tz=UTC),  # All Saints Day (Weekend)
            pd.Timestamp('2014-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2014-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2014-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2014-12-26', tz=UTC),  # St. Stephen's Day
            pd.Timestamp('2014-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_normal_holidays_after_2018(self):
        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-04-22', tz=UTC),  # Easter Monday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-06-10', tz=UTC),  # Whit Monday
            pd.Timestamp('2019-10-26', tz=UTC),  # National Day (Weekend)
            pd.Timestamp('2019-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-26', tz=UTC),  # St. Stephen's Day
            pd.Timestamp('2019-12-31', tz=UTC),  # New Year's Eve
        ]

        for session_label in expected_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    def test_holidays_fall_on_weekend(self):
        # Holidays falling on a weekend should generally not be made up
        # during the week, so test that the Fridays and Mondays surrounding
        # them are open market days.
        expected_sessions = [
            # Epiphany (January 6th) on a Saturday.
            pd.Timestamp('2018-01-05', tz=UTC),
            pd.Timestamp('2018-01-08', tz=UTC),
            # Assumption Day (August 15th) on a Saturday.
            pd.Timestamp('2015-08-14', tz=UTC),
            pd.Timestamp('2015-08-17', tz=UTC),
            # Labour Day (May 1st) on a Saturday.
            pd.Timestamp('2010-04-30', tz=UTC),
            pd.Timestamp('2010-05-03', tz=UTC),
            # National Day (October 26th) on a Sunday.
            pd.Timestamp('2014-10-24', tz=UTC),
            pd.Timestamp('2014-10-27', tz=UTC),
            # All Saints Day (November 1st) on a Sunday.
            pd.Timestamp('2015-10-30', tz=UTC),
            pd.Timestamp('2015-11-02', tz=UTC),
            # Immaculate Conception (December 8th) on a Saturday.
            pd.Timestamp('2018-12-07', tz=UTC),
            pd.Timestamp('2018-12-10', tz=UTC),
            # Christmas Eve on a Saturday and Christmas on a Sunday. This means
            # that the market should be open on the previous Friday, closed on
            # Monday for St. Stephen's Day, and open again on Tuesday.
            pd.Timestamp('2011-12-23', tz=UTC),
            pd.Timestamp('2011-12-27', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)

    def test_new_years_eve_falls_on_weekend(self):
        # Prior to 2016, when New Year's Eve fell on the weekend, it was
        # observed on the preceding Friday.
        expected_holidays = [
            # New Year's Eve on a Saturday, observed on Friday 12/30.
            pd.Timestamp('2011-12-30', tz=UTC),
            # New Year's Eve on a Sunday, observed on Friday 12/29.
            pd.Timestamp('2006-12-29', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, self.calendar.all_sessions)

        # In 2016 and after, it is not made up.
        expected_sessions = [
            # New Year's Eve on a Saturday, Friday 12/30 is a trading day.
            pd.Timestamp('2016-12-30', tz=UTC),
            # New Year's Eve on a Sunday, Friday 12/29 is a trading day.
            pd.Timestamp('2017-12-29', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, self.calendar.all_sessions)
