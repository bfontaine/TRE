#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import argparse
from tre import plotting
from tre.saramaki import stats, data

if __name__ == '__main__':
    rootpath = os.path.dirname(__file__) + '/..'
    fname = rootpath + '/docs/saramaki/dataset-01.csv'

    parser = argparse.ArgumentParser(description='draw Saramaki-paper-like graphs')

    parser.add_argument('--dataset', dest='dataset', type=str, default=fname)
    parser.add_argument('--from', dest='from_month', type=int, default=1, help='first month')
    parser.add_argument('--to', dest='to_month', type=int, default=6, help='last month')
    parser.add_argument('--parts', dest='parts', type=int, default=1)
    parser.add_argument('--max-vals', dest='mxvals', type=int, default=20)

    args = parser.parse_args()

    print "Using dataset '%s'." % args.dataset

    sigs = data.csv2social_signatures(args.dataset, args.from_month,
            args.to_month, args.parts, args.mxvals)

    refs = {}

    for ego, s in sigs.items():
        sig = s[0] # first part only
        #print "plotting signature for ego '%s'." % ego
        #plotting.plot_sig(sig,
        #        output='%s/plots/%s-sig.ps' % (rootpath, ego),
        #        title='%s' % ego,
        #        ylabel='fraction')

        refs[ego] = stats.jsd_ref(sig, *[s2[0] for e,s2 in sigs.items() if e!=ego])

    for ego, ref in refs.items():
        plotting.plot_jsd_refs(ref,
                output='%s/plots/%s-refs.ps' % (rootpath, ego),
                title='%s' % ego)
