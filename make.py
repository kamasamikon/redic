#!/usr/bin/env python3

import xmltodict
import sys
import traceback

import pymongo
client = pymongo.MongoClient()

db = client.dyi


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
    data = open(filepath).read()
    dic = xmltodict.parse(data)

    wordbook = dic.get("wordbook")
    for words in wordbook.values():
        for word in words:
            w = word.get("word")
            p = word.get("phonetic") or ""
            t = word.get("trans") or ""
            t = t.replace("\r", "\n").replace("\n", " ").replace("  ", " ").strip()
            addword(w, p, t)

            # output = "{0:>20} | {1:24} | {2}"
            # print(output.format(w,p,t))

import click

@click.command()
@click.option('--drop', default=True, help='Drop old database before update.')
@click.option('--verbose', default=True, help='Show how many words inserted.')
@click.argument('files', nargs=-1, type=str)
def main(files, drop, verbose):
    """Save words from FILES into MongoDB."""

    if drop:
        db.words.drop()

    for f in files:
        try:
            dotan(f)
        except:
            print("ERROR: ", f)
            traceback.print_exc()

    if verbose:
        print(db.words.find().count())

if __name__ == '__main__':
    main()
