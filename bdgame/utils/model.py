#!/usr/bin/env python
# coding=utf-8

class Board(object):
    ''' The Board Class '''

    def __init__(self, np, gsize, board):
        ''' Instantiate the board '''
        self.np = np
        self.gsize = gsize
        self.board = board

    def __repr__(self):
        ''' Represent the board '''
        return self.board


class Player(object):
    ''' The Player Class '''

    def __init__(self, name):
        ''' Instantiate the player object '''
        self.name = name

    def __repr__(self):
        ''' Represent the player object '''
        return "Player Name: %s", self.name
