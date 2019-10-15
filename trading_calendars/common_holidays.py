import pandas as pd
from pandas.tseries.holiday import DateOffset, Easter, FR, Holiday
from pandas.tseries.offsets import Day

from .trading_calendar import MONDAY, TUESDAY


def new_years_day(start_date=None,
                  end_date=None,
                  observance=None,
                  days_of_week=None):
    return Holiday(
        "New Year's Day",
        month=1,
        day=1,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def new_years_eve(start_date=None,
                  end_date=None,
                  observance=None,
                  days_of_week=None):
    return Holiday(
        "New Year's Eve",
        month=12,
        day=31,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def epiphany(start_date=None,
             end_date=None,
             observance=None,
             days_of_week=None):
    return Holiday(
        'Epiphany',
        month=1,
        day=6,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def anzac_day(start_date=None,
              end_date=None,
              observance=None,
              days_of_week=None):
    return Holiday(
        'Anzac Day',
        month=4,
        day=25,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def european_labour_day(start_date=None,
                        end_date=None,
                        observance=None,
                        days_of_week=None):
    return Holiday(
        "Labour Day",
        month=5,
        day=1,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


# Holy Wednesday, Maundy Thursday, Ascension Day, Whit Monday, and Corpus
# Christi do not take observance as a parameter because they depend on a
# particular offset, and offset and observance cannot both be passed to a
# Holiday.
def holy_wednesday(start_date=None, end_date=None, days_of_week=None):
    return Holiday(
        'Holy Wednesday',
        month=1,
        day=1,
        offset=[Easter(), -Day(4)],
        start_date=start_date,
        end_date=end_date,
        days_of_week=days_of_week,
    )


def maundy_thursday(start_date=None, end_date=None, days_of_week=None):
    return Holiday(
        'Maundy Thursday',
        month=1,
        day=1,
        offset=[Easter(), -Day(3)],
        start_date=start_date,
        end_date=end_date,
        days_of_week=days_of_week,
    )


def ascension_day(start_date=None, end_date=None):
    return Holiday(
        "Ascension Day",
        month=1,
        day=1,
        offset=[Easter(), Day(39)],
        start_date=start_date,
        end_date=end_date,
    )


def whit_monday(start_date=None, end_date=None):
    return Holiday(
        "Whit Monday",
        month=1,
        day=1,
        offset=[Easter(), Day(50)],
        start_date=start_date,
        end_date=end_date,
    )


def corpus_christi(start_date=None, end_date=None):
    return Holiday(
        'Corpus Christi',
        month=1,
        day=1,
        offset=[Easter(), Day(60)],
        start_date=start_date,
        end_date=end_date,
    )


def midsummer_eve(start_date=None, end_date=None):
    return Holiday(
        'Midsummer Eve',
        month=6,
        day=19,
        offset=DateOffset(weekday=FR(1)),
        start_date=start_date,
        end_date=end_date,
    )


def saint_peter_and_saint_paul_day(start_date=None,
                                   end_date=None,
                                   observance=None,
                                   days_of_week=None):
    return Holiday(
        'Saint Peter and Saint Paul Day',
        month=6,
        day=29,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def assumption_day(start_date=None,
                   end_date=None,
                   observance=None,
                   days_of_week=None):
    return Holiday(
        'Assumption Day',
        month=8,
        day=15,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def all_saints_day(start_date=None,
                   end_date=None,
                   observance=None,
                   days_of_week=None):
    return Holiday(
        'All Saints Day',
        month=11,
        day=1,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def immaculate_conception(start_date=None,
                          end_date=None,
                          observance=None,
                          days_of_week=None):
    return Holiday(
        'Immaculate Conception',
        month=12,
        day=8,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def christmas_eve(start_date=None,
                  end_date=None,
                  observance=None,
                  days_of_week=None):
    return Holiday(
        'Christmas Eve',
        month=12,
        day=24,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def christmas(start_date=None,
              end_date=None,
              observance=None,
              days_of_week=None):
    return Holiday(
        "Christmas",
        month=12,
        day=25,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def weekend_christmas(start_date=None, end_date=None, observance=None):
    """
    If christmas day is Saturday Monday 27th is a holiday
    If christmas day is sunday the Tuesday 27th is a holiday
    """
    return Holiday(
        "Weekend Christmas",
        month=12,
        day=27,
        days_of_week=(MONDAY, TUESDAY),
        start_date=start_date,
        end_date=end_date,
        observance=observance,
    )


def boxing_day(start_date=None,
               end_date=None,
               observance=None,
               days_of_week=None):
    return Holiday(
        "Boxing Day",
        month=12,
        day=26,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
        days_of_week=days_of_week,
    )


def weekend_boxing_day(start_date=None, end_date=None, observance=None):
    """
    If boxing day is saturday then Monday 28th is a holiday
    If boxing day is sunday then Tuesday 28th is a holiday
    """
    return Holiday(
        "Weekend Boxing Day",
        month=12,
        day=28,
        days_of_week=(MONDAY, TUESDAY),
        start_date=start_date,
        end_date=end_date,
        observance=observance,
    )


def chinese_national_day(start_date=None, end_date=None, observance=None):
    return Holiday(
        "Chinese National Day",
        month=10,
        day=1,
        start_date=start_date,
        end_date=end_date,
        observance=observance,
    )


# Precomputed Chinese Lunar Year dates.
#
# See Also
# --------
# trading_calendars/etc/lunisolar chinese-new-year
chinese_lunar_new_year_dates = pd.to_datetime([
    '1981-02-05',
    '1982-01-25',
    '1983-02-13',
    '1984-02-02',
    '1985-02-20',
    '1986-02-09',
    '1987-01-29',
    '1988-02-17',
    '1989-02-06',
    '1990-01-27',
    '1991-02-15',
    '1992-02-04',
    '1993-01-23',
    '1994-02-10',
    '1995-01-31',
    '1996-02-19',
    '1997-02-07',
    '1998-01-28',
    '1999-02-16',
    '2000-02-05',
    '2001-01-24',
    '2002-02-12',
    '2003-02-01',
    '2004-01-22',
    '2005-02-09',
    '2006-01-29',
    '2007-02-18',
    '2008-02-07',
    '2009-01-26',
    '2010-02-14',
    '2011-02-03',
    '2012-01-23',
    '2013-02-10',
    '2014-01-31',
    '2015-02-19',
    '2016-02-08',
    '2017-01-28',
    '2018-02-16',
    '2019-02-05',
    '2020-01-25',
    '2021-02-12',
    '2022-02-01',
    '2023-01-22',
    '2024-02-10',
    '2025-01-29',
    '2026-02-17',
    '2027-02-06',
    '2028-01-26',
    '2029-02-13',
    '2030-02-03',
    '2031-01-23',
    '2032-02-11',
    '2033-01-31',
    '2034-02-19',
    '2035-02-08',
    '2036-01-28',
    '2037-02-15',
    '2038-02-04',
    '2039-01-24',
    '2040-02-12',
    '2041-02-01',
    '2042-01-22',
    '2043-02-10',
    '2044-01-30',
    '2045-02-17',
    '2046-02-06',
    '2047-01-26',
    '2048-02-14',
    '2049-02-02',
])


# Precomputed Qingming Festival dates.
#
# See Also
# --------
# trading_calendars/etc/lunisolar qingming-festival
qingming_festival_dates = pd.to_datetime([
    '1980-04-04',
    '1981-04-05',
    '1982-04-05',
    '1983-04-05',
    '1984-04-04',
    '1985-04-05',
    '1986-04-05',
    '1987-04-05',
    '1988-04-04',
    '1989-04-05',
    '1990-04-05',
    '1991-04-05',
    '1992-04-04',
    '1993-04-05',
    '1994-04-05',
    '1995-04-05',
    '1996-04-04',
    '1997-04-05',
    '1998-04-05',
    '1999-04-05',
    '2000-04-04',
    '2001-04-05',
    '2002-04-05',
    '2003-04-05',
    '2004-04-04',
    '2005-04-05',
    '2006-04-05',
    '2007-04-05',
    '2008-04-04',
    '2009-04-04',
    '2010-04-05',
    '2011-04-05',
    '2012-04-04',
    '2013-04-04',
    '2014-04-05',
    '2015-04-05',
    '2016-04-04',
    '2017-04-04',
    '2018-04-05',
    '2019-04-05',
    '2020-04-04',
    '2021-04-04',
    '2022-04-05',
    '2023-04-05',
    '2024-04-04',
    '2025-04-04',
    '2026-04-05',
    '2027-04-05',
    '2028-04-04',
    '2029-04-04',
    '2030-04-05',
    '2031-04-05',
    '2032-04-04',
    '2033-04-04',
    '2034-04-05',
    '2035-04-05',
    '2036-04-04',
    '2037-04-04',
    '2038-04-05',
    '2039-04-05',
    '2040-04-04',
    '2041-04-04',
    '2042-04-04',
    '2043-04-05',
    '2044-04-04',
    '2045-04-04',
    '2046-04-04',
    '2047-04-05',
    '2048-04-04',
    '2049-04-04',
])


# Precomputed Buddha's Birthday dates on the Chinese Lunisolar Calendar.
#
# See Also
# --------
# trading_calendars/etc/lunisolar china-buddhas-birthday
#
# Notes
# -----
# The holiday "Buddha's Birthday" is celebrated in many countries, though
# different calendars are used. This function is for Buddha's Birthday on
# the Chinese Lunisolar Calendar, where it is the 8th day of the 4th month.
chinese_buddhas_birthday_dates = pd.to_datetime([
    '1981-05-11',
    '1982-05-01',
    '1983-05-20',
    '1984-05-08',
    '1985-05-27',
    '1986-05-16',
    '1987-05-05',
    '1988-05-23',
    '1989-05-12',
    '1990-05-02',
    '1991-05-21',
    '1992-05-10',
    '1993-05-28',
    '1994-05-18',
    '1995-05-07',
    '1996-05-24',
    '1997-05-14',
    '1998-05-03',
    '1999-05-22',
    '2000-05-11',
    '2001-04-30',
    '2002-05-19',
    '2003-05-08',
    '2004-05-26',
    '2005-05-15',
    '2006-05-05',
    '2007-05-24',
    '2008-05-12',
    '2009-05-02',
    '2010-05-21',
    '2011-05-10',
    '2012-04-28',
    '2013-05-17',
    '2014-05-06',
    '2015-05-25',
    '2016-05-14',
    '2017-05-03',
    '2018-05-22',
    '2019-05-12',
    '2020-04-30',
    '2021-05-19',
    '2022-05-08',
    '2023-05-26',
    '2024-05-15',
    '2025-05-05',
    '2026-05-24',
    '2027-05-13',
    '2028-05-02',
    '2029-05-20',
    '2030-05-09',
    '2031-05-28',
    '2032-05-16',
    '2033-05-06',
    '2034-04-26',
    '2035-05-15',
    '2036-05-03',
    '2037-05-22',
    '2038-05-11',
    '2039-04-30',
    '2040-05-18',
    '2041-05-07',
    '2042-05-26',
    '2043-05-16',
    '2044-05-05',
    '2045-05-24',
    '2046-05-13',
    '2047-05-02',
    '2048-05-20',
    '2049-05-09',
])


# Precomputed Dragon Boat (Tuen Ng Festival) dates.

# See Also
# --------
# trading_calendars/etc/lunisolar dragon-boat-festival
dragon_boat_festival_dates = pd.to_datetime([
    '1981-06-06',
    '1982-06-25',
    '1983-06-15',
    '1984-06-04',
    '1985-06-22',
    '1986-06-11',
    '1987-06-01',
    '1988-06-18',
    '1989-06-08',
    '1990-05-28',
    '1991-06-16',
    '1992-06-05',
    '1993-06-24',
    '1994-06-13',
    '1995-06-02',
    '1996-06-20',
    '1997-06-09',
    '1998-05-30',
    '1999-06-18',
    '2000-06-06',
    '2001-06-25',
    '2002-06-15',
    '2003-06-04',
    '2004-06-22',
    '2005-06-11',
    '2006-05-31',
    '2007-06-19',
    '2008-06-08',
    '2009-05-28',
    '2010-06-16',
    '2011-06-06',
    '2012-06-23',
    '2013-06-12',
    '2014-06-02',
    '2015-06-20',
    '2016-06-09',
    '2017-05-30',
    '2018-06-18',
    '2019-06-07',
    '2020-06-25',
    '2021-06-14',
    '2022-06-03',
    '2023-06-22',
    '2024-06-10',
    '2025-05-31',
    '2026-06-19',
    '2027-06-09',
    '2028-05-28',
    '2029-06-16',
    '2030-06-05',
    '2031-06-24',
    '2032-06-12',
    '2033-06-01',
    '2034-05-22',
    '2035-06-10',
    '2036-05-30',
    '2037-06-18',
    '2038-06-07',
    '2039-05-27',
    '2040-06-14',
    '2041-06-03',
    '2042-06-22',
    '2043-06-11',
    '2044-05-31',
    '2045-06-19',
    '2046-06-08',
    '2047-05-29',
    '2048-06-15',
    '2049-06-04',
])


# Precomputed Day after the Mid-Autumn Festival

# See Also
# --------
# trading_calendars/etc/lunisolar mid-autumn-festival
mid_autumn_festival_dates = pd.to_datetime([
    '1981-09-12',
    '1982-10-01',
    '1983-09-21',
    '1984-09-10',
    '1985-09-29',
    '1986-09-18',
    '1987-10-07',
    '1988-09-25',
    '1989-09-14',
    '1990-10-03',
    '1991-09-22',
    '1992-09-11',
    '1993-09-30',
    '1994-09-20',
    '1995-09-09',
    '1996-09-27',
    '1997-09-16',
    '1998-10-05',
    '1999-09-24',
    '2000-09-12',
    '2001-10-01',
    '2002-09-21',
    '2003-09-11',
    '2004-09-28',
    '2005-09-18',
    '2006-10-06',
    '2007-09-25',
    '2008-09-14',
    '2009-10-03',
    '2010-09-22',
    '2011-09-12',
    '2012-09-30',
    '2013-09-19',
    '2014-09-08',
    '2015-09-27',
    '2016-09-15',
    '2017-10-04',
    '2018-09-24',
    '2019-09-13',
    '2020-10-01',
    '2021-09-21',
    '2022-09-10',
    '2023-09-29',
    '2024-09-17',
    '2025-10-06',
    '2026-09-25',
    '2027-09-15',
    '2028-10-03',
    '2029-09-22',
    '2030-09-12',
    '2031-10-01',
    '2032-09-19',
    '2033-09-08',
    '2034-08-28',
    '2035-09-16',
    '2036-10-04',
    '2037-09-24',
    '2038-09-13',
    '2039-10-02',
    '2040-09-20',
    '2041-09-10',
    '2042-09-28',
    '2043-09-17',
    '2044-10-05',
    '2045-09-25',
    '2046-09-15',
    '2047-10-04',
    '2048-09-22',
    '2049-09-11',
])


# Precomputed Double Ninth Festival (Chung Yeung Festival) dates.
#
# See Also
# --------
# trading_calendars/etc/lunisolar double-ninth-festival
double_ninth_festival_dates = pd.to_datetime([
    '1981-10-06',
    '1982-10-25',
    '1983-10-14',
    '1984-10-03',
    '1985-10-22',
    '1986-10-12',
    '1987-10-31',
    '1988-10-19',
    '1989-10-08',
    '1990-10-26',
    '1991-10-16',
    '1992-10-04',
    '1993-10-23',
    '1994-10-13',
    '1995-11-01',
    '1996-10-20',
    '1997-10-10',
    '1998-10-28',
    '1999-10-17',
    '2000-10-06',
    '2001-10-25',
    '2002-10-14',
    '2003-10-04',
    '2004-10-22',
    '2005-10-11',
    '2006-10-30',
    '2007-10-19',
    '2008-10-07',
    '2009-10-26',
    '2010-10-16',
    '2011-10-05',
    '2012-10-23',
    '2013-10-13',
    '2014-10-02',
    '2015-10-21',
    '2016-10-09',
    '2017-10-28',
    '2018-10-17',
    '2019-10-07',
    '2020-10-25',
    '2021-10-14',
    '2022-10-04',
    '2023-10-23',
    '2024-10-11',
    '2025-10-29',
    '2026-10-18',
    '2027-10-08',
    '2028-10-26',
    '2029-10-16',
    '2030-10-05',
    '2031-10-24',
    '2032-10-12',
    '2033-10-01',
    '2034-09-21',
    '2035-10-09',
    '2036-10-27',
    '2037-10-17',
    '2038-10-07',
    '2039-10-26',
    '2040-10-14',
    '2041-10-03',
    '2042-10-22',
    '2043-10-11',
    '2044-10-29',
    '2045-10-18',
    '2046-10-08',
    '2047-10-27',
    '2048-10-16',
    '2049-10-05',
])

# These dates were initially calculated using the ummalqura Python
# package (https://pypi.org/project/ummalqura/), and then tweaked
# to fit Turkey's observance of Eid al-Fitr.  Other countries that
# observe Eid al-Fitr might use slightly different dates
eid_al_fitr_first_day = pd.to_datetime([
    '1981-08-01',
    '1982-07-21',
    '1983-07-11',
    '1984-06-30',
    '1985-06-19',
    '1986-06-08',
    '1987-05-28',
    '1988-05-16',
    '1989-05-06',
    '1990-04-26',
    '1991-04-15',
    '1992-04-04',
    '1993-03-24',
    '1994-03-13',
    '1995-03-02',
    '1996-02-19',
    '1997-02-08',
    '1998-01-29',
    '1999-01-18',
    '2000-01-08',
    '2000-12-27',
    '2001-12-16',
    '2002-12-05',
    '2003-11-25',
    '2004-11-14',
    '2005-11-03',
    '2006-10-23',
    '2007-10-12',
    '2008-09-30',
    '2009-09-20',
    '2010-09-09',
    '2011-08-30',
    '2012-08-19',
    '2013-08-08',
    '2014-07-28',
    '2015-07-17',
    '2016-07-05',
    '2017-06-25',
    '2018-06-15',
    '2019-06-04',
    '2020-05-24',
    '2021-05-13',
    '2022-05-02',
    '2023-04-21',
    '2024-04-10',
    '2025-03-30',
    '2026-03-20',
    '2027-03-09',
    '2028-02-26',
    '2029-02-14',
    '2030-02-04',
    '2031-01-24',
    '2032-01-14',
    '2033-01-02',
    '2033-12-23',
    '2034-12-12',
    '2035-12-01',
    '2036-11-19',
    '2037-11-08',
    '2038-10-29',
    '2039-10-19',
    '2040-10-07',
    '2041-09-26',
    '2042-09-15',
    '2043-09-04',
    '2044-08-24',
    '2045-08-14',
    '2046-08-03',
    '2047-07-24',
    '2048-07-12',
    '2049-07-01',
])

# These dates were initially calculated using the ummalqura Python
# package (https://pypi.org/project/ummalqura/), and then tweaked
# to fit Turkey's observance of Eid al-Adha.  Other countries that
# observe Eid al-Adha might use slightly different dates
eid_al_adha_first_day = pd.to_datetime([
    '1981-10-08',
    '1982-09-27',
    '1983-09-17',
    '1984-09-05',
    '1985-08-26',
    '1986-08-15',
    '1987-08-04',
    '1988-07-23',
    '1989-07-13',
    '1990-07-02',
    '1991-06-22',
    '1992-06-11',
    '1993-05-31',
    '1994-05-20',
    '1995-05-09',
    '1996-04-27',
    '1997-04-17',
    '1998-04-07',
    '1999-03-27',
    '2000-03-16',
    '2001-03-05',
    '2002-02-22',
    '2003-02-10',
    '2004-02-01',
    '2005-01-20',
    '2006-01-09',
    '2006-12-31',
    '2007-12-20',
    '2008-12-08',
    '2009-11-27',
    '2010-11-16',
    '2011-11-06',
    '2012-10-25',
    '2013-10-15',
    '2014-10-04',
    '2015-09-24',
    '2016-09-12',
    '2017-09-01',
    '2018-08-21',
    '2019-08-11',
    '2020-07-31',
    '2021-07-20',
    '2022-07-09',
    '2023-06-28',
    '2024-06-16',
    '2025-06-06',
    '2026-05-27',
    '2027-05-16',
    '2028-05-05',
    '2029-04-24',
    '2030-04-13',
    '2031-04-02',
    '2032-03-22',
    '2033-03-11',
    '2034-03-01',
    '2035-02-18',
    '2036-02-07',
    '2037-01-26',
    '2038-01-16',
    '2039-01-05',
    '2039-12-26',
    '2040-12-14',
    '2041-12-04',
    '2042-11-23',
    '2043-11-12',
    '2044-10-31',
    '2045-10-21',
    '2046-10-10',
    '2047-09-30',
    '2048-09-19',
    '2049-09-08',
])
