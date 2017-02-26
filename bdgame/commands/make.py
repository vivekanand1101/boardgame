#!/usr/bin/env python
# coding=utf-8

import os
import sys

import click

from bdgame.app import app
from bdgame.utils import create_config

@app.command()
@click.option('--gsize', prompt="Grid size: ",
              help="Grid size of board", default="15 15")
@click.option('--inp', help="Input file path of the grid")
@click.option('--wcount', prompt="Number of correct words",
              help="Number of correct words")
@click.option('--nplayers', prompt="Number of players in the game", default=2,
              help="The number of players that will play this game")
def make(nplayers, gsize, inp, wcount):
    ''' Given the game configurations, make the game '''

    if inp:
        if not inp.startswith('/'):
            inp = os.path.join(os.path.abspath(
                os.path.dirname(__file__)),
                '../..',
                inp
            )
        with click.open_file(inp, 'r') as input_file:
            grid = input_file.read()

    else:
        inp = click.prompt(
            "Enter the grid(console input) or try again and specify --inp ")
    players = []
    for i in range(1, nplayers + 1):
        name = click.prompt('Enter name of player', default='player %s' % i)
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
                                " on grid like( 2 3 2 5) ")
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
