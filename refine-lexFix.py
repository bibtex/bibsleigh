#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for lexical cleanup: turns even badly damaged JSONs into LRJs

import sys
import os.path

from lib.AST import Sleigh
from lib.NLP import strictstrip
from lib.JSON import parseJSON
from fancy.ANSI import C


ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False


def checkon(fn, o):
    if not os.path.exists(fn) or os.path.isdir(fn):
        fn = fn + '.json'
    f = open(fn, 'r')
    flines = f.readlines()[1:-1]
    f.close()
    sflines = [strictstrip(s) for s in flines]
    sjlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
    jlines = ['\t{},\n'.format(s) for s in sjlines]
    jlines[-1] = jlines[-1][:-2] + '\n'  # remove the last comma
    if sflines != sjlines:
        return 1
    elif jlines != flines:
        # f1 = [s for s in jlines if s not in flines]
        # f2 = [s for s in flines if s not in jlines]
        # print('∆:', f1, '\nvs', f2)
        f = open(fn, 'w')
        f.write('{\n')
        for line in jlines:
            f.write(line)
        f.write('}')
        f.close()
        return 2
    else:
        return 0


def checkreport(fn, o):
    statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
    r = checkon(fn, o)
    # non-verbose mode by default
    if verbose or r != 0:
        print('[ {} ] {}'.format(statuses[r], fn))
    return r


if __name__ == "__main__":
    if len(sys.argv) > 1:
        verbose = sys.argv[1] == '-v'
    print('{}: {} venues, {} papers\n{}'.format( \
        C.purple('BibSLEIGH'),
        C.red(len(sleigh.venues)),
        C.red(sleigh.numOfPapers()),
        C.purple('=' * 42)))
    cx = {0: 0, 1: 0, 2: 0}
    for v in sleigh.venues:
        for c in v.getConfs():
            cx[checkreport(c.filename, c)] += 1
            for p in c.papers:
                cx[checkreport(p.filename, p)] += 1
    print('{} files checked, {} ok, {} fixed, {} failed'.format( \
        C.bold(cx[0] + cx[1] + cx[2]),
        C.blue(cx[0]),
        C.yellow(cx[2]),
        C.red(cx[1])))
