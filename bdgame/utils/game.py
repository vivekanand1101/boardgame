#!/usr/bin/env python
# coding=utf-8

from bdgame.utils import model


def make_players(players):
    ''' Makes player objects from player names
    :args players: A list of names of all the players
    '''

    player_list = []
    for player in players:
        player_list.append(model.Player(name=player))

    return player_list


def make_game(board, players, conf):
    ''' Make the game from given board, players and game configurations '''

    game = model.Game(
        board=board,
        players=players,
        conf=conf
    )
    return game


def make_board(grid, glen, gbred):
    ''' Makes board object from the given grid '''

    board = model.Board(
        grid=grid,
        length=glen,
        breadth=gbred,
    )

    return board


def prepare_game(conf):
    ''' Given the game configurations, prepare the game '''

    players = make_players(conf['players'])
    board = make_board(conf['grid'], conf['glen'], conf['gbred'])
    game = make_game(board, players, conf)
    return game
