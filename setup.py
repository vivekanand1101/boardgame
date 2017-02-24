#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    ''' Open and read the file '''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='boardgame',
    packages=['boardgame'],
    version='0.0.1',
    description='A cli multiplayer board game in python',
    long_description=read('README.md'),
    author='Vivek Anand',
    author_email='vivekanand1101@fedoraproject.org',
    url='https://github.com/vivekanand1101/boardgame',
    keywords=['game', 'board', 'multiplayer'],
    classifiers=[
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    license='GNU General Public License v2.0',
    entry_points={
        'console_scripts': [
            'bdgame = bdgame.app:app'
        ],
    },
    include_package_data=True,
    install_requires=read('requirements.txt'),
    zip_safe=False,
)
