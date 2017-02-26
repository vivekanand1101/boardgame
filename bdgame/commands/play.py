#!/usr/bin/env python
# coding=utf-8

import click

from bdgame.app import app
from bdgame.utils import load_game_conf, make_players, make_board, play_game
from bdgame.exceptions import ItemNotFound, BDException

@app.command()
def play():
    ''' Play the game after loading configuration from .bdgame '''

    # Loads the config and returns a dict
    # containing 'nplayers', 'players', 'grid' as keys
    items = load_game_conf()

    # Make player and board
    players = make_players(items['players'])
    board = make_board(items['grid'], items['glen'], items['gbred'])
    click.echo(items['words'])
    result = play_game(players, board, items['words'])
    if not isinstance(result, str):
        click.echo()
        click.secho("The game is over and %s won the game. %s answered: %s"
                    % (result.name, result.name, result.correct_answers))
        click.echo()
    else:
        click.echo()
        click.secho("Match draw :/ ", fg="green")
        click.echo()
