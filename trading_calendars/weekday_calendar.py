from datetime import time

from trading_calendars import TradingCalendar


class WeekdayCalendar(TradingCalendar):
    """
    A TradingCalendar for an exchange that is open every minute of every
    weekday.
    """
    @property
    def name(self):
        return '24/5'

    @property
    def tz(self):
        return 'UTC'

    @property
    def open_time(self):
        return time(0)

    @property
    def close_time(self):
        return time(23, 59)
