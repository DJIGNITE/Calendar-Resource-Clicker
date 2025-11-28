"""
sprites.py
-------------------------------------------------------
Entity(Sprite): Superclass for all game sprites.
    - update(): Placeholder for entity-specific updates.
"""

import pygame
from pygame.sprite import Sprite

from events import EventHandler
from globals import *
from player import Player
from tooltip import TOOLTIPS

class Entity(Sprite):
    """Super Class to represent all sprites on the screen."""
    def __init__(self, groups, image=None, position= (0, 0)):
        super().__init__(groups)
        """
        Base class for all visible objects in the game.
        ---------------------------------------------------
        Inherited : pygame.sprite.Sprite

        Parameters:
            - groups : List of sprite groups to which this sprite belongs
            - image : Optional pygame.Surface representing the sprite
            - position : Tuple (x, y) specifying the sprite's top-left position
        """
        if image is None:
            image = pygame.Surface((DATEWIDTH, DATEHEIGHT))

        self.in_groups = groups
        self.image = image
        self.rect = self.image.get_rect(topleft = position)

    def update(self):
        
        """
        Placeholder for entity-specific updates.
        ---------------------------------------------------
        Called during scene update.
        """
        pass
