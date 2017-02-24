#!/usr/bin/env python
# coding=utf-8

import os
import sys
from configparser import ConfigParser

import click

CFG_PATH = os.path.join(os.environ.get('HOME'), '.bdgame')
CONFIG = ConfigParser()
CONFIG.optionxform = str


def create_config(nplayers, gsize, grid, players):
    ''' Method that creates the configuration file
    of the game based on the info provided

    :args np: Number of players to be playing the game
    :args gsize: Grid size of the board
    '''

    CONFIG['nplayers'] = {'nplayers': nplayers}
    CONFIG['gsize'] = {'gsize': gsize}
    CONFIG['grid'] = {'grid': grid}
    CONFIG['players'] = {'players': players}

    if os.path.exists(CFG_PATH):
        if click.confirm('You already have a config file, if you continue '
                         'the config of last game will be lost '):
            with click.open_file(CFG_PATH, 'w+') as config_file:
                CONFIG.write(config_file)
        else:
            sys.exit(1)
    else:
        with click.open_file(CFG_PATH, 'w+') as config_file:
            CONFIG.write(config_file)
