import numpy as np
import pandas as pd

NANOSECONDS_PER_MINUTE = int(6e10)

NP_NAT = np.array([pd.NaT])[0]


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


def compute_all_minutes(
    opens_in_ns, break_starts_in_ns, break_ends_in_ns, closes_in_ns,
):
    """
    Given arrays of opens and closes (in nanoseconds) and optionally
    break_starts and break ends, return an array of each minute between the
    opens and closes.

    NOTE: Add an extra minute to ending boundaries (break_start and close)
    so we include the last bar (arange doesn't include its stop).
    """
    pieces = []
    for open_time, break_start_time, break_end_time, close_time in zip(
        opens_in_ns, break_starts_in_ns, break_ends_in_ns, closes_in_ns
    ):
        if break_start_time != NP_NAT:
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
