from datetime import datetime
from unittest import TestCase

import pandas as pd
from pytz import UTC
from nose_parameterized import parameterized

from .test_trading_calendar import NoDSTExchangeCalendarTestBase
from trading_calendars.trading_calendar import WEEKENDS
from trading_calendars.exchange_calendar_xkar import XKARExchangeCalendar


class XKARCalendarTestCase(NoDSTExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xkar'
    calendar_class = XKARExchangeCalendar

    MAX_SESSION_HOURS = 5.967

    HAVE_EARLY_CLOSES = False

    @parameterized.expand([
        # https://www.psx.com.pk/psx/exchange/general/calendar-holidays
        ('2019-01-01', '2019-12-31', [
            '2019-02-05',  # Kashmir Day
            '2019-03-23',  # Pakistan Day
            '2019-05-01',  # Labour Day
            '2019-05-31',  # Juma-Tul-Wida
            '2019-06-04',  # [NOTE: not included on the website]
            '2019-06-05',  # Eid-ul-Fitr
            '2019-06-06',  # Eid-ul-Fitr
            '2019-06-07',  # Eid-ul-Fitr
            '2019-08-12',  # Eid-ul-Azha
            '2019-08-13',  # Eid-ul-Azha
            '2019-08-14',  # Independence Day
            '2019-08-15',  # Eid-ul-Azha
            '2019-09-09',  # Muharram (Ashura)
            '2019-09-10',  # Muharram (Ashura)
            '2019-11-10',  # Eid Milad-un-Nabi (SAW)
            '2019-12-25',  # Birthday of Quaid-e-Azam & Christmas
        ]),
    ])
    def test_holidays_in_date_range(self, start, end, holiday_dates):
        holidays = {pd.Timestamp(d, tz=UTC) for d in holiday_dates}
        date_range = pd.date_range(start=start, end=end, tz='UTC')

        # Sanity check for the test inputs.
        for holiday in holidays:
            if holiday not in date_range:
                raise ValueError("{} not in {}".format(holiday, date_range))

        sessions_on_holidays = {
            holiday for holiday in holidays
            if self.calendar.is_session(holiday)
        }

        missing_sessions = {
            day for day in date_range
            if not self.calendar.is_session(day)
            and day.dayofweek not in WEEKENDS
            and day not in holidays
        }

        errors = sessions_on_holidays | missing_sessions
        if errors:

            def print_info(timestamps, msg):
                if timestamps:
                    print(msg)
                    for ts in sorted(timestamps):
                        print(ts.date())

            print_info(
                sessions_on_holidays,
                "\n{} session(s) were marked as holidays in the"
                " test data, but were listed as sessions by the"
                " calendar:".format(len(sessions_on_holidays))
            )

            print_info(
                missing_sessions,
                "\n{} weekday(s) were not listed as sessions by the"
                " calendar, but were also not marked as holidays in the"
                " test data:".format(len(missing_sessions))
            )

            self.fail("{} error(s) between {} and {}".format(
                len(errors), start, end))

    def test_iqbal_day(self):
        for year in range(2002, 2014):
            # The datetime wrapper is required for Pandas 0.18.1
            iqbal_day = pd.Timestamp(datetime(year=year, month=11, day=9))
            is_session = self.calendar.is_session(iqbal_day)
            is_weekend = iqbal_day.dayofweek in WEEKENDS
            if year <= 2013:
                self.assertFalse(is_session, iqbal_day)
            else:
                self.assertTrue(is_session or is_weekend, iqbal_day)
