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

    wcount = get_item('wcount')
    if not wcount:
        raise ItemNotFound('Number of correct words (wcount) not in .bdgame')
    wcount = int(wcount)

    locations = get_locations()
    words = get_words(grid, locations)
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

def get_locations():
    ''' Get the locations from config  and turn it into a list '''

    locations = get_item('locations')
    if not locations:
        raise ItemNotFound(
            'Coordinates of correct words(locations) not found in .bdgame')
    locations = locations.strip().split(',')

    locations_copy = []
    for i in locations:
        i = i.strip().split(' ')
        i = [l for l in i if l != '']
        locations_copy.append(i)

    return locations_copy


def _get_word(grid, location, shape):
    ''' Get the word from the grid
    :args grid: A 2D list of letters
    :args location: A list of either 4 or 6 elements, depending upon the shape
    word in the grid.
    :args shape: A string saying what kind of shape the word forms like:
        horizontal, vertical, diagonal or L '''

    if shape == 'horizontal':
        string = ''
        for i in range(int(location[1]), int(location[3]) + 1):
            string += grid[int(location[0])][i]
        return string

    elif shape == 'vertical':
        string = ''
        for i in range(int(location[0]), int(location[2]) + 1):
            string += grid[i][int(location[1])]
        return string


def get_words(grid, locations):
    ''' Given the locations in grid, extract the words out of it
    :args grid: A 2D list of strings
    :args locations: A list of lists where each list represents Coordinates
    of each word
    '''

    words = {}
    for i in range(len(locations)):
        # the shape is not 'L'
        word = None
        if len(locations[i]) == 4:
            # if the shape is horizontal
            if locations[i][0] == locations[i][2]:
                word = _get_word(grid, locations[i], shape='horizontal')

            # if the shape is vertical
            elif locations[i][1] == locations[i][3]:
                word = _get_word(grid, locations[i], shape='vertical')

            # if the shape is diagonal
            # elif (
                    # locations[i][1] != locations[i][3]
                    # and locations[i][0] != locations[i][2]):
                # word = _get_word(grid, locations[i], shape='diagonal')

            else:
                # The shape is L
                pass

        if word not in words:
            words[word] = {}
            words[word]['count'] = 1
            words[word]['locations'] = [locations[i]]
        else:
            words[word]['count'] += 1
            words[word]['locations'].append(locations[i])

    return words


def _game_starter(players):
    ''' Choose who will start the game
    The logic can be tweaked '''
    return players[0]


def _get_player_turn(last_player, players):
    ''' Return the player object whose turn is now '''

    if not last_player:
        return _game_starter(players)

    for i in range(len(players)):
        if players[i] == last_player:
            return players[(i+1) % len(players)]


def _words_left(words):
    ''' Check if there are any words left to be checked out '''

    count = 0
    for word in words:
        count += words[word]['count']

    return count


def display_board(board):
    ''' Display the board in a fansy manner '''

    click.echo()
    for i in board.grid:
        for j in i:
            click.echo(click.style(str(j + ' '), fg="yellow"), nl=False)
            click.echo(nl=False)
        click.echo()


def play_game(players, board, words):
    ''' Let's play the game return the winner's name or 'draw' '''

    click.echo(words)
    last_player = None
    while _words_left(words):
        current_player = _get_player_turn(
            last_player=last_player,
            players=players
        )

        # Show the board
        display_board(board)

        # Prompt the user to give input
        user_input = click.prompt(
            "%s play, it\'s your turn: " % current_player.name)
        user_input = user_input.strip().upper()
        if user_input == 'PASS':
            current_player.answers.append(user_input)
            click.echo(
                "%s has PASSed, %s's score is %s" % (
                    current_player.name,
                    current_player.name,
                    current_player.score
                    )
            )
        elif user_input in words and words[user_input]['count'] > 0:
            # he answered correctly
            current_player.answers.append(user_input)

            # decrease the word count
            words[user_input]['count'] -= 1
            # as of now, just remove any of the duplicates
            words[user_input]['locations'].pop()

            # increase his score
            current_player.score += 1
            # update his correct_answers list
            correct_answers = current_player.correct_answers
            correct_answers.append(user_input)
            current_player.correct_answers = correct_answers
            click.echo(
                "%s is a correct choice. %s's score is %s" % (
                    user_input,
                    current_player.name,
                    current_player.score
                )
            )
        elif user_input in words and words[user_input]['count'] == 0:
            # The word already taken, even the duplicate ones of the word
            current_player.answers.append(user_input)
            click.echo(
                "%s is a already identified. %s's score is %s" % (
                    user_input,
                    current_player.name,
                    current_player.score
                )
            )
        else:
            # he answered wrong
            current_player.answers.append(user_input)
            click.echo(
                "%s is a wrong choice. %s's score is %s" % (
                    user_input,
                    current_player.name,
                    current_player.score
                )
            )

        draw = True
        for player in players:
            if player.answers[-2:] != ['PASS', 'PASS']:
                draw = False
        if draw:
            return 'draw'

        last_player = current_player

    return _check_winner(players)


def _check_winner(players):
    ''' From the players score, check who is the winner and return name
    and if any two players having highest score have same score, the match
    is draw, return 'draw' '''

    p_scores = sorted(players, key=lambda x: x.score, reverse=True)
    if p_scores[0].score == p_scores[1].score:
        return "draw"
    return p_scores[0]
