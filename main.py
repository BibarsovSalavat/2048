#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Module of application 2048
# Copyright (C) 2021
# Salavat Bibarsov <Bibarsov.Salavat@gmail.com>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


__all__ = ['Application']


# Python modules
from dataclasses import dataclass
import sys
import random
import pygame

# Modules of application
from library import States, Events, GameObject, TextObject


@dataclass(frozen=True)
class Config:
    """ Class to save application default config.  """

    display: tuple = (500, 672)
    fps: int = 30


@dataclass
class Color:
    """ Class to save game colors.  """

    header: tuple = (250, 248, 239)
    board: tuple = (187, 173, 160)
    null_tile: tuple = (205, 193, 180)
    black_text: tuple = (119, 100, 101)
    white_text: tuple = (249, 246, 242)
    value_color: tuple = (
        (237, 224, 200),
        (242, 177, 121),
        (245, 149, 99),
        (246, 124, 95),
        (246, 94, 59),
        (237, 207, 114)
    )


class GameHeader(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int, 
                color: tuple, title: str) -> None:

        super().__init__(x, y, width, height, color=color)

    
    def update(self, action): pass


class ValueOfTile(TextObject):
    """ .  """

    def update(self, value: str):
        self.value = value

    @property
    def size(self):

        length = len(str(self.value))
        size = length * 5

        return 75 - size

    @property
    def color(self):

        if self.value > 4: return Color.white_text
        else: return Color.black_text


class TileOfGameBoard(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        
        # Default value of tile
        self.value = ValueOfTile(0)

    def draw(self):

        super().draw()

        if int(self.value) != 0:
 
            value_rect = self.value.surface.get_rect()

            width, height = self.surface.get_size()

            value_rect.center = (width // 2, height // 2)

            self.surface.blit(self.value.surface, value_rect)

    @property
    def color(self): # TODO Color switch algorytm

        tile_color = None

        if int(self.value) == 0: tile_color = Color.null_tile
        else: 
            tile_color = (238, 228, 218)

        return tile_color


class GameBoard(GameObject):
    """ Main gameobject. He show tiles and do action for manipulate theys.  """

    def __init__(self, x: int, y: int, width: int, height: int, 
                color: tuple) -> None:
        super().__init__(x, y, width, height, color=color)

        self.value = self._create_tiles()

    def _create_tiles(self) -> list:

        value = []

        padding = 14

        x = padding
        y = padding

        for tile in range(1, 17):

            value.append(TileOfGameBoard(x, y, 107, 107))

            if tile % 4 == 0:
                x = padding
                y += 107 + padding

            else: x += 107 + padding
        
        else: return value

    def update(self, action: str):

        null = []

        for tile in self.value:
            if tile.value.value == 0:
                null.append(tile)

        tile = random.choice(null)
        tile.value.update(2)


class Application:
    """ Main facade. Class for running game application.  """

    def __init__(self, title: str, version: str, icon: str = None, 
                config: dataclass = Config()) -> None:
        
        self.title: str = title
        self.version: str = version
        self.icon: str = icon

        self.config: dataclass = config

        # Subsystems of application
        self.states = States()
        self.events = Events()

        # These attributes will be defined __load method
        self.clock: object
        self.screen: object
        self.queue = []

    def __load(self):
        """ Method of initialize application base objects.  """
        
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(self.title)

        if self.icon:
            self.icon = pygame.image.load(self.icon)
            pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.config.display)

        self.queue.append(GameHeader(0,0, 500, 172, Color.header, self.title))
        self.queue.append(GameBoard(0, 172, 500, 500, Color.board))

        self._drawinger()
        
    def _frame_rate(self):
        """ Method for control frame rate update.  """

        return self.clock.tick(self.config.fps)

    def _drawinger(self):
        
        for obj in self.queue:

            # Object draw
            obj.draw()

            # Object draw at screen
            self.screen.blit(obj.surface, obj.position.axises)

        # Display update
        pygame.display.update()

    def _updater(self):

        action = str(self.events.keyboard)

        for obj in self.queue:

            obj.update(action)

    def __bool__(self) -> bool:
        """ This method call event handler and check status application. """

        self.events() # To read all events
        self.states(self.events) # Check status

        return bool(self.states)

    def __call__(self) -> None:
        """ Method initialize main game loop.  """

        self.__load() # Starting application

        while self:
            """ Main game loop.  """

            # Screen will be updated if user call valid event
            if self.states.is_updated:
                
                self._updater() # Update games objects
                self._drawinger() # Draw screen

                print(self.events.keyboard) # TMP action

            self._frame_rate() # Control frame rate

        else:
            """ Single point of application exit.  """

            # TODO: Save game

            # Exit from application
            pygame.quit()
            sys.exit()