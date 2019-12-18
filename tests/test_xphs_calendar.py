from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import NoDSTExchangeCalendarTestBase
from trading_calendars.exchange_calendar_xphs import XPHSExchangeCalendar


class XPHSCalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xphs'
    calendar_class = XPHSExchangeCalendar

    # The XPHS is open from 9:30AM to 3:30PM
    MAX_SESSION_HOURS = 6.0

    HAVE_EARLY_CLOSES = False

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-02-05', tz=UTC),  # Chinese New Year
            pd.Timestamp('2019-04-09', tz=UTC),  # Araw Ng Kagitingan
            pd.Timestamp('2019-04-18', tz=UTC),  # Maundy Thursday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-06-05', tz=UTC),  # Eid al-Fitr
            pd.Timestamp('2019-06-12', tz=UTC),  # Independence Day
            pd.Timestamp('2019-08-12', tz=UTC),  # Eid al-Adha
            pd.Timestamp('2019-08-21', tz=UTC),  # Ninoy Aquino Day
            pd.Timestamp('2019-08-26', tz=UTC),  # National Heroes Day
            pd.Timestamp('2017-09-01', tz=UTC),  # Eid al-Adha
            pd.Timestamp('2019-11-01', tz=UTC),  # All Saint's Day
            pd.Timestamp('2018-11-30', tz=UTC),  # Bonifacio Day
            pd.Timestamp('2019-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas
            pd.Timestamp('2019-12-30', tz=UTC),  # Rizal Day
            pd.Timestamp('2019-12-31', tz=UTC),  # New Year's Eve
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # Holidays falling on weekends are not made up, so verify surrounding
        # Friday/Monday are trading days.
        expected_sessions = [
            # New Year's Day on Sunday, Jan 1st.
            #  2011-12-30 is Rizal Day
            pd.Timestamp('2011-12-29', tz=UTC),
            pd.Timestamp('2012-01-02', tz=UTC),
            # Chinese New Year's on Saturday, Jan 28th.
            pd.Timestamp('2017-01-27', tz=UTC),
            pd.Timestamp('2017-01-30', tz=UTC),
            # Araw Ng Kagitingan on Sunday, Apr 9th.
            pd.Timestamp('2017-04-07', tz=UTC),
            pd.Timestamp('2017-04-10', tz=UTC),
            # Labour Day on Saturday, May 1st.
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Independence Day on Sunday, Jun 12th.
            pd.Timestamp('2016-06-10', tz=UTC),
            pd.Timestamp('2016-06-13', tz=UTC),
            # Ninoy Aquino Day on Sunday, Aug 21st.
            pd.Timestamp('2016-08-19', tz=UTC),
            pd.Timestamp('2016-08-22', tz=UTC),
            # All Saint's Day on Sunday, Nov 1st.
            pd.Timestamp('2015-10-30', tz=UTC),
            pd.Timestamp('2015-11-02', tz=UTC),
            # Bonifacio Day on Saturday, Nov 30th.
            pd.Timestamp('2019-11-29', tz=UTC),
            pd.Timestamp('2019-12-02', tz=UTC),
            # Christmas Eve + Christmas Day on weekend.
            pd.Timestamp('2011-12-23', tz=UTC),
            pd.Timestamp('2011-12-26', tz=UTC),
            # Rizal Day + New Year's Eve on weekend.
            #  2018-01-01 and 2018-01-02 are both holidays.
            pd.Timestamp('2017-12-29', tz=UTC),
            pd.Timestamp('2018-01-03', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_national_heroes_day(self):
        all_sessions = self.calendar.all_sessions

        # National Heroes' Day takes place on the last Monday of every
        # August. This test makes sure the last Monday of every August
        # is a holiday.
        expected_holidays = [
            pd.Timestamp('2019-08-26', tz=UTC),
            pd.Timestamp('2018-08-27', tz=UTC),
            pd.Timestamp('2017-08-28', tz=UTC),
            pd.Timestamp('2016-08-29', tz=UTC),
            pd.Timestamp('2015-08-31', tz=UTC),
            pd.Timestamp('2014-08-25', tz=UTC),
            pd.Timestamp('2013-08-26', tz=UTC),
            pd.Timestamp('2012-08-27', tz=UTC),
            pd.Timestamp('2011-08-29', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_2008_adhoc(self):
        all_sessions = self.calendar.all_sessions

        # For this calendar, all holidays prior to 2011 are hard-coded
        # for convenience.  This test verifies that those holidays are
        # working by checking a subset of them (all 2008 holidays).
        expected_holidays = [
            pd.Timestamp('2008-01-01', tz=UTC),
            pd.Timestamp('2008-02-25', tz=UTC),
            pd.Timestamp('2008-03-20', tz=UTC),
            pd.Timestamp('2008-03-21', tz=UTC),
            pd.Timestamp('2008-04-07', tz=UTC),
            pd.Timestamp('2008-05-01', tz=UTC),
            pd.Timestamp('2008-06-09', tz=UTC),
            pd.Timestamp('2008-08-18', tz=UTC),
            pd.Timestamp('2008-08-25', tz=UTC),
            pd.Timestamp('2008-10-01', tz=UTC),
            pd.Timestamp('2008-12-01', tz=UTC),
            pd.Timestamp('2008-12-25', tz=UTC),
            pd.Timestamp('2008-12-26', tz=UTC),
            pd.Timestamp('2008-12-29', tz=UTC),
            pd.Timestamp('2008-12-30', tz=UTC),
            pd.Timestamp('2008-12-31', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
