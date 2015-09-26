# -*- coding: UTF-8 -*-

from vendor.entropy import jensen_shannon_divergence as _jsd
import numpy as np

def jsd(*sigs):
    """
    compute the JSD between two (or more) signatures
    """
    sigs = list(sigs)
    lens = map(len, sigs)
    lmin = min(lens)
    for i,s in enumerate(sigs):
        if lens[i] > lmin:
            print 'warning: truncating signature to %s elements' % lmin
            sigs[i] = s[:lmin]

    return _jsd(np.array(sigs))[0]

def jsd_ref(sig1, *sigs):
    """
    compute a list of JSD between the first signature and each of the following
    ones.
    """
    return map(lambda s: jsd(sig1, s), sigs)

def jsd_self(*sigs):
    """
    compute a list of JSD for an intervals list from a signatures list. For
    example `jsd_self(s1, s2, s3)` will return `[jsd(s1, s2), jsd(s2, s3)]`
    """
    return [jsd(sigs[i], sigs[i+1]) for i in range(len(sigs)-1)]

def jaccard_coeff(set1, set2):
    """
    Compute the Jaccard coefficient for two sets.
    """
    set1 = set(set1)
    set2 = set(set2)

    return len(set1.intersection(set2))/float(len(set1.union(set2)))
