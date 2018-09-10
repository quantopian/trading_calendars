from datetime import time
from itertools import chain
from pytz import timezone

from trading_calendars.trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
)
from .tse_holidays import (
    NewYearsHolidayDec31,
    NewYearsHolidayJan1,
    NewYearsHolidayJan2,
    NewYearsHolidayJan3,
    ComingOfAgeDay,
    NationalFoundationDay,
    VernalEquinoxes,
    GreeneryDayThrough2006,
    ShowaDay,
    ConstitutionMemorialDay,
    GreeneryDay2007Onwards,
    CitizensHolidayGoldenWeek,
    ChildrensDay,
    MarineDay2000to2002,
    MarineDay2003Onwards,
    AutumnalEquinoxes,
    CitizensHolidaySilverWeek,
    RespectForTheAgedDay2000to2002,
    RespectForTheAgedDay2003Onwards,
    HealthAndSportsDay,
    CultureDay,
    LaborThanksgivingDay,
    EmperorAkihitoBirthday,
    EmperorNaruhitoBirthday,
)


class TSEExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Tokyo Stock Exchange

    First session: 9:00am - 11:30am
    Lunch
    Second session: 12:30pm - 3:00pm

    NOTE: we are treating the two sessions per day as one session for now,
    because we will not be handling minutely data in the immediate future.

    Regularly-Observed Holidays (see tse_holidays.py for more info):
    - New Year's Holidays (Dec. 31 - Jan. 3)
    - Coming of Age Day (second Monday of January)
    - National Foundation Day (Feb. 11)
    - Vernal Equinox (usually Mar 20-22)
    - Greenery Day (Apr. 29 2000-2006, May 4 2007-present)
    - Showa Day (Apr. 29 2007-present)
    - Constitution Memorial Day (May 3)
    - Citizen's Holiday (May 4 2000-2006, later replaced by Greenery Day)
    - Children's Day (May 5)
    - Marine Day (July 20 2000-2002, third Monday of July 2003-present)
    - Respect for the Aged Day (Sep. 15 2000-2002, third Monday
      of Sep. 2003-present)
    - Autumnal Equinox (usually Sept. 22-24)
    - Health-Sports Day (second Monday of October)
    - Culture Day (November 3)
    - Labor Thanksgiving Day (Nov. 23)
    - Emperor's Birthday (Dec. 23)
    """

    @property
    def name(self):
        return "TSE"

    @property
    def tz(self):
        return timezone('Japan')

    @property
    def open_time(self):
        return time(9, 1)

    @property
    def close_time(self):
        return time(15)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            NewYearsHolidayDec31,
            NewYearsHolidayJan1,
            NewYearsHolidayJan2,
            NewYearsHolidayJan3,
            ComingOfAgeDay,
            NationalFoundationDay,
            GreeneryDayThrough2006,
            ShowaDay,
            ConstitutionMemorialDay,
            GreeneryDay2007Onwards,
            CitizensHolidayGoldenWeek,
            ChildrensDay,
            MarineDay2000to2002,
            MarineDay2003Onwards,
            RespectForTheAgedDay2000to2002,
            RespectForTheAgedDay2003Onwards,
            HealthAndSportsDay,
            CultureDay,
            LaborThanksgivingDay,
            EmperorAkihitoBirthday,
            EmperorNaruhitoBirthday,
        ])

    @property
    def adhoc_holidays(self):
        return list(chain(
            VernalEquinoxes,
            AutumnalEquinoxes,
            CitizensHolidaySilverWeek,
        ))
