#!/usr/bin/env python
# coding=utf-8

import click

from bdgame.app import app
from bdgame.utils import create_config

@app.command()
@click.option('--np', help="Number of players in the game ", default=2)
@click.option('--gsize', help="Grid size of board (like: 15x15) ", default="15x15")
def make(np, gsize):
    ''' Given the game configurations, make the game '''
    create_config(np=np, gsize=gsize)
