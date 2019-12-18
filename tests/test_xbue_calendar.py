from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xbue import XBUEExchangeCalendar


class XBUECalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xbue'
    calendar_class = XBUEExchangeCalendar

    # The XBUE is open from 11:00AM to 5:00PM
    MAX_SESSION_HOURS = 6

    # Daylight Savings was observed in Buenos Aires from 2007-2009
    DAYLIGHT_SAVINGS_DATES = ['2008-10-20', '2008-03-17']

    # TODO: Verify Christmas Eve, NYE early closes
    HAVE_EARLY_CLOSES = True

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-03-04', tz=UTC),  # Carnival Monday
            pd.Timestamp('2019-03-05', tz=UTC),  # Carnival Tuesday
            pd.Timestamp('2017-03-24', tz=UTC),  # Truth and Justice Mem Day
            pd.Timestamp('2019-04-02', tz=UTC),  # Malvinas Day
            pd.Timestamp('2019-04-13', tz=UTC),  # Maundy Thursday
            pd.Timestamp('2019-04-14', tz=UTC),  # Good Friday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2018-05-25', tz=UTC),  # May Day Revolution
            pd.Timestamp('2019-06-17', tz=UTC),  # Martin Miguel de-Guemes Day
            pd.Timestamp('2019-06-20', tz=UTC),  # National Flag Day
            pd.Timestamp('2019-07-09', tz=UTC),  # Independence Day
            pd.Timestamp('2019-08-19', tz=UTC),  # San Martin's Day
            pd.Timestamp('2019-10-14', tz=UTC),  # Cultural Diversity Day
            pd.Timestamp('2019-11-18', tz=UTC),  # Day of Natl Sovereignty
            pd.Timestamp('2017-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Holidays falling on weekends are not made up, so verify surrounding
        # days are trading days.
        expected_sessions = [
            # New Year's Day on Sunday, Jan 1st.
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
            # Truth and Justice Memorial Day on Sunday, Mar 24th.
            pd.Timestamp('2019-03-22', tz=UTC),
            pd.Timestamp('2019-03-25', tz=UTC),
            # Malvinas Day on Saturday, Apr 2nd.
            pd.Timestamp('2016-04-01', tz=UTC),
            pd.Timestamp('2016-04-04', tz=UTC),
            # Labour Day on Sunday, May 1st.
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # May Day Revolution on Saturday, May 25th.
            pd.Timestamp('2019-05-24', tz=UTC),
            pd.Timestamp('2019-05-27', tz=UTC),
            # Martin Miguel de-Guemes Day on Sunday, Jun 17th.
            pd.Timestamp('2018-06-15', tz=UTC),
            pd.Timestamp('2018-06-18', tz=UTC),
            # National Flag Day on Saturday, Jun 20th.
            pd.Timestamp('2015-06-19', tz=UTC),
            pd.Timestamp('2015-06-22', tz=UTC),
            # Independence Day on Sunday, Jul 9th.
            pd.Timestamp('2017-07-07', tz=UTC),
            pd.Timestamp('2017-07-10', tz=UTC),
            # Bank Holiday on Sunday, Nov 6th.
            pd.Timestamp('2016-11-04', tz=UTC),
            pd.Timestamp('2016-11-07', tz=UTC),
            # Immaculate Conception on Sunday, Dec 8th.
            pd.Timestamp('2019-12-06', tz=UTC),
            pd.Timestamp('2019-12-09', tz=UTC),
            # Christmas on Sunday
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-26', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_cultural_diversity_day(self):
        all_sessions = self.calendar.all_sessions

        # Day of Respect for Cultural Diversity follows a "nearest Monday"
        # rule.  When Oct 12 falls on a Tuesday or Wednesday the holiday is
        # observed on the previous Monday, and when it falls on any other
        # non-Monday it is observed on the following Monday.  This means
        # the holiday will be observed between Oct 10 and Oct 16.
        expected_holidays = [
            pd.Timestamp('2019-10-14', tz=UTC),  # Falls on Saturday
            pd.Timestamp('2018-10-15', tz=UTC),  # Falls on Friday
            pd.Timestamp('2017-10-16', tz=UTC),  # Falls on Thursday
            pd.Timestamp('2016-10-10', tz=UTC),  # Falls on Wednesday
            pd.Timestamp('2015-10-12', tz=UTC),  # Falls on Monday
            pd.Timestamp('2014-10-13', tz=UTC),  # Falls on Sunday
            pd.Timestamp('2013-10-14', tz=UTC),  # Falls on Saturday
            pd.Timestamp('2010-10-11', tz=UTC),  # Falls on Tuesday
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_early_closes(self):
        # The session label and close time for expected early closes.
        buenos_aires_tz = 'America/Argentina/Buenos_Aires'
        expected_early_closes = [
            # Christmas Eve
            (
                pd.Timestamp('2019-12-24', tz=UTC),
                pd.Timestamp('2019-12-24 13:00', tz=buenos_aires_tz),
            ),
            # New Year's Eve
            (
                pd.Timestamp('2019-12-31', tz=UTC),
                pd.Timestamp('2019-12-31 13:00', tz=buenos_aires_tz),
            ),
        ]

        for session, expected_close in expected_early_closes:
            self.assertEqual(
                self.calendar.session_close(session),
                expected_close,
            )
