# -*- coding: UTF-8 -*-

import re
import Gnuplot, Gnuplot.funcutils
from Gnuplot.PlotItems import _FIFOFileItem
Gnuplot.GnuplotOpts.default_term = 'x11'

import patterns

class FileListItem(_FIFOFileItem):
    def __init__(self, data, **kws):
        _FIFOFileItem.__init__(self, "\n".join(map(str, data)), **kws)

__string_opts = ['title', 'output', 'xlabel', 'ylabel']

def __set_gnuplot_options(g, **kws):
    """
    Set some Gnuplot options from a dict
    """
    for k,v in kws.items():
        if k in __string_opts:
            v = '"%s"' % v
        g("set %s %s" % (k, v))

def mk_gnuplot(opts={}, instance=None, reset=True):
    """
    return a Gnuplot instance
    """
    g = Gnuplot.Gnuplot() if instance is None else instance
    if reset:
        g('reset')
    __set_gnuplot_options(g, **opts)
    return g

def plot_sig(sig, max_plots=20, **kws):
    """
    plot a social signature in a postscript file.
    """
    sig = list(enumerate(sig))
    opts = {
        'terminal': 'postscript',
        'style':    'data linespoints',
        'logscale': 'y',
        'yrange':   '[0.001:1]'
    }
    opts.update(kws)
    g = mk_gnuplot(opts)
    g.plot(sig[:max_plots])

def plot_jsd_refs(refs, bars_count=10, **kws):
    """
    plot a set of JSD refs as in graph B in Saramaki's paper.
    """
    min_val, max_val = min(refs), max(refs)
    width = (max_val-min_val)/float(bars_count) # bar width
    half = width/2.0
    bars = [[k*width+(min_val + half), 0] for k in xrange(0, bars_count)]

    for v in refs:
        bars[int((v - min_val)/width)-1][1] += 1

    # FIXME: we need to have the same ymax value accross all histograms to do
    # it like in Saramaki's paper
    ymax = max(map(lambda e: e[1], bars))

    data = map(lambda e: "\t".join(map(str, e)), bars)
    opts = {
        'terminal': 'postscript',
        'style':    'data histograms',
        'yrange':   '[0:%d]' % ymax,
        'xrange':   '[0.0:0.3]',
        'xlabel':   'distance d',
        'ylabel':   'P(d)',
        'xtics':    '0.1',
       #'boxwidth': width*0.9,
    }
    opts.update(kws)
    g = mk_gnuplot(opts)
    g('unset ytics')
    g('width=%d' % width)
    g.plot(FileListItem(data, using='1:2', with_='boxes'))

def plot_count_histograms(datafiles, outputfile, w=8, h=20, truncate=48,
        colors=False, titles=True,
        minactivity=30, pw='42cm', ph='59.4cm', **kw):
    """
    Example:

        >>> from glob import glob
        >>> from src.tre import plotting
        >>> datafiles = glob('histograms/pubcounts/*.dat')
        >>> plotting.plot_count_histograms(datafiles, 'foo.ps')
    """
    minpub = kw.get('minpub', truncate)

    for s in ('minpub',):
        if s in kw:
            del kw[s]

    col = 'color' if colors else ''

    opts = {
        'terminal': 'postscript eps enhanced %s size %s,%s' % (col, pw, ph),
       #'style': 'data histograms',
       #'xlabel': 'mois',
        'output': outputfile,
        'xrange': '[0:%d]' % truncate,
        'xtics': '12',
        'ytics': 'format " "',
    }
    opts.update(kw)

    g = mk_gnuplot(opts)

    g('set style fill solid 1.00 border 0')
    g('set style histogram')
    g('set style data histogram')

    g('set multiplot layout %d,%d' % (h, w))

    skipped = 0
    drawn = 0
    n = w*h + w

    for i, datafile in enumerate(datafiles):

        with open(datafile, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0 and lines[0].startswith('#'):
                lines.pop(0)
            data = list(map(lambda s: int(re.split(r'\s+', s)[1]), lines))

        ldata = len(data)
        mx = float(max(data)) if ldata > 0 else 0
        #data = list(map(lambda e: e*100/mx, data))


        eid = datafile.split('/')[-1].split('.')[0]
        e = eid[:8]

        if ldata < minpub:
            skipped += 1
            #print 'skipping %s, less than a few years of activity' % e
            continue

        if mx < minactivity:
            skipped += 1
            #print 'skipping %s, not enough activity' % e
            continue

        green = '#99D594'
        red = '#FC8D59'

        color = green if patterns.late_to_the_party(data, mx, e) else red

        data = data[:truncate]

        if titles:
            g('set title "%s - max=%d"' % (e, int(mx)))
        with_ = 'boxes'
        if colors:
            with_ += ' linecolor rgb "%s"' % color
        source = FileListItem(data, using='1', with_=with_)
        g.plot(source)
        drawn += 1

        if drawn > n:
            break

        #if drawn%n == 0:
        #    g('set multiplot layout %d,%d' % (h, w))

    print 'Skipped %d egos' % skipped
