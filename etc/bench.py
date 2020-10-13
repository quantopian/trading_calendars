import itertools

from trading_calendars.calendar_utils import (
    _default_calendar_aliases,
    _default_calendar_factories,
    TradingCalendarDispatcher,
)


def construct_all_calendars():
    dispatcher = TradingCalendarDispatcher(
        calendars={},
        calendar_factories=_default_calendar_factories,
        aliases=_default_calendar_aliases,
    )

    calendar_names = itertools.chain(
        _default_calendar_aliases, _default_calendar_factories
    )

    for name in calendar_names:
        assert dispatcher.get_calendar(name) is not None
        dispatcher.deregister_calendar(name)


def test_calendar_construction(benchmark):
    benchmark(construct_all_calendars)
