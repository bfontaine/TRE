# -*- coding: UTF-8 -*-

def _ensure_ints(lst):
    return map(int, lst)


def late_to_the_party(pubs, mx=0, eid=None, threshold=0.05, minipubs=5):
    """
    Réveil tardif
    """

    # at least one year below the threshold, then over it

    activity_start = 0

    prev = 0
    for i, p in enumerate(pubs):
        if p > prev*1.5 and p > minipubs:
            activity_start = i
            break

        prev = p

    if activity_start < 12:
        return False

    before, after = sum(pubs[:activity_start]), sum(pubs[activity_start:])

    v = before / float(before + after)

    return v < threshold
