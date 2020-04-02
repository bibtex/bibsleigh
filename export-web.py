#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import cProfile
import os.path, glob
from fancy.ANSI import C
from fancy.Templates import aboutHTML, syncHTML
from lib.AST import Sleigh
from lib.JSON import parseJSON
from lib.LP import lastSlash

ienputdir = '../json'
corpusdir = ienputdir + '/corpus'
outputdir = '../frontend'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(corpusdir, name2file)


def next_year(vvv):
    return int(lastSlash(sorted(glob.glob(vvv + '/*'))[-2])) + 1


def main():
    print('{}: {} venues, {} papers\n{}'.format(
        C.purple('BibSLEIGH'),
        C.red(len(sleigh.venues)),
        C.red(sleigh.numOfPapers()),
        C.purple('=' * 42)))
    # generate the index
    f = open(outputdir + '/index.html', 'w', encoding='utf-8')
    f.write(sleigh.getPage())
    f.close()
    # generate all individual pages
    # if False:
    for v in sleigh.venues:
        r = C.blue(v.getKey())
        f = open(outputdir + '/' + v.getKey() + '.html', 'w', encoding='utf-8')
        f.write(v.getPage())
        f.close()
        if v.brands:
            r += '{' + '+'.join([C.blue(b.getKey()) for b in v.brands]) + '}'
            for b in v.brands:
                f = open(outputdir + '/' + b.getKey() + '.brand.html', 'w', encoding='utf-8')
                f.write(b.getPage())
                f.close()
        r += ' => '
        for c in v.getConfs():
            f = open(outputdir + '/' + c.getKey() + '.html', 'w', encoding='utf-8')
            f.write(c.getPage())
            f.close()
            for p in c.papers:
                f = open(outputdir + '/' + p.getKey() + '.html', 'w', encoding='utf-8')
                f.write(p.getPage())
                f.close()
            purekey = c.getKey().replace(v.getKey(), '').replace('-', ' ').strip()
            r += '{} [{}], '.format(purekey, C.yellow(len(c.papers)))
        print(r)
    # generate the icon lineup
    icons = []
    linked = []
    pngs = [lastSlash(png).split('.')[0] for png in glob.glob(outputdir + '/stuff/*.png')]
    pngs = [png for png in pngs \
            if not (png.startswith('a-') or png.startswith('p-') or png.startswith('ico-')
                    or png in ('cc-by', 'xhtml', 'css', 'open-knowledge', 'edit'))]
    for brand in glob.glob(outputdir + '/*.brand.html'):
        pure = lastSlash(brand).split('.')[0]
        img = pure.lower().replace(' ', '')
        if img in pngs:
            pic = '<div class="wider"><a href="{0}.brand.html"><img class="abc" src="{1}" alt="{0}"/></a><span>{0}</span></div>'.format( \
                pure,
                'stuff/' + img + '.png')
            pngs.remove(img)
            icons.append(pic)
        else:
            # print('No image for', pure)
            pass
    corner = {'ada': 'TRI-Ada', 'comparch': 'CompArch', 'floc': 'FLoC', 'bibsleigh': 'index'}
    for pure in pngs:
        venueCandidate = corner[pure] if pure in corner else pure.upper()
        canlink = sorted(glob.glob(outputdir + '/' + venueCandidate + '*.html'), key=len)
        if canlink:
            pic = '<div class="wider"><a href="{0}"><img class="abc" src="stuff/{1}.png" alt="{2}"/></a><span>{2}</span></div>'.format( \
                canlink[0].split('/')[-1],
                pure,
                venueCandidate,
                canlink[0].split('/')[0])
        elif pure == 'twitter':
            pic = '<div class="wider"><a href="https://about.twitter.com/company/brand-assets"><img class="abc" src="stuff/twitter.png" alt="Twitter"/></a><span>Twitter</span></div>'
        elif pure == 'email':
            pic = '<div class="wider"><a href="mailto:vadim@grammarware.net"><img class="abc" src="stuff/email.png" alt="e-mail"/></a><span>email</span></div>'
        else:
            print('Lonely', pure)
            pic = '<img class="abc" src="stuff/{0}.png" alt="{0}"/>'.format(pure)
        icons.append(pic)
    # find last year of each venue
    # for ven in glob.glob(corpusdir + '/*'):
    # 	venname = lastSlash(ven)
    # 	newstuff += '<strong><a href="http://dblp.uni-trier.de/db/conf/{}/">{} {}</a></strong>, '.format(venname.lower(), venname, nextYear(ven))
    # print(lastSlash(ven), ':', lastYear(ven))
    # write "more info" file
    f = open(outputdir + '/about.html', 'w', encoding='utf-8')
    f.write(aboutHTML.format(
        len(icons),
        '<div class="minibar">' + '\n'.join(sorted(icons)) + '</div>'
    ))
    f.close()

    # generate the DBLP sync page
    cell_by_conf_by_year = {}
    Ys = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009]
    dblplinks = {}

    with open(ienputdir + '/meta/dblpguide.sync', 'r') as f:
        for line in f:
            if not line or line.startswith('#'):
                continue
            words = line.split('|')
            if len(words) != 3:
                print('- Metaline {} skipped!'.format(words))
                continue
            name = words[0].strip()
            dome = words[1].strip()
            dblp = words[2].strip()
            cell_by_conf_by_year[name] = {}
            dblplinks[name] = dblp
            for y in Ys:
                cell_by_conf_by_year[name][y] = '(no)'
            v = sleigh.getVenue(dome)
            if v:
                for yy in Ys:
                    y = v.getYear(yy)
                    if y:
                        ckey = '{}-{}'.format(name, yy)
                        c = y.getConf(ckey)
                        if c:
                            cell_by_conf_by_year[name][yy] = c.getIconItem2('', '')
                        else:
                            # print('- Conference {} of year {} in venue {} not found in the corpus'.format(ckey, yy, name))
                            for alt in 'v1', 'p1', 'c1', '1', 'J':
                                ckey = '{}-{}-{}'.format(name, alt, yy)
                                c = y.getConf(ckey)
                                if c:
                                    cell_by_conf_by_year[name][yy] = c.getIconItem2('', '')
                                    break
                # else:
                # 	print('- Year {} in venue {} not found in the corpus among {}'.format(yy, name, [z.year for z in v.years]))
        # else:
        # 	print('- Venue {} not found in the corpus'.format(name))

    table = '<table>'
    table += '<tr><td></td>'
    for y in Ys:
        table += '<th>{}</th>\n'.format(y)
    table += '</tr>'
    # print (cell_by_conf_by_year)
    for name in sorted(cell_by_conf_by_year.keys()):
        table += '<tr><th><a href="{}.brand.html">[@]</a> <a href="{}">{}</a></th>'.format(name, dblplinks[name], name)
        for y in Ys:
            table += '<td>{}</td>\n'.format(cell_by_conf_by_year[name][y])
        table += '</tr>'
    table += '</table>'

    with open(outputdir + '/sync.html', 'w', encoding='utf-8') as f:
        f.write(syncHTML.format(table))

    print('{}\nDone with {} venues, {} papers.'.format(
        C.purple('=' * 42),
        C.red(len(sleigh.venues)),
        C.red(sleigh.numOfPapers())))


if __name__ == "__main__":
    main()
# cProfile.run('main()')
