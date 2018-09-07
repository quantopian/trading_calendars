from datetime import time

from trading_calendars import TradingCalendar


class AlwaysOpenCalendar(TradingCalendar):
    """A TradingCalendar for an exchange that's open every minute of every day.
    """
    @property
    def name(self):
        return '24/7'

    @property
    def tz(self):
        return 'UTC'

    @property
    def weekmask(self):
        return '1111111'

    @property
    def open_time(self):
        return time(0)

    @property
    def close_time(self):
        return time(23, 59)
