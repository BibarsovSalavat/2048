#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Module of application 2048
# Copyright (C) 2021
# Salavat Bibarsov <Bibarsov.Salavat@gmail.com>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


__all__ = ['Events', 'States', 'GameObject']


# Python modules
from abc import ABC
from dataclasses import dataclass
import pygame

# Modules of application
#

@dataclass
class _XY:
    """ Class for save axises coordinate.  """

    x: int
    y: int

    def get(self, attr = None) -> tuple:
        
        if attr: return getattr(self, attr)
        else: return self.x, self.y

    @property
    def axises(self) -> tuple:

        return (self.x, self.y)

# ABSTRACT CLASSES

class GameObject(ABC):
    """ Base class for all gameobject of tile type.  """

    def __init__(self, x: int, y: int,  width: int, height: int, 
                color: tuple = None) -> None:
        
        self.position = _XY(x, y)
        self.surface = pygame.Surface((width, height))

        if color:self.color = color
        
        self.value: list

    def draw(self):
        """ Method of draw object"""

        if self.color: self.surface.fill(self.color)

        if hasattr(self, 'value'):

            if type(self.value) is list:

                for item in self.value:

                    item.draw()
                    self.surface.blit(item.surface, item.position.axises)


class _SubsystemEvents(ABC):
    """ Base class for event subsystem all types.  """

    def __init__(self) -> None:
        
        self.status: bool = None
        self.value: str = None

    def __bool__(self) -> bool:
        """ Method to return status of event. """

        return self.status
    
    def __str__(self) -> str:
        """ Method to return value of event.  """

        value = str()

        if self.value: value = self.value

        return value

    def __call__(self) -> None:
        """ Event handler. To call this method in every subsystem events.  """

        # Reset values
        self.status = False
        self.value = None


class _ApplicationEvents(_SubsystemEvents):
    """ Subsystem of application events.  """

    def __call__(self, event) -> None:
        """ Application event handler.  """

        # Reset values
        super().__call__()

        # Default control settings
        if event.type == pygame.QUIT or\
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):

            self.status = True
            self.value = 'Quit'


class _KeyboardEvents(_SubsystemEvents):
    """ Subsystem of keyboard events.  """

    def __call__(self, event) -> None:
        """ Keyboard event handler.  """

        # Reset values
        super().__call__()

        # Default control settings
        if event.type == pygame.KEYDOWN:

            KEYBOARD_MAP = {
                'up': (pygame.K_UP, pygame.K_w, pygame.K_KP8),
                'down': (pygame.K_DOWN, pygame.K_s, pygame.K_KP2),
                'left': (pygame.K_LEFT, pygame.K_a, pygame.K_KP4),
                'right': (pygame.K_RIGHT, pygame.K_d, pygame.K_KP6)
            }

            for key, value in KEYBOARD_MAP.items():

                if event.key in value: 

                    self.status = True
                    self.value = key


class _MouseEvents(_SubsystemEvents):
    """ Subsystem of mouse events.  """

    def __call__(self, event) -> None:
        """ Mouse event handler.  """

        # Reset values
        super().__call__()


class Events:
    """ Interface for all subsystems of events.  """

    def __init__(self) -> None:

        # Subsystems of events
        self.application = _ApplicationEvents()
        self.keyboard = _KeyboardEvents()
        self.mouse = _MouseEvents()

    def __bool__(self) -> bool:
        """ This method return control events states.  """

        return any([self.keyboard, self.mouse])

    def __call__(self) -> None:
        """ Method for handle all event types.  """
        
        # Get event
        event = pygame.event.poll()

        # Call all handle methods
        self.application(event=event)
        self.keyboard(event=event)
        self.mouse(event=event)


class States:
    """ Interface for application control of states.  """

    def __init__(self) -> None:
        
        self.is_running: bool = True
        self.is_updated: bool = False

    def __bool__(self) -> bool:
        """ Method To Return main application state.  """

        return self.is_running

    def __call__(self, events: Events) -> None:
        """ Method to check events to change application state.  """

        # Check application events
        if events.application: self.is_running = False

        # Check valid user events
        if events: self.is_updated = True
        else: self.is_updated = False