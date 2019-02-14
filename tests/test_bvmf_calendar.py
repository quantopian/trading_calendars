from unittest import TestCase
import pandas as pd
from pytz import UTC

from .test_trading_calendar import ExchangeCalendarTestBase
from trading_calendars.exchange_calendar_bvmf import BVMFExchangeCalendar


class BVMFCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'bvmf'
    calendar_class = BVMFExchangeCalendar

    MINUTE_INDEX_TO_SESSION_LABELS_START = pd.Timestamp('2011-01-05', tz=UTC)
    MINUTE_INDEX_TO_SESSION_LABELS_END = pd.Timestamp('2011-04-05', tz=UTC)

    HAVE_EARLY_CLOSES = False

    DAYLIGHT_SAVINGS_DATES = ['2017-02-17', '2017-10-16']

    # Open from 10am to 5pm
    MAX_SESSION_HOURS = 7

    def test_normal_year(self):
        expected_holidays_2017 = [
            pd.Timestamp('2017-01-25', tz=UTC),  # Sao Paolo City Anniversary
            pd.Timestamp('2017-02-27', tz=UTC),  # Carnival
            pd.Timestamp('2017-02-28', tz=UTC),  # Carnival
            pd.Timestamp('2017-04-14', tz=UTC),  # Good Friday
            pd.Timestamp('2017-04-21', tz=UTC),  # Tiradentes Day
            pd.Timestamp('2017-05-01', tz=UTC),  # Labor Day
            pd.Timestamp('2017-06-15', tz=UTC),  # Corpus Christi Day
            pd.Timestamp('2017-09-07', tz=UTC),  # Independence Day
            pd.Timestamp('2017-10-12', tz=UTC),  # Our Lady of Aparecida Day
            pd.Timestamp('2017-11-02', tz=UTC),  # All Souls Day
            pd.Timestamp('2017-11-15', tz=UTC),  # Proclamation of the
                                                 #  Republic Day
            pd.Timestamp('2017-11-20', tz=UTC),  # Black Consciousness Day
            pd.Timestamp('2017-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2017-12-29', tz=UTC),  # Day before New Years
        ]

        for session_label in expected_holidays_2017:
            self.assertNotIn(session_label, self.calendar.all_sessions)

        other_holidays = [
            pd.Timestamp("2018-01-01", tz=UTC),  # New Year's Day
            pd.Timestamp("2015-07-09", tz=UTC),  # Constitutional
                                                 #  Revolution Day
        ]

        for session_label in other_holidays:
            self.assertNotIn(session_label, self.calendar.all_sessions)

    # FIXME: add back in later.
    # def test_late_opens(self):
    #     # Ash Wednesday, 46 days before Easter Sunday
    #     late_opens = [
    #         pd.Timestamp("2016-02-10", tz=UTC),
    #         pd.Timestamp("2017-03-01", tz=UTC),
    #         pd.Timestamp("2018-02-14", tz=UTC),
    #     ]

    #     for late_open_session_label in late_opens:
    #         self.assertIn(
    #             late_open_session_label,
    #             self.calendar.late_opens,
    #         )

    def test_special_holidays(self):
        # Constitutionalist Revolution started in 1998
        self.assertNotIn(
            pd.Timestamp("1998-07-09", tz=UTC),
            self.calendar.all_sessions
        )

        self.assertIn(
            pd.Timestamp("1997-07-09", tz=UTC),
            self.calendar.all_sessions
        )

        # Day of Black Awareness started in 2004
        self.assertNotIn(
            pd.Timestamp("2006-11-20", tz=UTC),
            self.calendar.all_sessions
        )

        self.assertIn(
            pd.Timestamp("2003-11-20", tz=UTC),
            self.calendar.all_sessions
        )

    def test_day_before_new_year(self):
        # if Jan 1 is Tuesday through Saturday, we are closed the day before.
        # if Jan 1 is Monday or Sunday, we are closed the Friday before.

        # 2018: Jan 1 is Monday, so Friday 12/29 should be closed
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2017-12-29', tz=UTC))
        )

        # 2017: Jan 1 is Sunday, so Friday 12/30 should be closed
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2016-12-30', tz=UTC))
        )

        # 2011: Jan 1 is Saturday, so Friday 12/31 should be closed
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2010-12-31', tz=UTC))
        )

        # 2014: Jan 1 is Wednesday, so Tuesday 12/31 should be closed
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2013-12-31', tz=UTC))
        )

    def test_world_cup(self):
        self.assertFalse(
            self.calendar.is_session(pd.Timestamp('2014-06-12', tz=UTC))
        )
