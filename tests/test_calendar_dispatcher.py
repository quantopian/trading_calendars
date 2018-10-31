"""
Tests for TradingCalendarDispatcher.
"""
from unittest import TestCase
from trading_calendars.errors import (
    CalendarNameCollision,
    CyclicCalendarAlias,
    InvalidCalendarName,
)
from trading_calendars.calendar_utils import TradingCalendarDispatcher
from trading_calendars.exchange_calendar_iepa import IEPAExchangeCalendar


class CalendarAliasTestCase(TestCase):

    @classmethod
    def setupClass(cls):
        # Make a calendar once so that we don't spend time in every test
        # instantiating calendars.
        cls.dispatcher_kwargs = dict(
            calendars={'IEPA': IEPAExchangeCalendar()},
            calendar_factories={},
            aliases={
                'IEPA_ALIAS': 'IEPA',
                'IEPA_ALIAS_ALIAS': 'IEPA_ALIAS',
            },
        )

    def setUp(self):
        self.dispatcher = TradingCalendarDispatcher(
            # Make copies here so that tests that mutate the dispatcher dicts
            # are isolated from one another.
            **{k: v.copy() for k, v in self.dispatcher_kwargs.items()}
        )

    def tearDown(self):
        self.dispatcher = None

    @classmethod
    def tearDownClass(cls):
        cls.dispatcher_kwargs = None

    def test_follow_alias_chain(self):
        self.assertIs(
            self.dispatcher.get_calendar('IEPA_ALIAS'),
            self.dispatcher.get_calendar('IEPA'),
        )
        self.assertIs(
            self.dispatcher.get_calendar('IEPA_ALIAS_ALIAS'),
            self.dispatcher.get_calendar('IEPA'),
        )

    def test_add_new_aliases(self):
        with self.assertRaises(InvalidCalendarName):
            self.dispatcher.get_calendar('NOT_IEPA')

        self.dispatcher.register_calendar_alias('NOT_IEPA', 'IEPA')

        self.assertIs(
            self.dispatcher.get_calendar('NOT_IEPA'),
            self.dispatcher.get_calendar('IEPA'),
        )

        self.dispatcher.register_calendar_alias(
            'IEPA_ALIAS_ALIAS_ALIAS',
            'IEPA_ALIAS_ALIAS'
        )
        self.assertIs(
            self.dispatcher.get_calendar('IEPA_ALIAS_ALIAS_ALIAS'),
            self.dispatcher.get_calendar('IEPA'),
        )

    def test_remove_aliases(self):
        self.dispatcher.deregister_calendar('IEPA_ALIAS_ALIAS')
        with self.assertRaises(InvalidCalendarName):
            self.dispatcher.get_calendar('IEPA_ALIAS_ALIAS')

    def test_reject_alias_that_already_exists(self):
        with self.assertRaises(CalendarNameCollision):
            self.dispatcher.register_calendar_alias('IEPA', 'NOT_IEPA')

        with self.assertRaises(CalendarNameCollision):
            self.dispatcher.register_calendar_alias('IEPA_ALIAS', 'NOT_IEPA')

    def test_allow_alias_override_with_force(self):
        self.dispatcher.register_calendar_alias('IEPA', 'NOT_IEPA', force=True)
        with self.assertRaises(InvalidCalendarName):
            self.dispatcher.get_calendar('IEPA')

    def test_reject_cyclic_aliases(self):
        add_alias = self.dispatcher.register_calendar_alias

        add_alias('A', 'B')
        add_alias('B', 'C')

        with self.assertRaises(CyclicCalendarAlias) as e:
            add_alias('C', 'A')

        expected = "Cycle in calendar aliases: ['C' -> 'A' -> 'B' -> 'C']"
        self.assertEqual(str(e.exception), expected)
