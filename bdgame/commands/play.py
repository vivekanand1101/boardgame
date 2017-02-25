#!/usr/bin/env python
# coding=utf-8

import click

from bdgame.app import app
from bdgame.utils import get_item, check_grid_sane, get_grid
from bdgame.exceptions import ItemNotFound, BDException

@app.command()
def play():
    ''' Play the game after loading configuration from .bdgame '''

    nplayers = get_item('nplayers')
    if not nplayers:
        raise ItemNotFound('Number of players(nplayers) not found in .bdgame')
    nplayers = int(nplayers)

    players = get_item('players')
    if not players:
        raise ItemNotFound('Player names (players) not found in .bdgame')

    players = players.split(',')
    if len(players) != nplayers:
        raise BDException('Names of all the players aren\'t present in .bdgame file')

    gsize = get_item('gsize')
    if not gsize:
        raise ItemNotFound('Grid size (gsize) is absent in .bdgame')

    if len(gsize.split(' ')) != 2:
        raise BDException('Grid size format is wrong.')

    gsize = gsize.strip().split(' ')
    glen, gbred = gsize[0], gsize[1]

    grid = get_item('grid')
    if not grid:
        raise ItemNotFound('Grid is absent in .bdgame')

    sane = check_grid_sane(grid, glen, gbred)
    if not sane:
        click.echo('Grid does not match with grid size, check in config file '
                   ' or make the game again')

    # Get the grid in form of 2D array
    grid = get_grid(grid)
