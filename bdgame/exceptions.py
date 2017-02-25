#!/usr/bin/env python
# coding=utf-8

class BDException(Exception):
    ''' Generic exception class for bdgame '''

    def __init__(self, msg):
        self.msg = msg


class ItemNotFound(BDException):
    ''' Raised when the item is not found '''

    def __init__(self, msg):
        self.msg = msg
