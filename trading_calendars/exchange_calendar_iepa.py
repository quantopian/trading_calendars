from datetime import time
from itertools import chain

from pandas.tseries.holiday import (
    GoodFriday,
    USPresidentsDay,
    USLaborDay,
    USThanksgivingDay
)
from pandas import Timestamp
from pytz import timezone
from pytz import UTC

from trading_calendars import TradingCalendar
from trading_calendars.trading_calendar import HolidayCalendar
from trading_calendars.us_holidays import (
    USNewYearsDay,
    Christmas,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USIndependenceDay,
    USNationalDaysofMourning)


class IEPAExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for ICE US (IEPA).

    Open Time: 8pm, US/Eastern
    Close Time: 6pm, US/Eastern

    https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf # noqa
    """
    name = 'IEPA'

    tz = timezone("US/Eastern")

    open_times = (
        (None, time(20, 1)),
    )

    close_times = (
        (None, time(18)),
    )

    @property
    def open_offset(self):
        return -1

    @property
    def special_closes(self):
        return [
            (time(13), HolidayCalendar([
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                USMemorialDay,
                USIndependenceDay,
                USLaborDay,
                USThanksgivingDay
            ]))
        ]

    @property
    def adhoc_holidays(self):
        return list(chain(
            USNationalDaysofMourning,
            # ICE was only closed on the first day of the Hurricane Sandy
            # closings (was not closed on 2012-10-30)
            [Timestamp('2012-10-29', tz=UTC)]
        ))

    @property
    def regular_holidays(self):
        # https://www.theice.com/publicdocs/futures_us/exchange_notices/NewExNot2016Holidays.pdf # noqa
        return HolidayCalendar([
            USNewYearsDay,
            GoodFriday,
            Christmas
        ])
