#!/usr/bin/env python
# coding=utf-8

import click

from bdgame.app import app
from bdgame.utils import create_config

@app.command()
@click.option('--nplayers', prompt="Number of players in the game: ", default=2,
              help="The number of players that will play this game")
@click.option('--gsize', prompt="Grid size (like: 15x15): ",
              help="Grid size of board (like: 15x15): ", default="15x15")
def make(nplayers, gsize):
    ''' Given the game configurations, make the game '''

    click.echo('number of players: ', nplayers)
    click.echo('grid size: ', gsize)
    # create_config(nplayers=nplayers, gsize=gsize)
