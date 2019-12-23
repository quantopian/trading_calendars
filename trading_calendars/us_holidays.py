from pandas import (
    Timestamp,
    DateOffset,
)
from pytz import UTC

from pandas.tseries.holiday import (
    Holiday,
    sunday_to_monday,
    nearest_workday,
)

from dateutil.relativedelta import (
    MO,
    TH
)
from pandas.tseries.offsets import Day

from .common_holidays import new_years_day
from .trading_calendar import (
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
)


def july_5th_holiday_observance(datetime_index):
    return datetime_index[
        (datetime_index.year != 2013) & (datetime_index.year != 2019)
    ]


# These have the same definition, but are used in different places because the
# NYSE closed at 2:00 PM on Christmas Eve until 1993.
ChristmasEveBefore1993 = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
    end_date=Timestamp('1993-01-01'),
    # When Christmas is a Saturday, the 24th is a full holiday.
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
)
ChristmasEveInOrAfter1993 = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
    start_date=Timestamp('1993-01-01'),
    # When Christmas is a Saturday, the 24th is a full holiday.
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
)
USNewYearsDay = new_years_day(
    # When Jan 1 is a Sunday, US markets observe the subsequent Monday.
    # When Jan 1 is a Saturday (as in 2005 and 2011), no holiday is observed.
    observance=sunday_to_monday
)
USMartinLutherKingJrAfter1998 = Holiday(
    'Dr. Martin Luther King Jr. Day',
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp('1998-01-01'),
    offset=DateOffset(weekday=MO(3)),
)
USMemorialDay = Holiday(
    # NOTE: The definition for Memorial Day is incorrect as of pandas 0.16.0.
    # See https://github.com/pydata/pandas/issues/9760.
    'Memorial Day',
    month=5,
    day=25,
    offset=DateOffset(weekday=MO(1)),
)
USIndependenceDay = Holiday(
    'July 4th',
    month=7,
    day=4,
    observance=nearest_workday,
)
Christmas = Holiday(
    'Christmas',
    month=12,
    day=25,
    observance=nearest_workday,
)

MonTuesThursBeforeIndependenceDay = Holiday(
    # When July 4th is a Tuesday, Wednesday, or Friday, the previous day is a
    # half day.
    'Mondays, Tuesdays, and Thursdays Before Independence Day',
    month=7,
    day=3,
    days_of_week=(MONDAY, TUESDAY, THURSDAY),
    start_date=Timestamp("1995-01-01"),
)
FridayAfterIndependenceDayExcept2013and2019 = Holiday(
    # When July 4th is a Thursday, the next day is a half day (except in 2013,
    # and 2019 when, for no explicable reason, Wednesday was a half day
    # instead).
    "Fridays after Independence Day that aren't in 2013,2019",
    month=7,
    day=5,
    days_of_week=(FRIDAY,),
    observance=july_5th_holiday_observance,
    start_date=Timestamp("1995-01-01"),
)
USBlackFridayBefore1993 = Holiday(
    'Black Friday',
    month=11,
    day=1,
    # Black Friday was not observed until 1992.
    start_date=Timestamp('1992-01-01'),
    end_date=Timestamp('1993-01-01'),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)
USBlackFridayInOrAfter1993 = Holiday(
    'Black Friday',
    month=11,
    day=1,
    start_date=Timestamp('1993-01-01'),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)
BattleOfGettysburg = Holiday(
    # All of the floor traders in Chicago were sent to PA
    'Markets were closed during the battle of Gettysburg',
    month=7,
    day=(1, 2, 3),
    start_date=Timestamp("1863-07-01"),
    end_date=Timestamp("1863-07-03")
)


# http://en.wikipedia.org/wiki/Aftermath_of_the_September_11_attacks
# use list for consistency in returning ad-hoc dates
September11Closings = [
    Timestamp('2001-09-11', tz=UTC),
    Timestamp('2001-09-12', tz=UTC),
    Timestamp('2001-09-13', tz=UTC),
    Timestamp('2001-09-14', tz=UTC)
]

# http://en.wikipedia.org/wiki/Hurricane_sandy
# use list for consistency in returning ad-hoc dates
HurricaneSandyClosings = [
    Timestamp('2012-10-29', tz=UTC),
    Timestamp('2012-10-30', tz=UTC)
]

# add Hurricane Gloria closing
# http://s3.amazonaws.com/armstrongeconomics-wp/2013/07/NYSE-Closings.pdf
# use singleton list as must be iterable type
HurricaneGloriaClosing = [
    Timestamp('1985-09-27', tz=UTC)
]

# add New York Blackout closing
# http://s3.amazonaws.com/armstrongeconomics-wp/2013/07/NYSE-Closings.pdf
# use singleton list as must be iterable type
NewYorkBlackout = [
    Timestamp('1977-07-14', tz=UTC)
]

# add closings for pre-1980 Presidential Election Day closings
# http://s3.amazonaws.com/armstrongeconomics-wp/2013/07/NYSE-Closings.pdf
PresidentialElectionDays = [
    Timestamp('1972-11-07', tz=UTC),
    Timestamp('1976-11-02', tz=UTC),
    Timestamp('1980-11-04', tz=UTC)
]

# National Days of Mourning
# - President Harry S. Truman - December 28, 1972
# - President Lyndon B. Johnson - January 25, 1973
# - President Richard Nixon - April 27, 1994
# - President Ronald W. Reagan - June 11, 2004
# - President Gerald R. Ford - Jan 2, 2007
# - President George H.W. Bush - Dec 5, 2018
# added Truman and Johnson to go back to 1970
# http://s3.amazonaws.com/armstrongeconomics-wp/2013/07/NYSE-Closings.pdf
USNationalDaysofMourning = [
    Timestamp('1972-12-28', tz=UTC),
    Timestamp('1973-01-25', tz=UTC),
    Timestamp('1994-04-27', tz=UTC),
    Timestamp('2004-06-11', tz=UTC),
    Timestamp('2007-01-02', tz=UTC),
    Timestamp('2018-12-05', tz=UTC),
]
