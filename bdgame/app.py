#!/usr/bin/env python
# coding=utf-8

import click


@click.group()
def app():
    pass

__all__ = [
    'app',
]

import bdgame.commands.make
import bdgame.commands.play


if __name__ == '__main__':
    app()
