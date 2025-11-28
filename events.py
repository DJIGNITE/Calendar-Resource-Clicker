"""
events.py
-------------------------------------------------------
This file defines the EventHandler class, which handles all
keyboard and mouse input for the game. It tracks events
each frame and provides methods to check for key presses
and mouse clicks.


Class:
    - EventHandler: Handles input events and provides methods
      for key presses and mouse clicks.

Methods:
    - __init__: Initializes the event queue.
    - poll_events: Updates the event list from pygame.
    - keydown: Checks if a specific key was pressed.
    - clicked: Checks if a specific mouse button was clicked.
    - clicked_any: Checks if any mouse button was clicked.
    - mouse_pos: Checks the mouse position
    - hovering: checks if mouse is hovering over a sprite
"""

import pygame

class EventHandler:
    """Handles all input events for the game, including keyboard and mouse input."""
    def __init__() -> None:  
        """
        Initializes the EventHandler and fetches the initial
        list of events from pygame.
        -------------------------------------------------------
        Called Once:
            On creation of EventHandler
        """
        EventHandler.events = pygame.event.get()

        
    def poll_events():
        """
        Refreshes the event queue from pygame.
        -------------------------------------------------------
        Called Each Frame:
            Must be called once per frame to update the current
            list of events.
        """
        EventHandler.events = pygame.event.get()


    def keydown(key):
        """
        Checks if a specific key was pressed this frame.
        -------------------------------------------------------
        Parameters:
            - key: pygame key constant (e.g., pygame.K_SPACE)

        Returns:
            - True if the key was pressed this frame
            - False otherwise
        """
        for event in EventHandler.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
        return False
    
    def clicked(leftright = 1) -> bool:
        """
        Checks if a specific mouse button was clicked this frame.
        -------------------------------------------------------
        Parameters:
            - leftright: 1 for left click, 3 for right click

        Returns:
            - True if the button was clicked this frame
            - False if not clicked or already consumed
        """
        if EventHandler.click_consumed:
            return False
        for event in EventHandler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == leftright:
                    return True
                
    def clicked_any() -> bool:
        """
        Checks if any mouse button was clicked this frame.
        -------------------------------------------------------
        Returns:
            - True if any mouse button was clicked this frame
            - False otherwise
        """
        for event in EventHandler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False
    
    def mouse_pos():
        """
        Returns the current mouse position.
        -------------------------------------------------------
        Returns:
            - (x, y) tuple of mouse coordinates
        """
        return pygame.mouse.get_pos()


    def hovering(rect):
        """
        Checks if the mouse is currently hovering over a given rect.
        -------------------------------------------------------
        Parameters:
            - rect: pygame.Rect object to test hover against
        
        Returns:
            - True if mouse is inside the rect
            - False otherwise
        """
        return rect.collidepoint(EventHandler.mouse_pos())
