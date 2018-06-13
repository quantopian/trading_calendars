import numpy as np

NANOSECONDS_PER_MINUTE = 60000000000


def next_divider_idx(dividers, minute_val):

    divider_idx = np.searchsorted(dividers, minute_val, side="right")
    target = dividers[divider_idx]

    if minute_val == target:
        # if dt is exactly on the divider, go to the next value
        return divider_idx + 1
    else:
        return divider_idx


def previous_divider_idx(dividers, minute_val):

    divider_idx = np.searchsorted(dividers, minute_val)

    if divider_idx == 0:
        raise ValueError("Cannot go earlier in calendar!")

    return divider_idx - 1


def is_open(opens, closes, minute_val):

    open_idx = np.searchsorted(opens, minute_val)
    close_idx = np.searchsorted(closes, minute_val)

    if open_idx != close_idx:
        # if the indices are not same, that means the market is open
        return True
    else:
        try:
            # if they are the same, it might be the first minute of a
            # session
            return minute_val == opens[open_idx]
        except IndexError:
            # this can happen if we're outside the schedule's range (like
            # after the last close)
            return False


def compute_all_minutes(opens_in_ns, closes_in_ns):
    """
    Given arrays of opens and closes, both in nanoseconds,
    return an array of each minute between the opens and closes.
    """
    deltas = closes_in_ns - opens_in_ns

    # + 1 because we want 390 mins per standard day, not 389
    daily_sizes = (deltas // NANOSECONDS_PER_MINUTE) + 1
    num_minutes = daily_sizes.sum()

    # One allocation for the entire thing. This assumes that each day
    # represents a contiguous block of minutes.
    all_minutes = np.empty(num_minutes, dtype='int64')
    ix = 0

    for day_ix in range(len(daily_sizes)):
        size = daily_sizes[day_ix]
        minute = opens_in_ns[day_ix]

        all_minutes[ix:ix+size] = np.arange(
            minute,
            minute + (size * NANOSECONDS_PER_MINUTE),
            NANOSECONDS_PER_MINUTE
        )

        ix += size

    return all_minutes.view('datetime64[ns]')
