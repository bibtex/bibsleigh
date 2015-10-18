#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for matching authors/editors with people entries

import sys
import glob
import os.path

from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify
from lib.LP import listify


ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False


def report(s, r):
    statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
    # non-verbose mode by default
    if verbose or r != 0:
        print('[ {} ] {}'.format(statuses[r], s))
    return r


if __name__ == "__main__":
    verbose = sys.argv[-1] == '-v'
    # All known contributors
    cx = {0: 0, 1: 0, 2: 0}
    people = {}
    for fn in glob.glob(ienputdir + '/people/*.json'):
        p = parseJSON(fn)
        if p['name'] in people.keys():
            cx[report(C.red('duplicate') + ' ' + C.yellow(p), 1)] += 1
            continue
        people[p['name']] = p
    print('{}: {} venues, {} papers written by {} people\n{}'.format( \
        C.purple('BibSLEIGH'),
        C.red(len(sleigh.venues)),
        C.red(sleigh.numOfPapers()),
        C.red(len(people)),
        C.purple('=' * 42)))
    # traverse ALL the papers!
    for v in sleigh.venues:
        for c in v.getConfs():
            for p in c.papers:
                if 'author' in p.json.keys():
                    for a in listify(p.json['author']):
                        if a in people.keys():
                            if 'authored' not in people[a].keys():
                                people[a]['authored'] = []
                            if p.getKey() not in people[a]['authored']:
                                people[a]['authored'].append(p.getKey())
                        else:
                            report(C.yellow('Author not found: ') + a, 0)
            if 'editor' in c.json.keys():
                for e in listify(c.json['editor']):
                    if e in people.keys():
                        if 'edited' not in people[e].keys():
                            people[e]['edited'] = []
                        if c.getKey() not in people[e]['edited']:
                            people[e]['edited'].append(c.getKey())
                    else:
                        report(C.yellow('Editor not found: ') + e, 0)
            if 'roles' in c.json.keys():
                for name, role in listify(c.json['roles']):
                    if name in people.keys():
                        if 'roles' in people[name].keys():
                            if [c.getKey(), role] not in people[name]['roles']:
                                # new information
                                people[name]['roles'].append([c.getKey(), role])
                        else:
                            # first role ever
                            people[name]['roles'] = [[c.getKey(), role]]
                    else:
                        # unknown person?
                        print('[{}] Unacquainted with {} ({} of {})'.format(C.red('PERS'), name, role, c.getKey()))

    # now unfold
    for p in people.keys():
        if 'edited' in people[p].keys():
            if 'roles' not in people[p].keys():
                people[p]['roles'] = []
            for e in people[p]['edited']:
                if [e, "Editor"] not in people[p]['roles']:
                    people[p]['roles'].append([e, "Editor"])
            del people[p]['edited']
    # have to read again to see who’s changed
    for fn in glob.glob(ienputdir + '/people/*.json'):
        p = parseJSON(fn)
        if p == people[p['name']]:
            cx[report(p['name'], 0)] += 1
        else:
            cx[report(p['name'], 2)] += 1
            f = open(fn, 'w')
            del people[p['name']]['FILE']
            f.write(jsonify(people[p['name']]))
            f.close()
    print('{} files checked, {} ok, {} fixed, {} failed'.format( \
        C.bold(cx[0] + cx[1] + cx[2]),
        C.blue(cx[0]),
        C.yellow(cx[2]),
        C.red(cx[1])))
