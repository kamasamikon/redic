#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
import jieba

from mie.bprint import varfmt


def main(word):
    '''
    {
        work: "",
        phon: "",
        tran: {
            n: "xxxx",
            v: "xxxx",
            vi: "xxx",
        }
    }
    '''

    dic = {}

    url = "http://youdao.com/w/eng/%s/" % word
    r = requests.get(url)
    content = r.text
    soup = BeautifulSoup(content, "html.parser")

    dic["word"] = soup.find("span", {"class": "keyword"}).text
    dic["phon"] = soup.find("span", {"class": "phonetic"}).text
    dic["tran"] = {}

    trans = soup.find("div", {"class": "trans-container"})
    liList = trans.find_all("li")
    text = " ".join([li.text for li in liList])

    def add(typ, word):
        lis = dic["tran"].get(typ)
        if not lis:
            lis = []
            dic["tran"][typ] = lis
        lis.append(word)

    tList = ("v", "vt", "vi", "n", "int", "pron", "adv", "adj")
    typ = "o"
    seg_list = jieba.cut(text, cut_all=True)
    for x in seg_list:
        if not x:
            continue

        x = x.lower()
        if x in tList:
            typ = x
            continue

        add(typ, x)
    print(varfmt(dic, None, True))


if __name__ == "__main__":
    wList = ("shit", "who", "true", "none", "call")
    for w in wList:
        main(w)

# vim: sw=4 ts=4 sts=4 ai et
