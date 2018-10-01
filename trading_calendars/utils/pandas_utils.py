import pandas as pd


def days_at_time(days, t, tz, day_offset=0):
    """
    Create an index of days at time ``t``, interpreted in timezone ``tz``.

    The returned index is localized to UTC.

    Parameters
    ----------
    days : DatetimeIndex
        An index of dates (represented as midnight).
    t : datetime.time
        The time to apply as an offset to each day in ``days``.
    tz : pytz.timezone
        The timezone to use to interpret ``t``.
    day_offset : int
        The number of days we want to offset @days by

    Examples
    --------
    In the example below, the times switch from 13:45 to 12:45 UTC because
    March 13th is the daylight savings transition for US/Eastern.  All the
    times are still 8:45 when interpreted in US/Eastern.

    >>> import pandas as pd; import datetime; import pprint
    >>> dts = pd.date_range('2016-03-12', '2016-03-14')
    >>> dts_at_845 = days_at_time(dts, datetime.time(8, 45), 'US/Eastern')
    >>> pprint.pprint([str(dt) for dt in dts_at_845])
    ['2016-03-12 13:45:00+00:00',
     '2016-03-13 12:45:00+00:00',
     '2016-03-14 12:45:00+00:00']
    """
    days = pd.DatetimeIndex(days).tz_localize(None)
    if len(days) == 0:
        return days.tz_localize('UTC')

    # Offset days without tz to avoid timezone issues.
    delta = pd.Timedelta(
        days=day_offset,
        hours=t.hour,
        minutes=t.minute,
        seconds=t.second,
    )
    return (days + delta).tz_localize(tz).tz_convert('UTC')


def series_from_records(records):
    """Construct a Series from a list of tuples.

    Parameters
    ----------
    records : list[tuple]
        A list of tuples, with the first element in each tuple
        corresponding to a Series index, and the second element in each
        corresponding to Series values.

    Returns
    -------
    pd.Series
    """
    df = pd.DataFrame.from_records(records, index=[0])

    if df.empty:
        return pd.Series()

    return df[1]
