#!/usr/bin/env python
# coding=utf-8

import click

from bdgame.app import app
from bdgame.utils import load_game_conf
from bdgame.exceptions import ItemNotFound, BDException

@app.command()
def play():
    ''' Play the game after loading configuration from .bdgame '''

    # Loads the config and returns a dict
    # containing 'nplayers', 'players', 'grid' as keys
    items = load_game_conf()
