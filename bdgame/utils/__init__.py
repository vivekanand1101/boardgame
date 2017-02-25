#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json
from configparser import ConfigParser

import click

from bdgame.exceptions import BDException, ItemNotFound
from bdgame.utils import model

CFG_PATH = os.path.join(os.environ.get('HOME'), '.bdgame')
CONFIG = ConfigParser()
CONFIG.optionxform = str


def create_config(nplayers, gsize, grid, players, wcount, locations):
    ''' Method that creates the configuration file
    of the game based on the info provided

    :args np: Number of players to be playing the game
    :args gsize: Grid size of the board
    '''

    CONFIG['nplayers'] = {'nplayers': nplayers}
    CONFIG['players'] = {'players': players}
    CONFIG['wcount'] = {'wcount': wcount}
    CONFIG['locations'] = {'locations': locations}
    CONFIG['gsize'] = {'gsize': gsize}
    CONFIG['grid'] = {'grid': grid}

    if os.path.exists(CFG_PATH):
        if click.confirm('You already have a config file, if you continue '
                         'the config of last game will be lost '):
            with click.open_file(CFG_PATH, 'w+') as config_file:
                CONFIG.write(config_file)
            click.echo('New config file created in $HOME/.bdgame')
        else:
            click.echo('You aborted creating new config file')
            sys.exit(1)
    else:
        with click.open_file(CFG_PATH, 'w+') as config_file:
            CONFIG.write(config_file)


def get_item(item):
    ''' Read the configuration file and return the value of given
    item in config '''

    if os.path.exists(CFG_PATH):
        CONFIG.read(CFG_PATH)
        if item not in CONFIG.sections():
            return None
        values = CONFIG[item]
        return values[item]
    return None


def check_grid_sane(grid, glen, gbred):
    ''' Check if the grid is according to the specifics
    mentioned by the user '''

    grid = grid.splitlines()
    if len(grid) != glen:
        return False
    for row in grid:
        row = row.split()
        if len(row) != gbred:
            return False
    return True


def get_grid(grid):
    ''' Return grid in form of 2D list '''

    grid = grid.splitlines()
    grid_copy = []
    for row in grid:
        row = row.split()
        grid_copy.append(row)
    return grid_copy


def load_game_conf():
    ''' Method which returns all the items required for the game '''

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
    glen, gbred = int(gsize[0]), int(gsize[1])

    grid = get_item('grid')
    if not grid:
        raise ItemNotFound('Grid is absent in .bdgame')

    sane = check_grid_sane(grid, glen, gbred)
    if not sane:
        click.echo('Grid does not match with grid size, check in config file '
                   ' or make the game again')

    # Get the grid in form of 2D array
    grid = get_grid(grid)

    output = {
        'nplayers': nplayers,
        'players': players,
        'grid': grid,
        'glen': glen,
        'gbred': gbred
    }

    return output

def make_players(players):
    ''' Makes player objects from player names
    :args players: A list of names of all the players
    '''

    player_list = []
    for player in players:
        player_list.append(model.Player(name=player))

    return player_list


def make_board(grid, glen, gbred):
    ''' Makes board object from the given grid '''

    board = model.Board(
        grid=grid,
        length=glen,
        breadth=gbred,
    )

    return board
