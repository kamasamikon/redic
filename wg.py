#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import click

import urllib.parse as urllib_parse

@click.command()
@click.option('--maxlen', '-m', default=40, help='Max length of trans part.')
@click.option('--phase', '-p', default=False, is_flag=True, help='Show phase.')
@click.option('--full', '-f', default=False, is_flag=True, help='Full output.')
@click.option('--similar', '-s', default=False, is_flag=True, help='Find similar.')
@click.argument('pat', type=str)
def search(pat, maxlen, phase, full, similar):
    '''Search words according to given re pattern.'''

    try:
        winwidth = os.get_terminal_size().columns
    except:
        winwidth = 0

    url = "http://localhost:12000/"
    url += urllib_parse.quote_plus(pat)
    url += "?m=%d" % int(maxlen)
    url += "&p=%d" % int(phase)
    url += "&f=%d" % int(full)
    url += "&s=%d" % int(similar)
    url += "&w=%d" % int(winwidth)

    print(url)
    r = requests.get(url)
    if r.ok:
        print(r.text)

if __name__ == "__main__":
    search()

# vim: sw=4 ts=4 sts=4 ai et
