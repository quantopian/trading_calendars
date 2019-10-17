from .always_open import AlwaysOpenCalendar
from .errors import (
    CalendarNameCollision,
    CyclicCalendarAlias,
    InvalidCalendarName,
)
from .exchange_calendar_asex import ASEXExchangeCalendar
from .exchange_calendar_bvmf import BVMFExchangeCalendar
from .exchange_calendar_cmes import CMESExchangeCalendar
from .exchange_calendar_iepa import IEPAExchangeCalendar
from .exchange_calendar_xams import XAMSExchangeCalendar
from .exchange_calendar_xasx import XASXExchangeCalendar
from .exchange_calendar_xbkk import XBKKExchangeCalendar
from .exchange_calendar_xbog import XBOGExchangeCalendar
from .exchange_calendar_xbom import XBOMExchangeCalendar
from .exchange_calendar_xbru import XBRUExchangeCalendar
from .exchange_calendar_xbud import XBUDExchangeCalendar
from .exchange_calendar_xbue import XBUEExchangeCalendar
from .exchange_calendar_xcbf import XCBFExchangeCalendar
from .exchange_calendar_xcse import XCSEExchangeCalendar
from .exchange_calendar_xdub import XDUBExchangeCalendar
from .exchange_calendar_xfra import XFRAExchangeCalendar
from .exchange_calendar_xhel import XHELExchangeCalendar
from .exchange_calendar_xhkg import XHKGExchangeCalendar
from .exchange_calendar_xice import XICEExchangeCalendar
from .exchange_calendar_xidx import XIDXExchangeCalendar
from .exchange_calendar_xist import XISTExchangeCalendar
from .exchange_calendar_xjse import XJSEExchangeCalendar
from .exchange_calendar_xkar import XKARExchangeCalendar
from .exchange_calendar_xkls import XKLSExchangeCalendar
from .exchange_calendar_xkrx import XKRXExchangeCalendar
from .exchange_calendar_xlim import XLIMExchangeCalendar
from .exchange_calendar_xlis import XLISExchangeCalendar
from .exchange_calendar_xlon import XLONExchangeCalendar
from .exchange_calendar_xmad import XMADExchangeCalendar
from .exchange_calendar_xmex import XMEXExchangeCalendar
from .exchange_calendar_xmil import XMILExchangeCalendar
from .exchange_calendar_xmos import XMOSExchangeCalendar
from .exchange_calendar_xnys import XNYSExchangeCalendar
from .exchange_calendar_xnze import XNZEExchangeCalendar
from .exchange_calendar_xosl import XOSLExchangeCalendar
from .exchange_calendar_xpar import XPARExchangeCalendar
from .exchange_calendar_xphs import XPHSExchangeCalendar
from .exchange_calendar_xpra import XPRAExchangeCalendar
from .exchange_calendar_xses import XSESExchangeCalendar
from .exchange_calendar_xsgo import XSGOExchangeCalendar
from .exchange_calendar_xshg import XSHGExchangeCalendar
from .exchange_calendar_xsto import XSTOExchangeCalendar
from .exchange_calendar_xswx import XSWXExchangeCalendar
from .exchange_calendar_xtai import XTAIExchangeCalendar
from .exchange_calendar_xtks import XTKSExchangeCalendar
from .exchange_calendar_xtse import XTSEExchangeCalendar
from .exchange_calendar_xwar import XWARExchangeCalendar
from .exchange_calendar_xwbo import XWBOExchangeCalendar
from .us_futures_calendar import QuantopianUSFuturesCalendar
from .weekday_calendar import WeekdayCalendar

_default_calendar_factories = {
    # Exchange calendars.
    'ASEX': ASEXExchangeCalendar,
    'BVMF': BVMFExchangeCalendar,
    'CMES': CMESExchangeCalendar,
    'IEPA': IEPAExchangeCalendar,
    'XAMS': XAMSExchangeCalendar,
    'XASX': XASXExchangeCalendar,
    'XBKK': XBKKExchangeCalendar,
    'XBOG': XBOGExchangeCalendar,
    'XBOM': XBOMExchangeCalendar,
    'XBRU': XBRUExchangeCalendar,
    'XBUD': XBUDExchangeCalendar,
    'XBUE': XBUEExchangeCalendar,
    'XCBF': XCBFExchangeCalendar,
    'XCSE': XCSEExchangeCalendar,
    'XDUB': XDUBExchangeCalendar,
    'XFRA': XFRAExchangeCalendar,
    'XHEL': XHELExchangeCalendar,
    'XHKG': XHKGExchangeCalendar,
    'XICE': XICEExchangeCalendar,
    'XIDX': XIDXExchangeCalendar,
    'XIST': XISTExchangeCalendar,
    'XJSE': XJSEExchangeCalendar,
    'XKAR': XKARExchangeCalendar,
    'XKLS': XKLSExchangeCalendar,
    'XKRX': XKRXExchangeCalendar,
    'XLIM': XLIMExchangeCalendar,
    'XLIS': XLISExchangeCalendar,
    'XLON': XLONExchangeCalendar,
    'XMAD': XMADExchangeCalendar,
    'XMEX': XMEXExchangeCalendar,
    'XMIL': XMILExchangeCalendar,
    'XMOS': XMOSExchangeCalendar,
    'XNYS': XNYSExchangeCalendar,
    'XNZE': XNZEExchangeCalendar,
    'XOSL': XOSLExchangeCalendar,
    'XPAR': XPARExchangeCalendar,
    'XPHS': XPHSExchangeCalendar,
    'XPRA': XPRAExchangeCalendar,
    'XSES': XSESExchangeCalendar,
    'XSGO': XSGOExchangeCalendar,
    'XSHG': XSHGExchangeCalendar,
    'XSTO': XSTOExchangeCalendar,
    'XSWX': XSWXExchangeCalendar,
    'XTAI': XTAIExchangeCalendar,
    'XTKS': XTKSExchangeCalendar,
    'XTSE': XTSEExchangeCalendar,
    'XWAR': XWARExchangeCalendar,
    'XWBO': XWBOExchangeCalendar,
    # Miscellaneous calendars.
    'us_futures': QuantopianUSFuturesCalendar,
    '24/7': AlwaysOpenCalendar,
    '24/5': WeekdayCalendar,
}
_default_calendar_aliases = {
    'NYSE': 'XNYS',
    'NASDAQ': 'XNYS',
    'BATS': 'XNYS',
    'FWB': 'XFRA',
    'LSE': 'XLON',
    'TSX': 'XTSE',
    'BMF': 'BVMF',
    'CME': 'CMES',
    'CBOT': 'CMES',
    'COMEX': 'CMES',
    'NYMEX': 'CMES',
    'ICE': 'IEPA',
    'ICEUS': 'IEPA',
    'NYFE': 'IEPA',
    'CFE': 'XCBF',
    'JKT': 'XIDX',
}
default_calendar_names = sorted(_default_calendar_factories.keys())


class TradingCalendarDispatcher(object):
    """
    A class for dispatching and caching trading calendars.

    Methods of a global instance of this class are provided by
    calendars.calendar_utils.

    Parameters
    ----------
    calendars : dict[str -> TradingCalendar]
        Initial set of calendars.
    calendar_factories : dict[str -> function]
        Factories for lazy calendar creation.
    aliases : dict[str -> str]
        Calendar name aliases.
    """
    def __init__(self, calendars, calendar_factories, aliases):
        self._calendars = calendars
        self._calendar_factories = dict(calendar_factories)
        self._aliases = dict(aliases)

    def get_calendar(self, name):
        """
        Retrieves an instance of an TradingCalendar whose name is given.

        Parameters
        ----------
        name : str
            The name of the TradingCalendar to be retrieved.

        Returns
        -------
        calendar : calendars.TradingCalendar
            The desired calendar.
        """
        canonical_name = self.resolve_alias(name)

        try:
            return self._calendars[canonical_name]
        except KeyError:
            # We haven't loaded this calendar yet, so make a new one.
            pass

        try:
            factory = self._calendar_factories[canonical_name]
        except KeyError:
            # We don't have a factory registered for this name.  Barf.
            raise InvalidCalendarName(calendar_name=name)

        # Cache the calendar for future use.
        calendar = self._calendars[canonical_name] = factory()
        return calendar

    def has_calendar(self, name):
        """
        Do we have (or have the ability to make) a calendar with ``name``?
        """
        return (
            name in self._calendars
            or name in self._calendar_factories
            or name in self._aliases
        )

    def register_calendar(self, name, calendar, force=False):
        """
        Registers a calendar for retrieval by the get_calendar method.

        Parameters
        ----------
        name: str
            The key with which to register this calendar.
        calendar: TradingCalendar
            The calendar to be registered for retrieval.
        force : bool, optional
            If True, old calendars will be overwritten on a name collision.
            If False, name collisions will raise an exception.
            Default is False.

        Raises
        ------
        CalendarNameCollision
            If a calendar is already registered with the given calendar's name.
        """
        if force:
            self.deregister_calendar(name)

        if self.has_calendar(name):
            raise CalendarNameCollision(calendar_name=name)

        self._calendars[name] = calendar

    def register_calendar_type(self, name, calendar_type, force=False):
        """
        Registers a calendar by type.

        This is useful for registering a new calendar to be lazily instantiated
        at some future point in time.

        Parameters
        ----------
        name: str
            The key with which to register this calendar.
        calendar_type: type
            The type of the calendar to register.
        force : bool, optional
            If True, old calendars will be overwritten on a name collision.
            If False, name collisions will raise an exception.
            Default is False.

        Raises
        ------
        CalendarNameCollision
            If a calendar is already registered with the given calendar's name.
        """
        if force:
            self.deregister_calendar(name)

        if self.has_calendar(name):
            raise CalendarNameCollision(calendar_name=name)

        self._calendar_factories[name] = calendar_type

    def register_calendar_alias(self, alias, real_name, force=False):
        """
        Register an alias for a calendar.

        This is useful when multiple exchanges should share a calendar, or when
        there are multiple ways to refer to the same exchange.

        After calling ``register_alias('alias', 'real_name')``, subsequent
        calls to ``get_calendar('alias')`` will return the same result as
        ``get_calendar('real_name')``.

        Parameters
        ----------
        alias : str
            The name to be used to refer to a calendar.
        real_name : str
            The canonical name of the registered calendar.
        force : bool, optional
            If True, old calendars will be overwritten on a name collision.
            If False, name collisions will raise an exception.
            Default is False.
        """
        if force:
            self.deregister_calendar(alias)

        if self.has_calendar(alias):
            raise CalendarNameCollision(calendar_name=alias)

        self._aliases[alias] = real_name

        # Ensure that the new alias doesn't create a cycle, and back it out if
        # we did.
        try:
            self.resolve_alias(alias)
        except CyclicCalendarAlias:
            del self._aliases[alias]
            raise

    def resolve_alias(self, name):
        """
        Resolve a calendar alias for retrieval.

        Parameters
        ----------
        name : str
            The name of the requested calendar.

        Returns
        -------
        canonical_name : str
            The real name of the calendar to create/return.
        """
        seen = []

        while name in self._aliases:
            seen.append(name)
            name = self._aliases[name]

            # This is O(N ** 2), but if there's an alias chain longer than 2,
            # something strange has happened.
            if name in seen:
                seen.append(name)
                raise CyclicCalendarAlias(
                    cycle=" -> ".join(repr(k) for k in seen)
                )

        return name

    def deregister_calendar(self, name):
        """
        If a calendar is registered with the given name, it is de-registered.

        Parameters
        ----------
        cal_name : str
            The name of the calendar to be deregistered.
        """
        self._calendars.pop(name, None)
        self._calendar_factories.pop(name, None)
        self._aliases.pop(name, None)

    def clear_calendars(self):
        """
        Deregisters all current registered calendars
        """
        self._calendars.clear()
        self._calendar_factories.clear()
        self._aliases.clear()


# We maintain a global calendar dispatcher so that users can just do
# `register_calendar('my_calendar', calendar) and then use `get_calendar`
# without having to thread around a dispatcher.
global_calendar_dispatcher = TradingCalendarDispatcher(
    calendars={},
    calendar_factories=_default_calendar_factories,
    aliases=_default_calendar_aliases,
)

get_calendar = global_calendar_dispatcher.get_calendar
clear_calendars = global_calendar_dispatcher.clear_calendars
deregister_calendar = global_calendar_dispatcher.deregister_calendar
register_calendar = global_calendar_dispatcher.register_calendar
register_calendar_type = global_calendar_dispatcher.register_calendar_type
register_calendar_alias = global_calendar_dispatcher.register_calendar_alias
resolve_alias = global_calendar_dispatcher.resolve_alias
