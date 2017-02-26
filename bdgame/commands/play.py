#!/usr/bin/env python
# coding=utf-8

import os

import click

from bdgame.app import app
from bdgame.utils import load_game_conf, override_conf
from bdgame.utils.game import prepare_game


@app.command()
@click.option('--inp',
              help="Input file path of the grid containing grid and other details",
              required=False)
def play(inp):
    ''' Play the game after loading configuration from .bdgame '''

    if inp:
        if not inp.startswith('/'):
            inp = os.path.join(os.path.abspath(
                os.path.dirname(__file__)),
                '../..',
                inp
            )

        with click.open_file(inp, 'r') as stream:
            data = stream.readlines()
        override_conf(data)

    # Loads the config and returns a dict
    conf = load_game_conf()

    # game time
    game = prepare_game(conf)
    result = game.play_game()
    game.display_results(result)
