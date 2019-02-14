import pandas as pd
from pytz import UTC


def T(x):
    return pd.Timestamp(x, tz=UTC)
