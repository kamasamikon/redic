#!/usr/bin/env python3

import os
import click
import dbquery


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

    lines = dbquery.search(pat, maxlen, phase, full, similar, winwidth)
    print("\r\n".join(lines))

if __name__ == "__main__":
    search()
