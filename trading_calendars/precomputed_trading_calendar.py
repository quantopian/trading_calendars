from abc import abstractproperty
from pytz import UTC
import numpy as np
import pandas as pd
from .trading_calendar import TradingCalendar


class PrecomputedTradingCalendar(TradingCalendar):
    """
    Used to model an exchange calendar whose holidays are precomputed and
    hardcoded.
    """
    def __init__(self, start=None, end=None):
        earliest_precomputed_year = np.min(self.precomputed_holidays).year
        latest_precomputed_year = np.max(self.precomputed_holidays).year

        if start is None:
            start = pd.Timestamp(
                '{}-01-01'.format(earliest_precomputed_year), tz=UTC
            )

        if end is None:
            end = pd.Timestamp(
                '{}-12-31'.format(latest_precomputed_year), tz=UTC
            )

        super(PrecomputedTradingCalendar, self).__init__(start=start, end=end)

        if earliest_precomputed_year > self.first_trading_session.year:
            raise ValueError(
                'The {} holidays are only recorded back to {},'
                ' cannot instantiate the {} calendar back to {}.'.format(
                    self.name,
                    earliest_precomputed_year,
                    self.name,
                    self.first_trading_session.year
                ),
            )

        if latest_precomputed_year < self.last_trading_session.year:
            raise ValueError(
                'The {} holidays are only recorded to {},'
                ' cannot instantiate the {} calendar for {}.'.format(
                    self.name,
                    latest_precomputed_year,
                    self.name,
                    self.last_trading_session.year
                ),
            )

    @abstractproperty
    def precomputed_holidays(self):
        raise NotImplementedError()

    @property
    def adhoc_holidays(self):
        return self.precomputed_holidays
