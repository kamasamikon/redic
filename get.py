#!/usr/bin/env python3

import re
import click

import pymongo
db = pymongo.MongoClient().dyi


@click.command()
@click.option('--maxlen', default=2000, help='Max length of trans part.')
@click.option('--phase', '-p', default=False, is_flag=True, help='Show phase.')
@click.argument('pat', type=str)
def search(pat, maxlen, phase):
    '''Search words according to given re pattern.'''

    regx = re.compile(pat, re.IGNORECASE)
    items = list(db.words.find({"_id": regx}))

    wwide = max(len(i.get("_id") or " ") for i in items)
    pwide = max(len(i.get("p") or " ") for i in items)

    for i in items:
        w = i.get("_id")
        p = i.get("p") or " "
        t = i.get("t") or " "

        if not phase and len(w.split()) > 1:
            continue

        t = t[:maxlen]

        pat = "{0:>{wwide}} | {1:<{pwide}} | {2}"
        print(pat.format(w, p, t, wwide=wwide, pwide=pwide))

if __name__ == "__main__":
    search()
