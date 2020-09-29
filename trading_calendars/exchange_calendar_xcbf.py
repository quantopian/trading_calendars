from datetime import time
from itertools import chain

import pandas as pd
from pandas.tseries.holiday import (
    Holiday,
    USPresidentsDay,
    USLaborDay,
    USThanksgivingDay,
    GoodFriday
)
from pytz import timezone

from trading_calendars import TradingCalendar
from trading_calendars.trading_calendar import HolidayCalendar
from trading_calendars.us_holidays import (
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USBlackFridayInOrAfter1993,
    USNewYearsDay,
    USIndependenceDay,
    Christmas,
    HurricaneSandyClosings,
    USNationalDaysofMourning,
)


def good_friday_unless_christmas_nye_friday(dt):
    """
    Good Friday is a valid trading day if Christmas Day or New Years Day fall
    on a Friday.
    """
    year_str = str(dt.year)
    christmas_weekday = Christmas.observance(
        pd.Timestamp(year_str+"-12-25")
    ).weekday()
    nyd_weekday = USNewYearsDay.observance(
        pd.Timestamp(year_str+"-01-01")
    ).weekday()
    if christmas_weekday != 4 and nyd_weekday != 4:
        return GoodFriday._apply_rule(
            pd.Timestamp(str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day))
        )
    else:
        # compatibility for pandas 0.18.1
        return pd.NaT


GoodFridayUnlessChristmasNYEFriday = Holiday(
    name="Good Friday XCBF",
    month=1,
    day=1,
    observance=good_friday_unless_christmas_nye_friday,
)


class XCBFExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the CBOE Futures Exchange (XCBF).

    http://cfe.cboe.com/aboutcfe/expirationcalendar.aspx

    Open Time: 8:30am, America/Chicago
    Close Time: 3:15pm, America/Chicago

    (We are ignoring extended trading hours for now)
    """
    name = 'XCBF'

    tz = timezone("America/Chicago")

    open_times = (
        (None, time(8, 31)),
    )

    close_times = (
        (None, time(15, 15)),
    )

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            USNewYearsDay,
            USMartinLutherKingJrAfter1998,
            USPresidentsDay,
            GoodFridayUnlessChristmasNYEFriday,
            USIndependenceDay,
            USMemorialDay,
            USLaborDay,
            USThanksgivingDay,
            Christmas
        ])

    @property
    def special_closes(self):
        return [(
            time(12, 15),
            HolidayCalendar([
                USBlackFridayInOrAfter1993,
            ])
        )]

    @property
    def adhoc_holidays(self):
        return list(chain(
            HurricaneSandyClosings,
            USNationalDaysofMourning,
        ))
