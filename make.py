#!/usr/bin/env python3

import xmltodict
import sys
import traceback

import pymongo
client = pymongo.MongoClient()

db = client.dyi

wordcount = 0


def addword(w, p, t):
    o = dict(_id=w, p=p, t=t)

    old = db.words.find_one({"_id": w})
    if old:
        oldt = old.get("t", "")
        if oldt != t:
            o["t"] = t + " " + oldt
            db.words.replace_one({"_id": w}, o, True)
    else:
        db.words.insert_one(o)


def dotan(filepath):
    global wordcount

    data = open(filepath).read()
    dic = xmltodict.parse(data)

    wordbook = dic.get("wordbook")
    for words in wordbook.values():
        for word in words:
            w = word.get("word")
            p = word.get("phonetic") or ""
            t = word.get("trans").replace("\r", "\n").replace("\n", " ").replace("  ", " ").strip()

            addword(w, p, t)

            wordcount += 1

            # output = "{0:>20} | {1:24} | {2}"
            # print(output.format(w,p,t))

if __name__ == "__main__":
    print("usage: make db/*.xml")
    for filepath in sys.argv[1:]:
        try:
            dotan(filepath)
        except:
            print("ERROR: ", filepath)
            traceback.print_exc()

    print("wordcount:", wordcount)
