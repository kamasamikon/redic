#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# As a server to get words from website
#

import sys
from bottle import run, request, get, post

import dbquery

from mie.xlogger import klog
klog.to_stdout()


@get("/<word>")
def getword(word):
    q = request.query
    maxlen = int(q.get("m", 40))
    phase = int(q.get("p", 0))
    full = int(q.get("f", 0))
    similar = int(q.get("s", 0))
    winwidth = int(q.get("w", 0))
    pat = word

    klog.d()
    lines = dbquery.search(pat, maxlen, phase, full, similar, winwidth)
    klog.d()
    resp = "\r\n".join(lines).encode() or b"<NOT FOUND>"
    klog.d()
    return resp


@post("/spider/<type>")
def spider(word):
    """Query word"""


def main(argv=None):
    argv = argv if argv else sys.argv
    run(server='paste', host='0.0.0.0', port=12000, debug=True)

if __name__ == "__main__":
    sys.exit(main())

# vim: sw=4 ts=4 sts=4 ai et
