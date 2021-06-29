#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Module of application 2048
# Copyright (C) 2021
# Salavat Bibarsov <Bibarsov.Salavat@gmail.com>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


__title__ = '2048'
__summary__ = 'Clone of 2048 game on python and pygame library.'
__url__ = 'https://github.com/BibarsovSalavat/2048'

__version__ = '0.0.1 init (dev)'

__author__ = 'Salavat Bibarsov'
__email__ = 'Bibarsov.Salavat@gmail.com'

__license__ = 'GNU General Public License v3.0'
__copyright__ = 'Copyright, 2021 %s' % __author__

__all__ = []


# Python modules
import os

# Modules of application
from main import Application

# Set icon path
_BASE = os.path.dirname(__file__)
icon = os.path.join(_BASE, 'icon.png')

if os.path.exists(icon): _ICON = icon
else: _ICON = None


if __name__ == '__main__':

    # Application Initialize
    Game = Application(__title__, __version__, _ICON)

    # Running game application
    Game()
