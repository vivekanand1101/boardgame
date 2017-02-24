#!/usr/bin/env python
# coding=utf-8

import os

import click

from bdgame.app import app
from bdgame.utils import create_config

@app.command()
@click.option('--nplayers', prompt="Number of players in the game: ", default=2,
              help="The number of players that will play this game")
@click.option('--gsize', prompt="Grid size: ",
              help="Grid size of board ", default="15 15")
@click.option('--input', prompt="Input file path of grid",
              help="Input file path of the grid", default="input.txt")
def make(nplayers, gsize, input):
    ''' Given the game configurations, make the game '''

    if not input.startswith('/'):
        input = os.path.join(os.path.abspath(
            os.path.dirname(__file__)),
            '../..',
            input
        )
    with click.open_file(input, 'r') as input_file:
        grid = input_file.read()

    players = []
    for i in range(1, nplayers + 1):
        players.append(click.prompt('Enter name of player:',
                default='player %s' % i))
    create_config(nplayers=nplayers, gsize=gsize, grid=grid, players=players)
