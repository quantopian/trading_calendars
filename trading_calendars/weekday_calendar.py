from datetime import time
from pytz import UTC

from trading_calendars import TradingCalendar


class WeekdayCalendar(TradingCalendar):
    """
    A TradingCalendar for an exchange that is open every minute of every
    weekday.
    """
    name = '24/5'
    tz = UTC
    open_times = (
        (None, time(0)),
    )
    close_times = (
        (None, time(23, 59)),
    )
