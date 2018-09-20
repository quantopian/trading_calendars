from pandas.tseries.holiday import Holiday, Easter
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


# Whit Monday and Ascension day don't take observance as a parameter because
# they depend on a particular offset, and offset and observance cannot both
# be passed to a Holiday
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
