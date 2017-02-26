#!/usr/bin/env python
# coding=utf-8


class Board(object):
    ''' The Board Class '''

    def __init__(self, grid, length, breadth):
        ''' Instantiate the board '''
        self.grid = grid
        self.length = length
        self.breadth = breadth

    def __repr__(self):
        ''' Represent the board '''
        return "Board looks like: %s" % self.grid


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
