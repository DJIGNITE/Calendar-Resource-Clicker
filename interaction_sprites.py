"""
buttons_tooltip.py
    SleepButton - Button to advance the day and reset player actions
        __init__ - Initializes the sleep button with optional text and image
    Tooltip - Tooltip sprite for displaying dynamic or static text over a resource/building icon
        __init__ - Sets up the tooltip with the associated icon, text, and player reference
        update - Updates tooltip visibility, position, and text each frame
"""

# Standard Library Imports
import time

# Third Party Imports
import pygame

# My Imports
from sprites import Entity
from tooltip import TOOLTIPS
from globals import *
from interaction import check_interaction
from save_load import clear_save


class SleepButton(Entity):
    """Button to end the day and reset player actions."""

    def __init__(self, groups, image=None, name='sleep', text='Sleep', position=(0, 0), font_size=32):
        """
        Initializes a SleepButton sprite.
        -------------------------------------------------------------
        Inherited from:
            - Entity

        Parameters:
            - groups : list of pygame.sprite.Group, groups to add this sprite to
            - image : pygame.Surface, optional custom button image
            - name : str, internal button label, default 'sleep'
            - text : str, displayed on the button
            - position : tuple(int, int), center position on screen
            - font_size : int, font size for rendering text
        """
        font = pygame.font.SysFont(None, font_size)
        text_surf = font.render(name.capitalize(), True, 'black')
        width, height = text_surf.get_size()

        if image is None:
            image = pygame.Surface((width + 10, height + 10))
            image.fill('darkblue')

        text_rect = text_surf.get_rect(center=(image.get_width() // 2, image.get_height() // 2))
        image.blit(text_surf, text_rect)

        super().__init__(groups, image, position)
        self.rect = image.get_rect(center=position)


class Tooltip(Entity):
    """
    Tooltip sprite that displays contextual information for a resource
    or building icon when the mouse hovers over it.
    -------------------------------------------------------------
    Attributes:
        - icon : reference to the resource/building sprite this tooltip is attached to
        - text : either a string or a callable returning a string (for dynamic text)
        - player : reference to Player object (used if text is a callable)
        - font : pygame.font.Font instance for rendering text
        - visible : bool indicating if tooltip is currently visible
    """

    PADDING = 6

    def __init__(self, groups, icon, text, player):
        """
        Initializes the Tooltip sprite.
        -------------------------------------------------------------
        Parameters:
            - groups : list of pygame.sprite.Group, groups to add tooltip to
            - icon : Resource or Building sprite that this tooltip is associated with
            - text : str or callable(player) -> str, content to display
            - player : Player instance, passed to callable if text is dynamic
        """
        self.icon = icon
        self.text = text
        self.player = player
        self.font = pygame.font.SysFont(None, 24)
        self.visible = False

        image = pygame.Surface((1, 1), pygame.SRCALPHA)  # placeholder, updated in update()
        super().__init__(groups, image=image, position=(0, 0))

    def update(self):
        """
        Updates the tooltip each frame.
        Checks if the mouse is hovering over the associated icon,
        updates text content, resizes the tooltip image, and positions it near the mouse.
        -------------------------------------------------------------
        Called each frame via Scene.update().
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.icon.rect.collidepoint(mouse_pos):
            display_text = self.text(self.player) if callable(self.text) else self.text
            lines = display_text.split('\n')

            # Calculate width and height
            line_height = self.font.get_height()
            width = max(self.font.size(line)[0] for line in lines) + self.PADDING * 2
            height = len(lines) * line_height + (len(lines) - 1) * 4 + self.PADDING * 2

            # Create image
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill('black')  # background
            pygame.draw.rect(self.image, 'white', self.image.get_rect(), 2)  # border

            tip_title_font = pygame.font.SysFont(None, 24, bold=True)
            y_offset = self.PADDING
            for i, line in enumerate(lines):
                font = tip_title_font if i == 0 else self.font
                color = 'lightskyblue' if i == 0 else 'white'
                text_surf = font.render(line, True, color)
                self.image.blit(text_surf, (self.PADDING, y_offset))
                y_offset += line_height + 4

            # Position tooltip near mouse
            self.rect = self.image.get_rect(topleft=(mouse_pos[0] + 12, mouse_pos[1] + 12))
            if self.rect.right > SCREENWIDTH:
                self.rect = self.image.get_rect(topright=(mouse_pos[0] - 12, mouse_pos[1] + 12))
            self.visible = True
        else:
            self.visible = False
            self.rect.topleft = (-999, -999)

class ClearSave(pygame.sprite.Sprite):
    def __init__(self, groups, scene, position):
        super().__init__(groups)
        self.scene = scene
        self.position = position
        self.countdown = 5   # 5 clicks required
        self.font = pygame.font.SysFont(None, 18)
        self.last_click_time = None

        # Base image
        self.base_image = pygame.image.load("res/clear_save.png").convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (BUILDINGWIDTH, BUILDINGHEIGHT))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=position)

        self.update_text()

    def update_text(self, confirmation=False):
        """Draw countdown text onto the button."""
        self.image = self.base_image.copy()
        if confirmation:
            text = f"Reseting your save data.\n Click again to confirm."
            color = 'red'
        else:
            text = f"Clear Save File\n{self.countdown} clicks"
            color = 'black'
        lines = text.split('\n')

        total_height = sum(self.font.size(line)[1] for line in lines)
        y_offset = (self.image.get_height() - total_height) // 2
        for line in lines:
            surf = self.font.render(line, True, color)
            x =(self.image.get_width() - surf.get_width()) // 2
            self.image.blit(surf, (x, y_offset))
            y_offset += surf.get_height()

    def on_click(self):
        """Called when user clicks the button."""
        self.check_time_since_click()
        if check_interaction(self, self.scene):
            self.last_click_time = time.time()
            if self.countdown > 2:
                self.countdown -= 1
                self.update_text()
            elif self.countdown == 2:
                self.countdown -= 1
                self.update_text(confirmation=True)
            else:
                # LAST CLICK → perform reset
                self.clear_save_and_reload()

    def clear_save_and_reload(self):
        # Clear save file
        clear_save()

        # Reset your player / world state here
        self.scene.reset()

        # Trigger your full refresh logic
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "reload"}))

    def check_time_since_click(self):
        if self.last_click_time and (time.time() - self.last_click_time >5):
            self.countdown = 5
            self.last_click_time = None
            self.update_text()


