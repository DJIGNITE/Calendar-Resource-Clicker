"""
calendar_sprites.py
    DateBlock - Represents a single day block on the calendar grid
    WeekDay - Represents a weekday label at the top of the calendar
    Month - Displays the current month and year above the calendar
    MonthButton - Clickable button to navigate between months
"""

# Standard Library Imports

# Third Party Imports
import pygame

# My Imports
from sprites import Entity
from globals import *


class DateBlock(Entity):
    """Represents a single day block on the calendar grid."""
    
    def __init__(self, groups, image=None, position=(0, 0)):
        """
        Initializes an individual day in the calendar.
        ---------------------------------------------------
        Inherited : Entity

        Parameters:
            - groups : list of pygame.sprite.Group to add this sprite to
            - image : Optional pygame.Surface, defaults to DATEWIDTH x DATEHEIGHT
            - position : Top-left coordinates for placement on the screen
        """
        if image is None:
            image = pygame.Surface((DATEWIDTH, DATEHEIGHT))
        super().__init__(groups, image, position)
        self.rect = image.get_rect(topleft=position)


class WeekDay(Entity):
    """Represents a weekday label at the top of the calendar."""
    
    def __init__(self, groups, name=None, image=None, position=(0, 0), font_size=28):
        """
        Creates a static label showing the day of the week.
        ---------------------------------------------------
        Inherited : Entity

        Parameters:
            - groups : list of pygame.sprite.Group to add this sprite to
            - name : Name of the weekday (Monday, Tuesday, etc.)
            - image : Optional pygame.Surface
            - position : Top-left coordinates for placement
            - font_size : Font size for text rendering
        """
        if image is None and name is not None:
            font = pygame.font.SysFont(None, font_size)
            text_surf = font.render(name, True, 'black')

            image = pygame.Surface((DATEWIDTH, font_size), pygame.SRCALPHA)
            image.fill('lightblue')
            text_rect = text_surf.get_rect(center=(DATEWIDTH // 2, font_size // 2))
            image.blit(text_surf, text_rect)

        super().__init__(groups, image=image, position=position)


class Month(Entity):
    """Represents the month and year label on the calendar."""
    
    def __init__(self, groups, name=None, image=None, position=(0, 0), font_size=40):
        """
        Displays the current month and year above the calendar.
        ---------------------------------------------------
        Inherited : Entity

        Parameters:
            - groups : list of pygame.sprite.Group to add this sprite to
            - name : Month name (e.g., "November 2025")
            - image : Optional pygame.Surface
            - position : Top-left coordinates for placement
            - font_size : Font size for text rendering
        """
        if image is None and name is not None:
            font = pygame.font.SysFont(None, font_size)
            text_surf = font.render(name, True, 'black')

            image_width = SCREENWIDTH // 2
            image_height = font_size + 10
            image = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
            image.fill('lightblue')
            text_rect = text_surf.get_rect(center=(image_width // 2, image_height // 2))
            image.blit(text_surf, text_rect)

        super().__init__(groups, image=image, position=position)


class MonthButton(Entity):
    """Clickable button to navigate between months."""
    
    def __init__(self, groups, name=None, image=None, position=(0, 0)):
        """
        Represents a navigation button (forward/back) for the calendar month.
        ---------------------------------------------------
        Inherited : Entity

        Parameters:
            - groups : list of pygame.sprite.Group to add this sprite to
            - name : Button identifier ("month_forward" or "month_back")
            - image : Optional pygame.Surface
            - position : Top-left coordinates for placement
        """
        if image is None and name is not None:
            image = pygame.Surface((10, 10))
            image.fill('black')

        self.name = name
        super().__init__(groups, image, position)
