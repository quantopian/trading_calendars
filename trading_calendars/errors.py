#
# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from trading_calendars.utils.memoize import lazyval


class ZiplineCalendarError(Exception):
    msg = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @lazyval
    def message(self):
        return str(self)

    def __str__(self):
        msg = self.msg.format(**self.kwargs)
        return msg

    __unicode__ = __str__
    __repr__ = __str__


class InvalidCalendarName(ZiplineCalendarError):
    """
    Raised when a calendar with an invalid name is requested.
    """
    msg = (
        "The requested TradingCalendar, {calendar_name}, does not exist."
    )


class CalendarNameCollision(ZiplineCalendarError):
    """
    Raised when the static calendar registry already has a calendar with a
    given name.
    """
    msg = (
        "A calendar with the name {calendar_name} is already registered."
    )


class CyclicCalendarAlias(ZiplineCalendarError):
    """
    Raised when calendar aliases form a cycle.
    """
    msg = "Cycle in calendar aliases: [{cycle}]"


class ScheduleFunctionWithoutCalendar(ZiplineCalendarError):
    """
    Raised when schedule_function is called but there is not a calendar to be
    used in the construction of an event rule.
    """
    # TODO update message when new TradingSchedules are built
    msg = (
        "To use schedule_function, the TradingAlgorithm must be running on an "
        "ExchangeTradingSchedule, rather than {schedule}."
    )


class ScheduleFunctionInvalidCalendar(ZiplineCalendarError):
    """
    Raised when schedule_function is called with an invalid calendar argument.
    """
    msg = (
        "Invalid calendar '{given_calendar}' passed to schedule_function. "
        "Allowed options are {allowed_calendars}."
    )
