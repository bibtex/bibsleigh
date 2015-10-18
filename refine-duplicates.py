#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for finding duplicates in people

import sys
import glob
import os.path

from fancy.ANSI import C
from fancy.Latin import simpleLatin, nodiaLatin
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify
from lib.LP import listify


ienputdir = '../json'
verbose = False
cx = {0: 0, 1: 0, 2: 0}


def report(s, r):
    statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
    # non-verbose mode by default
    if verbose or r != 0:
        print('[ {} ] {}'.format(statuses[r], s))
    return r


if __name__ == "__main__":
    verbose = sys.argv[-1] == '-v'
    # Load all contributors
    people = {}
    for fn in glob.glob(ienputdir + '/people/*.json'):
        p = parseJSON(fn)
        people[p['name']] = p
    print('{}: {} people\n{}'.format( \
        C.purple('BibSLEIGH'),
        C.red(len(people)),
        C.purple('=' * 42)))
    # check for duplicates
    bysurname = {}
    for name in people.keys():
        byword = name.split(' ')
        j = -1
        while -j < len(byword) and (
            byword[j - 1][0].islower() or byword[j - 1].lower() in ('de', 'di', 'du', 'van', 'von', 'le' 'la')):
            j -= 1
        surname = ' '.join(byword[j:])
        firstnames = ' '.join(byword[:j])
        if verbose:
            print('Thinking “{}” is “{}” + “{}”'.format(name, firstnames, surname))
        if not firstnames:
            report('suspicious that “{}” has no first names'.format(name), 1)
            continue
        if not surname:
            report('suspicious that “{}” has no surname'.format(name), 1)
            continue
        if surname not in bysurname.keys():
            bysurname[surname] = {}
        bysurname[surname][firstnames] = people[name]
    # check per surname
    for surname in bysurname.keys():
        if len(bysurname[surname]) == 1:
            continue
        variants = sorted(bysurname[surname].keys())
        if len(bysurname[surname]) > 2:
            # TODO
            continue
        if variants[0].isdigit():
            # TODO
            continue
        # Heuristic 1: more names
        # if len(variants[0]) > len(variants[1]):
        # 	longer = variants[0]
        # 	shoter = variants[1]
        # else:
        # 	longer = variants[1]
        # 	shoter = variants[0]
        # if ' ' not in shoter and shoter in longer.split(' '):
        # 	report('{}: “{}” == “{}”?'.format(surname, longer, shoter), 2)
        # Heuristic 2: no diacritics
        if nodiaLatin(variants[0]) == nodiaLatin(variants[1]):
            report('{}: “{}” == “{}”?'.format(surname, variants[0], variants[1]), 2)
        # Heuristic 3: dealt with diacritics
        if simpleLatin(variants[0]) == simpleLatin(variants[1]):
            report('{}: “{}” == “{}”?'.format(surname, variants[0], variants[1]), 2)
        # print
        pvariants = ['“{}”'.format(v) for v in variants]
        report('{}: {}'.format(surname, ' vs '.join(pvariants)), 0)
    # write back if changed
    for k in people.keys():
        p = people[k]
        if p['FILE']:
            if os.path.exists(p['FILE']):
                cur = parseJSON(p['FILE'])
                if cur == p:
                    cx[0] += 1
                    if verbose:
                        print('[', C.green('FIXD'), ']', p['name'])
                    continue
            print('[', C.yellow('FIXD'), ']', p['name'])
            cx[2] += 1
            f = open(p['FILE'], 'w')
            del p['FILE']
            f.write(jsonify(p))
            f.close()
        else:
            print('How can that be?')
    print('{} people checked, {} ok, {} fixed, {} failed'.format( \
        C.bold(cx[0] + cx[1] + cx[2]),
        C.blue(cx[0]),
        C.yellow(cx[2]),
        C.red(cx[1])))
