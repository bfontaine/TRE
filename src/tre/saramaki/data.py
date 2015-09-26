# -*- coding: UTF-8 -*-

import csv
import utils

def csv2social_signatures(fname, from_month=1, to_month=6, parts=1,
        max_values=20):
    """
    load social signatures from a CSV dataset
        fname:      path to the CSV file
        from_month: first month to include in the output, starting at 1.
                    Default is 1.
        to_month:   last month to include in the output, starting at 1. Default
                    is 6.
        parts:      how many different parts should the signatures be split
                    into. Default is 1, which means we're getting one
                    signature per ego. With parts=2, each ego would get two
                    social signature, one for the first half of time and
                    another for the second half (for 6 months, that gives us
                    one signature for the first 3 and another for the last 3).
                    `parts` cannot be higher than the number of months, and
                    `to_month-from_month` should be divisible by `parts`.
        max_values: maximum number of values to include in each signature.
                    Default is 20. All signatures should have the same length
                    to compute JSDs between them.
    """
    if to_month < from_month:
        raise Exception("to_month cannot be less than from_month (%d < %d)"
                % (to_month, from_month))

    if parts > to_month - from_month + 1:
        raise Exception("too many parts (%d) for %d months."
                % (parts, to_month - from_month + 1))

    months = range(from_month, to_month+1)
    calls = {}

    if parts < 1: parts = 1

    parts_indexes = utils.mk_chunk_indexes(months, parts)

    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None) # skip header
        for row in reader:
            ego, alter, month, n_calls, duration = map(lambda s: s.strip(), row)
            imonth = int(month)
            if imonth not in months:
                continue
            calls.setdefault(ego, [{} for _ in range(parts)])
            p = parts_indexes[imonth]
            calls[ego][p].setdefault(alter, 0)
            calls[ego][p][alter] += round(float(n_calls))

    for ego, parts in calls.items():
        for i, part in enumerate(parts):
            v = part.values()
            total_calls = sum(v)
            ss = [x/total_calls for x in v]
            ss.sort(reverse=True)
            ss = ss[:max_values]
            calls[ego][i] = ss

    return calls
