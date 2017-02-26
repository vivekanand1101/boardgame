#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json
from configparser import ConfigParser

import click

from bdgame.exceptions import BDException, ItemNotFound

CFG_PATH = os.path.join(os.environ.get('HOME'), '.bdgame')
CONFIG = ConfigParser()
CONFIG.optionxform = str

BLACKLISTED_WORDS = ['PASS']

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


def _get_item(item):
    ''' Read the configuration file and return the value of given
    item in config '''

    if os.path.exists(CFG_PATH):
        CONFIG.read(CFG_PATH)
        if item not in CONFIG.sections():
            return None
        values = CONFIG[item]
        return values[item]
    return None


def _check_grid_sane(grid, glen, gbred):
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


def _get_grid(grid):
    ''' Return grid in form of 2D list '''

    grid = grid.splitlines()
    grid_copy = []
    for row in grid:
        row = row.split()
        row = [i.upper() for i in row]
        grid_copy.append(row)
    return grid_copy


def _get_locations():
    ''' Get the locations from config  and turn it into a list '''

    locations = _get_item('locations')
    if not locations:
        raise ItemNotFound(
            'Coordinates of correct words(locations) not found in .bdgame')
    locations = locations.strip().split(',')

    locations_copy = []
    for i in locations:
        i = i.strip().split()
        locations_copy.append(i)

    return locations_copy


def _get_words(grid, locations):
    ''' Given the locations in grid, extract the words out of it
    :args grid: A 2D list of strings
    :args locations: A list of lists where each list represents Coordinates
    of each word
    '''

    words = {}
    for location in locations:
        shape = recognize_shape(location)
        if not shape:
            raise BDException('The word is not fitting any shape')

        word = trav_grid(
            grid=grid,
            location=location,
            shape=shape,
            select='word'
        )

        if word not in words:
            words[word] = {}
            words[word]['count'] = 1
            words[word]['locations'] = [location]
        else:
            words[word]['count'] += 1
            words[word]['locations'].append(location)

        for bword in BLACKLISTED_WORDS:
            if bword in words:
                words.pop(bword)
                click.echo("%s is blacklisted, removed")

    return words


def load_game_conf():
    ''' Method which returns all the items required for the game '''

    nplayers = _get_item('nplayers')
    if not nplayers:
        raise ItemNotFound('Number of players(nplayers) not found in .bdgame')
    nplayers = int(nplayers)

    players = _get_item('players')
    if not players:
        raise ItemNotFound('Player names (players) not found in .bdgame')

    players = players.split(',')
    if len(players) != nplayers:
        raise BDException('Names of all the players aren\'t present in .bdgame file')

    gsize = _get_item('gsize')
    if not gsize:
        raise ItemNotFound('Grid size (gsize) is absent in .bdgame')

    if len(gsize.split(' ')) != 2:
        raise BDException('Grid size format is wrong.')

    gsize = gsize.strip().split(' ')
    glen, gbred = int(gsize[0]), int(gsize[1])

    grid = _get_item('grid')
    if not grid:
        raise ItemNotFound('Grid is absent in .bdgame')

    sane = _check_grid_sane(grid, glen, gbred)
    if not sane:
        click.echo('Grid does not match with grid size, check in config file '
                   ' or make the game again')

    # Get the grid in form of 2D array
    grid = _get_grid(grid)

    wcount = _get_item('wcount')
    if not wcount:
        raise ItemNotFound('Number of correct words (wcount) not in .bdgame')
    wcount = int(wcount)

    locations = _get_locations()
    words = _get_words(grid, locations)
    output = {
        'nplayers': nplayers,
        'players': players,
        'grid': grid,
        'glen': glen,
        'gbred': gbred,
        'wcount': wcount,
        'words': words,
        'locations': locations,
    }

    return output


def override_conf(stream):
    ''' Given the file data in form of list of strings, override the existing config
    file. The grid is fixed to be 15 x 15 in this case '''

    # The first 15 lines are the grid
    grid = stream[:15]
    grid = ''.join(grid)

    # Number of correct words
    wcount = int(stream[15])

    # Locations of correct words
    locations = ','.join(stream[16:16+wcount])

    # Number of players
    nplayers = int(stream[16+wcount])

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

    create_config(
        nplayers=nplayers,
        grid=grid,
        gsize='15 15',
        players=players,
        wcount=wcount,
        locations=locations,
    )


def take_console_input(gsize):
    ''' Take the console input of the grid '''

    gsize = gsize.strip().split()
    grid = ''
    click.echo("Enter the grid(console input) or try again and specify --inp ")
    for i in range(int(gsize[0])):
        grid += click.prompt('', prompt_suffix='')
        grid += '\n'
    return grid


def trav_grid(grid, location, shape='any', select='word'):
    ''' Get the word from the grid
    :args grid: A 2D list of letters
    :args location: A list of either 4 or 6 elements, depending upon the shape
    word in the grid.
    :args shape: A string saying what kind of shape the word forms like:
        horizontal, vertical, diagonal or L '''

    coordinates = []
    if shape == 'horizontal':
        for i in range(int(location[1]), int(location[3]) + 1):
            if (int(location[0]), i) not in coordinates:
                coordinates.append((int(location[0]), i))

    if shape == 'vertical':
        for i in range(int(location[0]), int(location[2]) + 1):
            if (i, int(location[1])) not in coordinates:
                coordinates.append((i, int(location[1])))

    if shape == 'diagonal':
        diff = abs(int(location[0]) - int(location[2]))
        for i in range(diff+1):
            if (int(location[0])+i, int(location[1])+i) not in coordinates:
                coordinates.append((int(location[0])+i, int(location[1])+i))

    if shape == 'oneletter':
        if (int(location[0]), int(location[1])) not in coordinates:
            coordinates.append((int(location[0]), int(location[1])))

    if select == 'word':
        string = ''
        for i in coordinates:
            string += grid[i[0]][i[1]]
        return string

    return coordinates


def recognize_shape(location):
    ''' Given a location, find what shape it is '''

    if len(location) == 2:
        return 'oneletter'

    if len(location) == 4:
        if location[0] == location[2]:
            return 'horizontal'

        if location[1] == location[3]:
            return 'vertical'

        # if the shape is diagonal
        # x1 - x2 == y1 - y2
        if int(location[0]) == (
                int(location[2]) + int(location[1]) - int(location[3])):
            return 'diagonal'

    elif len(location) == 6:
        # Maybe L shape in future
        pass
