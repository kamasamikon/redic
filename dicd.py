#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# As a server to get words from website
#

import sys
from bottle import run, request, get, post

import dbquery

from mie.bottlemisc import body
from mie.xlogger.klog import klog
klog.to_stdout()


@post("/<word>")
def word_add(word):
    calldic = body()
    usr = calldic.get("user")



@get("/<word>")
def word_get(word):
    q = request.query
    maxlen = int(q.get("m", 40))
    phase = int(q.get("p", 0))
    full = int(q.get("f", 0))
    similar = int(q.get("s", 0))
    winwidth = int(q.get("w", 0))
    pat = word

    lines = dbquery.word_get(pat, maxlen, phase, full, similar, winwidth)
    resp = "\r\n".join(lines).encode() or "<NOT FOUND>"
    return resp


@get("/spider/<spider>/start")
def spider_start(spider):
    return "Start it"


@get("/spider/<spider>/stop")
def spider_stop(spider):
    return "Stop it"


@get("/spider/<spider>/status")
def spider_status(spider):
    return "Status it"


def main(argv=None):
    argv = argv if argv else sys.argv
    run(server='paste', host='0.0.0.0', port=12000, debug=True)

if __name__ == "__main__":
    sys.exit(main())

# vim: sw=4 ts=4 sts=4 ai et
