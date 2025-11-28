"""
interaction.py
    check_interaction - Determines if a sprite is being interacted with by the player.
"""

# Standard Library Imports

# Third Party Imports
import pygame

# My Imports
from events import EventHandler

def check_interaction(sprite: pygame.sprite, scene) -> bool:
    """
    Checks whether a given sprite is being interacted with by the player.
    Interaction is defined as a left mouse click while hovering over the sprite,
    and only if no conflicting UI elements (like build menu or sleep button) are present.

    -------------------------------------------------------------
    Parameters:
        - sprite : pygame.sprite.Sprite
            The sprite to check for interaction.
        - scene : Scene object
            The current scene containing UI elements and context.

    Returns:
        - bool : True if the sprite was clicked and interaction is allowed, else False
    """
    if hasattr(scene, 'build_menu'):
        return False
    
    if hasattr(scene, 'sleep_button'):
        return False
    
    if not EventHandler.clicked_any():
        return False
    
    mouse_pos = pygame.mouse.get_pos()
    if not sprite.rect.collidepoint(mouse_pos):
        return False
    
    if EventHandler.clicked(1):
        return True
    
    return False
