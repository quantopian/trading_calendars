from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.exchange_calendar_xlim import XLIMExchangeCalendar

from .test_trading_calendar import NoDSTExchangeCalendarTestBase


class XLIMCalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xlim'
    calendar_class = XLIMExchangeCalendar

    # The XLIM is open from 9:00AM to 4:00PM.
    MAX_SESSION_HOURS = 7

    HAVE_EARLY_CLOSES = False

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-04-18', tz=UTC),  # Maundy Thursday
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2018-06-29', tz=UTC),  # St. Peter and St. Paul Day
            pd.Timestamp('2016-07-28', tz=UTC),  # Independence Day 1
            pd.Timestamp('2016-07-29', tz=UTC),  # Independence Day 2
            pd.Timestamp('2019-08-30', tz=UTC),  # Santa Rosa
            pd.Timestamp('2019-10-08', tz=UTC),  # Battle of Angamos
            pd.Timestamp('2019-11-01', tz=UTC),  # All Saints' Day
            pd.Timestamp('2017-12-08', tz=UTC),  # Immaculate Conception
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
            # Labour Day (May 1st) on a Sunday.
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Saint Peter and Saint Paul Day (June 29th) on a Saturday.
            pd.Timestamp('2019-06-28', tz=UTC),
            pd.Timestamp('2019-07-01', tz=UTC),
            # Independence Days (July 28th and 29th) on a Saturday and Sunday.
            pd.Timestamp('2018-07-27', tz=UTC),
            pd.Timestamp('2018-07-30', tz=UTC),
            # Santa Rosa (August 30th) on a Sunday.
            pd.Timestamp('2015-08-28', tz=UTC),
            pd.Timestamp('2015-08-31', tz=UTC),
            # Battle of Angamos (October 8th) on a Sunday.
            pd.Timestamp('2017-10-06', tz=UTC),
            pd.Timestamp('2017-10-09', tz=UTC),
            # All Saints' Day (November 1st) on a Sunday.
            pd.Timestamp('2015-10-30', tz=UTC),
            pd.Timestamp('2015-11-02', tz=UTC),
            # Immaculate Conception (December 8th) on a Sunday.
            pd.Timestamp('2019-12-06', tz=UTC),
            pd.Timestamp('2019-12-09', tz=UTC),
            # Christmas on a Sunday.
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-26', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_new_years_eve(self):
        """
        New Year's Eve ceased being a holiday after 2007.
        """
        all_sessions = self.calendar.all_sessions

        for year in range(2000, 2008):
            self.assertNotIn(
                pd.Timestamp('{}-12-31'.format(year), tz=UTC),
                all_sessions,
            )

        self.assertIn(pd.Timestamp('2008-12-31', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2009-12-31', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2010-12-31', tz=UTC), all_sessions)

    def test_adhoc_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            # Exchange holidays.
            pd.Timestamp('2009-01-02', tz=UTC),
            pd.Timestamp('2009-07-27', tz=UTC),
            pd.Timestamp('2015-01-02', tz=UTC),
            pd.Timestamp('2015-07-27', tz=UTC),
            pd.Timestamp('2015-10-09', tz=UTC),
            # ASPA Summit.
            pd.Timestamp('2012-10-01', tz=UTC),
            pd.Timestamp('2012-10-02', tz=UTC),
            # APEC Summit.
            pd.Timestamp('2016-11-17', tz=UTC),
            pd.Timestamp('2016-11-18', tz=UTC),
            # 8th Summit of the Americas.
            pd.Timestamp('2018-04-13', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)
