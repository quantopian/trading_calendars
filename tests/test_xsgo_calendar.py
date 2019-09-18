from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.exchange_calendar_xsgo import XSGOExchangeCalendar

from .test_trading_calendar import ExchangeCalendarTestBase


class XSGOCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xsgo'
    calendar_class = XSGOExchangeCalendar

    # The XSGO's longest sessions happen from November to February, when it is
    # open from 9:30AM to 5:00PM.
    MAX_SESSION_HOURS = 7.5

    # In 2018 in Chile, daylight savings time ended on May 13th and began again
    # on August 12th.
    DAYLIGHT_SAVINGS_DATES = ['2018-05-14', '2018-08-13']

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-05-21', tz=UTC),  # Navy Day
            pd.Timestamp('2019-07-16', tz=UTC),  # Our Lady of Mount Carmel Day
            pd.Timestamp('2019-08-15', tz=UTC),  # Assumption Day
            pd.Timestamp('2019-09-18', tz=UTC),  # Independence Day
            pd.Timestamp('2019-09-19', tz=UTC),  # Army Day
            pd.Timestamp('2019-09-20', tz=UTC),  # Public Holiday
            pd.Timestamp('2019-10-31', tz=UTC),  # Evangelical Church Day
            pd.Timestamp('2019-11-01', tz=UTC),  # All Saints' Day
            pd.Timestamp('2017-12-08', tz=UTC),  # Immaculate Conception
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-31', tz=UTC),  # Bank Holiday
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # All holidays falling on a weekend should not be made up, so verify
        # that the surrounding Fridays/Mondays are trading days.
        expected_sessions = [
            # Bank Holiday on Saturday, December 31st and  New Year's Day on
            # Sunday, January 1st.
            pd.Timestamp('2011-12-30', tz=UTC),
            pd.Timestamp('2012-01-02', tz=UTC),
            # Labour Day on Sunday, May 1st.
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Navy Day on Sunday, May 21st.
            pd.Timestamp('2017-05-19', tz=UTC),
            pd.Timestamp('2017-05-22', tz=UTC),
            # Saint Peter and Saint Paul Day on Saturday, June 29th.
            pd.Timestamp('2019-06-28', tz=UTC),
            pd.Timestamp('2019-07-01', tz=UTC),
            # Our Lady of Mount Carmel Day on Sunday, July 16th.
            pd.Timestamp('2017-07-14', tz=UTC),
            pd.Timestamp('2017-07-17', tz=UTC),
            # Assumption Day on Saturday, August 15th.
            pd.Timestamp('2015-08-14', tz=UTC),
            pd.Timestamp('2015-08-17', tz=UTC),
            # In 2004 Independence Day and Army Day fell on a Saturday and
            # Sunday, so the surrounding Friday and Monday should both be
            # trading days.
            pd.Timestamp('2004-09-17', tz=UTC),
            pd.Timestamp('2004-09-20', tz=UTC),
            # Dia de la Raza on Saturday, October 12th.
            pd.Timestamp('2019-10-11', tz=UTC),
            pd.Timestamp('2019-10-14', tz=UTC),
            # Evangelical Church Day (Halloween) and All Saints' Day fall on a
            # Saturday and Sunday, so Friday the 30th and Monday the 2nd should
            # both be trading days.
            pd.Timestamp('2015-10-30', tz=UTC),
            pd.Timestamp('2015-11-02', tz=UTC),
            # Immaculate Conception on Sunday, December 8th.
            pd.Timestamp('2019-12-06', tz=UTC),
            pd.Timestamp('2019-12-09', tz=UTC),
            # Christmas on a Sunday.
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-26', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_early_closes(self):
        # The session label and close time for expected early closes.
        expected_early_closes = [
            # Maundy Thursday.
            (
                pd.Timestamp('2019-04-18', tz=UTC),
                pd.Timestamp('2019-04-18 13:30', tz='America/Santiago'),
            ),
            # Day before Independence Day.
            (
                pd.Timestamp('2019-09-17', tz=UTC),
                pd.Timestamp('2019-09-17 13:30', tz='America/Santiago'),
            ),
            # Christmas Eve.
            (
                pd.Timestamp('2019-12-24', tz=UTC),
                pd.Timestamp('2019-12-24 12:30', tz='America/Santiago'),
            ),
            # Day before Bank Holiday.
            (
                pd.Timestamp('2019-12-30', tz=UTC),
                pd.Timestamp('2019-12-30 12:30', tz='America/Santiago'),
            ),
        ]

        for session, expected_close in expected_early_closes:
            self.assertEqual(
                self.calendar.session_close(session),
                expected_close,
            )

    def test_close_time_change(self):
        """
        In March the market close time changes from 5:00PM to 4:00PM and in
        November it changes from 4:00PM to 5:00PM. This happens every year.
        """
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2019-02-28', tz=UTC)),
            pd.Timestamp('2019-02-28 17:00', tz='America/Santiago'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2019-03-01', tz=UTC)),
            pd.Timestamp('2019-03-01 16:00', tz='America/Santiago'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2019-10-30', tz=UTC)),
            pd.Timestamp('2019-10-30 16:00', tz='America/Santiago'),
        )
        self.assertEqual(
            self.calendar.session_close(pd.Timestamp('2019-11-04', tz=UTC)),
            pd.Timestamp('2019-11-04 17:00', tz='America/Santiago'),
        )

    def test_adhoc_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            # Bicentennial Celebration.
            pd.Timestamp('2010-09-17', tz=UTC),
            pd.Timestamp('2010-09-20', tz=UTC),
            # For whatever reason New Year's Day, which was a Sunday, was
            # observed on Monday this one year.
            pd.Timestamp('2017-01-02', tz=UTC),
            # Census Day.
            pd.Timestamp('2017-04-19', tz=UTC),
            # Pope Visit.
            pd.Timestamp('2018-01-16', tz=UTC),
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_st_peter_and_st_paul_day(self):
        """
        Saint Peter and Saint Paul Day follows an unusual rule whereby if June
        29th falls on a Saturday, Sunday or Monday then the holiday is
        acknowledged on that day (Sat/Sun observances are not made up later).
        Otherwise it is observed on the closest Monday to the 29th.
        """
        all_sessions = self.calendar.all_sessions

        # In 2019, June 29th is a Saturday, so make sure the following Monday
        # is a trading day.
        self.assertIn(pd.Timestamp('2019-07-01', tz=UTC), all_sessions)

        # In 2018, June 29th is a Friday, so the following Monday should be a
        # holiday.
        self.assertNotIn(pd.Timestamp('2018-07-02', tz=UTC), all_sessions)

        # In 2017, June 29th is a Thursday, so the previous Monday should be a
        # holiday.
        self.assertNotIn(pd.Timestamp('2017-06-26', tz=UTC), all_sessions)

        # In 2016, June 29th is a Wednesday, so the previous Monday should be a
        # holiday.
        self.assertNotIn(pd.Timestamp('2016-06-27', tz=UTC), all_sessions)

        # In 2015, June 29th is a Monday, so that Monday should be a holiday.
        self.assertNotIn(pd.Timestamp('2015-06-29', tz=UTC), all_sessions)

        # In 2014, June 29th is a Sunday, so make sure the following Monday is
        # a trading day.
        self.assertIn(pd.Timestamp('2014-06-30', tz=UTC), all_sessions)

        # In 2010, June 29th is a Tuesday, so the previous Monday should be a
        # holiday.
        self.assertNotIn(pd.Timestamp('2010-06-28', tz=UTC), all_sessions)

    def test_dia_de_la_raza(self):
        """
        Dia de la Raza (also known as Columbus Day) follows the same rule as
        Saint Peter and Saint Paul Day described above. It is centered around
        October 12th.
        """
        all_sessions = self.calendar.all_sessions

        # In 2019, October 12th is a Saturday, so the following Monday should
        # be a trading day.
        self.assertIn(pd.Timestamp('2019-10-14', tz=UTC), all_sessions)

        # In 2018, October 12th is a Friday, so the following Monday should be
        # a holiday.
        self.assertNotIn(pd.Timestamp('2018-10-15', tz=UTC), all_sessions)

        # In 2017, October 12th is a Thursday, so the previous Monday should be
        # a holiday.
        self.assertNotIn(pd.Timestamp('2017-10-09', tz=UTC), all_sessions)

        # In 2016, October 12th is a Wednesday, so the previous Monday should
        # be a holiday.
        self.assertNotIn(pd.Timestamp('2016-10-10', tz=UTC), all_sessions)

        # In 2015, October 12th is a Monday, so that day should be a holiday.
        self.assertNotIn(pd.Timestamp('2015-10-12', tz=UTC), all_sessions)

        # In 2014, October 12th is a Sunday, so the following Monday should be
        # a trading day.
        self.assertIn(pd.Timestamp('2014-10-13', tz=UTC), all_sessions)

        # In 2010, October 12th is a Tuesday, so the previous Monday should be
        # a holiday.
        self.assertNotIn(pd.Timestamp('2010-10-11', tz=UTC), all_sessions)

    def test_public_holidays(self):
        """
        Independence Day and Army Day fall back to back on September 18th and
        19th. If they happen to fall on a Tue/Wed then the prior Monday is
        deemed a Public Holiday. If they happen to fall on a Wed/Thu then the
        following Friday is deemed a Public Holiday.
        """
        all_sessions = self.calendar.all_sessions

        # In 2019, Independence Day and Army Day are on Wednesday and Thursday,
        # so the 20th should also be a holiday.
        self.assertNotIn(pd.Timestamp('2019-09-20', tz=UTC), all_sessions)

        # In 2018, Independence Day and Army Day are on Tuesday and Wednesday,
        # so the 17th should also be a holiday.
        self.assertNotIn(pd.Timestamp('2018-09-17', tz=UTC), all_sessions)

    def test_evangelical_church_day(self):
        """
        Evangelical Church Day (also known as Halloween) adheres to the
        following rule: If October 31st falls on a Tuesday, it is observed the
        preceding Friday. If it falls on a Wednesday, it is observed the next
        Friday. If it falls on Thu, Fri, Sat, Sun, or Mon then the holiday is
        acknowledged that day.
        """
        all_sessions = self.calendar.all_sessions

        # In 2019, October 31st is a Thursday, so that day is a holiday.
        self.assertNotIn(pd.Timestamp('2019-10-31', tz=UTC), all_sessions)

        # In 2018, October 31st is a Wednesday, so the following Friday is a
        # holiday.
        self.assertNotIn(pd.Timestamp('2018-11-02', tz=UTC), all_sessions)

        # In 2017, October 31st is a Tuesday, so the previous Friday is a
        # holiday.
        self.assertNotIn(pd.Timestamp('2017-10-27', tz=UTC), all_sessions)

        # In 2016, October 31st is a Monday, so that day is a holiday.
        self.assertNotIn(pd.Timestamp('2016-10-31', tz=UTC), all_sessions)

        # In 2014, October 31st is a Friday, so that day is a holiday.
        self.assertNotIn(pd.Timestamp('2014-10-31', tz=UTC), all_sessions)
