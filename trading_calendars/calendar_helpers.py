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
        # we are not guaranteed to have a sorted list of breaks, since break
        # may not exist for a given date. Thus we need special logic.

        # if the indices are not same, that means we are within a session
        if (break_starts == NP_NAT).all() and (break_ends == NP_NAT).all():
            # this calendar has no breaks
            return True

        break_start_on_open_dt = break_starts[open_idx - 1]
        break_end_on_open_dt = break_ends[open_idx - 1]
        if break_start_on_open_dt == NP_NAT:
            # There is no break on the relevant day
            return True
        elif break_start_on_open_dt <= minute_val <= break_end_on_open_dt:
            # we're in the middle of a break
            return False
        else:
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

    NOTE: An extra minute is added to ending pbountaries (break_end and close)
    so we include the last bar.
    """
    pieces = []  # todo preallocat?
    for open_time, break_start_time, break_end_time, close_time in zip(
        opens_in_ns, break_starts_in_ns, break_ends_in_ns, closes_in_ns
    ):
        if break_start_time != NP_NAT and break_end_time != NP_NAT:
            pieces.append(
                np.arange(
                    open_time,
                    break_start_time + NANOSECONDS_PER_MINUTE,
                    NANOSECONDS_PER_MINUTE,
                )
            )
            pieces.append(
                np.arange(
                    break_end_time,
                    close_time + NANOSECONDS_PER_MINUTE,
                    NANOSECONDS_PER_MINUTE,
                )
            )
        else:
            pieces.append(
                np.arange(
                    open_time,
                    close_time + NANOSECONDS_PER_MINUTE,
                    NANOSECONDS_PER_MINUTE,
                )
            )
    out = np.concatenate(pieces).view("datetime64[ns]")
    return out
