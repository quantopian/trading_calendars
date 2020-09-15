import numpy as np
import pandas as pd

NANOSECONDS_PER_MINUTE = int(6e10)
# TODO this is a negative number - can we just check that?
NP_NAT = np.array([pd.NaT], dtype=np.int64)[0]


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


def is_open(opens, break_starts, break_ends, closes, minute_val):

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


def compute_all_minutes(
    opens_in_ns, break_starts_in_ns, break_ends_in_ns, closes_in_ns,
):
    """
    Given arrays of opens and closes (in nanoseconds) and optionally
    break_starts and break ends, return an array of each minute between the
    opens and closes.
    """
    pieces = []  # todo preallocat?
    for open_time, break_start_time, break_end_time, close_time in zip(
        opens_in_ns, break_starts_in_ns, break_ends_in_ns, closes_in_ns
    ):
        if break_start_time != NP_NAT and break_end_time != NP_NAT:
            pieces.append(
                np.arange(open_time, break_start_time, NANOSECONDS_PER_MINUTE)
            )
            # We add an extra minute so we include the ending minute
            pieces.append(
                np.arange(
                    break_end_time,
                    close_time + NANOSECONDS_PER_MINUTE,
                    NANOSECONDS_PER_MINUTE,
                )
            )
        else:
            # We add an extra minute so we include the ending minute
            pieces.append(
                np.arange(
                    open_time,
                    close_time + NANOSECONDS_PER_MINUTE,
                    NANOSECONDS_PER_MINUTE,
                )
            )
    out = np.concatenate(pieces).view("datetime64[ns]")
    return out
