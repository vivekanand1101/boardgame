#!/usr/bin/env python
# coding=utf-8

import click

from bdgame.app import app
from bdgame.utils import load_game_conf
from bdgame.utils.game import prepare_game


@app.command()
def play():
    ''' Play the game after loading configuration from .bdgame '''

    # Loads the config and returns a dict
    conf = load_game_conf()

    # game time
    game = prepare_game(conf)
    result = game.play_game()
    game.display_results(result)
