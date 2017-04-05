#!/usr/bin/env python3

import re
import click

import pymongo
db = pymongo.MongoClient().dyi

fmtn = '\033[0;3{}m{}\033[0m'.format
pipe = fmtn(1, '|')


@click.command()
@click.option('--maxlen', '-m', default=40, help='Max length of trans part.')
@click.option('--phase', '-p', default=False, is_flag=True, help='Show phase.')
@click.option('--full', '-f', default=False, is_flag=True, help='Full output.')
@click.argument('pat', type=str)
def search(pat, maxlen, phase, full):
    '''Search words according to given re pattern.'''

    if full:
        maxlen = 10000
    else:
        maxlen = 10000 if maxlen < 1 else maxlen

    regx = re.compile(pat, re.IGNORECASE)
    items = list(db.words.find({"_id": regx}))

    wwide, pwide = 0, 0

    for i in items:
        w = i.get("_id")
        p = i.get("p") or " "

        if not phase and len(w.split()) > 1:
            continue

        if wwide < len(w):
            wwide = len(w)
        if pwide < len(p):
            pwide = len(p)

    for i in items:
        w = i.get("_id")
        p = i.get("p") or " "
        t = i.get("t") or " "

        if not phase:
            ww = w.replace('-', ' ')
            if len(ww.split()) > 1:
                continue

        t = t[:maxlen]

        pat = " {0:>{wwide}} %s {1:<{pwide}} %s {2}" % (pipe, pipe)
        print(pat.format(w, p, t, wwide=wwide, pwide=pwide))

if __name__ == "__main__":
    try:
        search()
    except:
        pass
