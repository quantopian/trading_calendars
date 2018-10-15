from datetime import time
from itertools import chain

from pandas.tseries.holiday import (
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
            GoodFriday,
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
