#!/usr/bin/env python
# coding=utf-8

import os
import sys

import click

from bdgame.app import app
from bdgame.utils import create_config

@app.command()
@click.option('--nplayers', prompt="Number of players in the game: ", default=2,
              help="The number of players that will play this game")
@click.option('--gsize', prompt="Grid size: ",
              help="Grid size of board ", default="15 15")
@click.option('--inp_file', prompt="Input file path of grid",
              help="Input file path of the grid", default="input.txt")
@click.option('--wcount', prompt="Number of correct words: ",
              help="Number of correct words")
def make(nplayers, gsize, inp_file, wcount):
    ''' Given the game configurations, make the game '''

    if not inp_file.startswith('/'):
        inp_file = os.path.join(os.path.abspath(
            os.path.dirname(__file__)),
            '../..',
            inp_file
        )
    with click.open_file(inp_file, 'r') as input_file:
        grid = input_file.read()

    players = []
    for i in range(1, nplayers + 1):
        name = click.prompt('Enter name of player: ', default='player %s' % i)
        name = name.strip()
        if ',' in name:
            click.echo(', cannot be in a name, try again')
            sys.exit()
        players.append(name)

    # store the names of players as a comma separated string
    players = ",".join(players)

    locations = []
    for i in range(int(wcount)):
        location = click.prompt("Enter the location of word "
                                " on grid like( 2 3 2 5): ")
        if len(location.strip().split()) % 2 != 0:
            click.echo("Locations are two D coordinates, they have to be pairs"
                       " Try again.")
            sys.exit()
        elif location in locations:
            click.echo("Duplicate locations not allowed")
            sys.exit()
        locations.append(location)
        click.echo('Location noted')

    # store the locations as comma separated strings
    locations = ','.join(locations)
    create_config(
        nplayers=nplayers,
        gsize=gsize,
        grid=grid,
        players=players,
        wcount=int(wcount),
        locations=locations,
    )
