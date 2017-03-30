#!/usr/bin/env python3

import sys
import re

import pymongo
db = pymongo.MongoClient().dyi


if __name__ == "__main__":
    pat = sys.argv[1]
    maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    regx = re.compile(pat, re.IGNORECASE)
    items = list(db.words.find({"_id": regx}))

    wwide = max(len(i.get("_id") or " ") for i in items)
    pwide = max(len(i.get("p") or " ") for i in items)

    for i in items:
        w = i.get("_id")
        p = i.get("p") or " "
        t = i.get("t") or " "

        t = t[:maxlen]

        pat = "{0:>{wwide}} | {1:<{pwide}} | {2}"
        print(pat.format(w, p, t, wwide=wwide, pwide=pwide))
