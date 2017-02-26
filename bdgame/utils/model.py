#!/usr/bin/env python
# coding=utf-8

import click

import bdgame.utils as utils
from bdgame.exceptions import BDException


class Board(object):
    ''' The Board Class '''

    def __init__(self, grid, length, breadth):
        ''' Instantiate the board '''
        self.grid = grid
        self.length = length
        self.breadth = breadth
        self._recognized_locations = []

    def __repr__(self):
        ''' Represent the board '''
        return "Board looks like: %s" % self.grid

    @property
    def recognized_locations(self):
        ''' Return the recognized_locations in the grid '''
        return self._recognized_locations

    @recognized_locations.setter
    def recognized_locations(self, value):
        ''' Add new recognized_location on the board '''
        self._recognized_locations = value


class Player(object):
    ''' The Player Class '''

    def __init__(self, name):
        ''' Instantiate the player object '''
        self.name = name
        self.score = 0
        self.answers = []
        self._correct_answers = []

    def __repr__(self):
        ''' Represent the player object '''
        return "Player Name: %s" % self.name

    def __eq__(self, other):
        ''' Equality of player '''
        return self.name == other.name

    @property
    def correct_answers(self):
        ''' Returns the correct answers answered by the user '''
        return self._correct_answers

    @correct_answers.setter
    def correct_answers(self, correct_answers):
        ''' Set the correct answers '''
        self._correct_answers = correct_answers


class Game(object):
    ''' The Game class '''

    def __init__(self, board, players, conf):
        ''' Instantiate the game object '''
        self.board = board
        self.players = players
        self.conf = conf

    def _words_left(self):
        ''' Check if there are any words left to be checked out '''

        count = 0
        for word in self.conf['words']:
            count += self.conf['words'][word]['count']

        return count

    def _recognized_location(self, j, i):
        ''' From the recognized_locations in board, check if the Coordinates
        are recognized or not '''

        for location in self.board.recognized_locations:
            shape = utils.recognize_shape(location)
            if not shape:
                raise BDException('The word is not fitting any shape')
            all_coordinates = utils.trav_grid(
                self.board.grid,
                location,
                shape=shape,
                select='coordinates'
            )

            # click.echo(all_coordinates, nl=False)
            if (i, j) in all_coordinates:
                return True

        return False

    def display_board(self):
        ''' Display the board in a fancy manner '''

        click.echo()
        for i in range(self.board.length):
            for j in range(self.board.breadth):
                if not self._recognized_location(j, i):
                    click.echo(
                        click.style(str(self.board.grid[i][j] + ' '),
                                    fg="yellow"), nl=False
                    )
                    click.echo(nl=False)
                else:
                    click.echo(
                        click.style(str(self.board.grid[i][j] + ' '),
                                    fg="blue"), nl=False
                    )
                    click.echo(nl=False)

            click.echo()
        click.echo()

    def _game_starter(self):
        ''' Choose who will start the game
        The logic can be tweaked '''
        return self.players[0]

    def _get_player_turn(self, last_player):
        ''' Return the player object whose turn is now '''

        if not last_player:
            return self._game_starter()

        for i in range(len(self.players)):
            if self.players[i] == last_player:
                return self.players[(i+1) % len(self.players)]

    def _check_winner(self):
        ''' From the players score, check who is the winner and return name
        and if any two players having highest score have same score, the match
        is draw, return 'draw' '''

        p_scores = sorted(self.players, key=lambda x: x.score, reverse=True)
        if p_scores[0].score == p_scores[1].score:
            return "draw"
        return p_scores[0]

    def play_game(self):
        ''' Play the game '''

        words = self.conf['words']
        last_player = None
        while self._words_left():
            current_player = self._get_player_turn(
                last_player=last_player,
            )

            # Show the board
            self.display_board()

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

                # increase his score
                current_player.score += 1
                # update his correct_answers list
                correct_answers = current_player.correct_answers
                correct_answers.append(user_input)
                current_player.correct_answers = correct_answers

                # update the recognized_locations
                recognized_locations = self.board.recognized_locations
                recognized_locations.append(words[user_input]['locations'][0])
                self.board.recognized_locations = recognized_locations

                # decrease the word count
                words[user_input]['count'] -= 1
                # as of now, just remove any of the duplicates
                words[user_input]['locations'].pop()

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

            all_pass = True
            for player in self.players:
                if player.answers[-2:] != ['PASS', 'PASS']:
                    all_pass = False
            if all_pass:
                return self._check_winner()

            last_player = current_player

        return self._check_winner()


    def display_results(self, result):
        ''' Given the result, display it '''
        if not isinstance(result, str):
            click.echo()
            click.secho("The game is over and ", nl=False, fg="green")
            click.secho("%s " % result.name, nl=False, fg="blue")
            click.secho("won the game. ", nl=False, fg="green")
            click.secho("%s " % result.name, nl=False, fg="blue")
            click.secho("answered: ", nl=False, fg="green")
            click.secho("%s " % result.correct_answers, nl=False, fg="blue")
            click.echo()
            click.secho("The final board looks like: ", fg="red")
            self.display_board()
        else:
            click.echo()
            click.secho("Match draw :/ ", fg="green")
            click.echo()
            click.echo("The final board looks like: ")
            self.display_board()
