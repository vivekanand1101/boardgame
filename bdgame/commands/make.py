#!/usr/bin/env python
# coding=utf-8

from bdgame.app import app
from bdgame.utils import create_config

@app.command()
def make():
    ''' Given the game configurations, make the game '''
    create_config()
