#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click

from mie.xlogger import klog
klog.to_stdout()


@click.command()
@click.option('--maxlen', '-m', default=40, help='Max length of trans part.')
@click.option('--phase', '-p', default=False, is_flag=True, help='Show phase.')
@click.option('--full', '-f', default=False, is_flag=True, help='Full output.')
@click.option('--similar', '-s', default=False, is_flag=True, help='Find similar.')
@click.option('--local', '-l', default=False, is_flag=True, help='Find local DB.')
@click.argument('pat', type=str)
def search(pat, maxlen, phase, full, similar, local):
    '''Search words according to given re pattern.'''

    try:
        winwidth = os.get_terminal_size().columns
    except:
        winwidth = 0

    if local:
        klog.d()
        import dbquery
        klog.d()
        lines = dbquery.search(pat, maxlen, phase, full, similar, winwidth)
        klog.d()
        print("\r\n".join(lines))
        klog.d()
    else:
        klog.d()
        import requests
        import urllib.parse as urllib_parse
        klog.d()

        url = "http://localhost:12000/"
        url += urllib_parse.quote_plus(pat)
        url += "?m=%d" % int(maxlen)
        url += "&p=%d" % int(phase)
        url += "&f=%d" % int(full)
        url += "&s=%d" % int(similar)
        url += "&w=%d" % int(winwidth)

        print(url)
        klog.d()
        r = requests.get(url)
        klog.d()
        if r.ok:
            klog.d()
            print(r.text)
            klog.d()


if __name__ == "__main__":
    klog.d(">>>")
    search()
    klog.d("<<<")

# vim: sw=4 ts=4 sts=4 ai et
