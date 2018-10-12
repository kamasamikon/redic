#!/usr/bin/env python3

import re
import os
from Levenshtein import ratio

import pymongo
db = pymongo.MongoClient().dyi

fmtn = '\033[0;3{}m{}\033[0m'.format
pipe = fmtn(2, '|')


def scored(word, maxlen=50, minration=0.7):
    words = db.words.find({}, {"_id": 1})

    d = {}
    for w in words:
        w = w["_id"]
        if w == word or w.find(" ") >= 0:
            continue
        r = ratio(word, w)
        if r >= minration:
            d[w] = r

    words = sorted(d.items(), key=lambda x: -x[1])[:maxlen]
    return [w[0] for w in words]


def word_get(pat, maxlen, phase, full, similar, winwidth=0):
    '''Search words according to given re pattern.'''

    print("PAT::::: ", pat)

    lines = []

    if similar:
        words = scored(pat)
        pat = "|".join(["\\b" + w + "\\b" for w in words])

    try:
        if winwidth <= 0:
            columns = os.get_terminal_size().columns
        else:
            columns = winwidth
    except:
        full = True

    if full:
        maxlen = 10000
    else:
        maxlen = 10000 if maxlen < 1 else maxlen

    regx = re.compile(pat, re.IGNORECASE)
    ascii = re.compile(u'[\x00-\x7F]+', re.IGNORECASE)

    if ascii.match(pat):
        items = list(db.words.find({"_id": regx}))
    else:
        items = list(db.words.find({"t": regx}))

    wwide, pwide = 0, 0

    for i in items:
        w = i.get("_id")
        if not phase:
            ww = w.replace('-', ' ').replace('.', ' ')
            if len(ww.split()) > 1:
                continue

        p = i.get("p") or " "

        if wwide < len(w):
            wwide = len(w)
        if pwide < len(p):
            pwide = len(p)

    if not full:
        maxlen = columns - wwide - pwide - 8
        maxlen = int(maxlen / 2)

    for i in items:
        w = i.get("_id")
        p = i.get("p") or " "
        t = i.get("t") or " "

        if full:
            count = 100000
        else:
            left = columns - wwide - pwide - 8

            count = 0
            for i in t:
                left -= 2 if ord(i) > 127 else 1
                if left <= 0:
                    break
                count += 1

        if not phase:
            ww = w.replace('-', ' ').replace('.', ' ')
            if len(ww.split()) > 1:
                continue

        t = t[:count]

        ofmt = " {0:>{wwide}} %s {1:<{pwide}} %s {2}" % (pipe, pipe)
        ostr = ofmt.format(w, p, t, wwide=wwide, pwide=pwide)

        lines.append(re.sub(r"(%s)" % pat, r"\033[0;31m\1\033[0m", ostr))

    return lines


def word_add(w, p, t):
    o = dict(_id=w, p=p, t=t)

    old = db.words.find_one({"_id": w})
    if old:
        oldt = old.get("t", "")
        if oldt != t:
            o["t"] = t + " " + oldt
            db.words.replace_one({"_id": w}, o, True)
    else:
        db.words.insert_one(o)

# vim: sw=4 ts=4 sts=4 ai et
