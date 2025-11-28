"""
player_sprites.py
    Resources - Represents a resource icon and its current value.
        __init__ - Initializes the resource sprite with player reference and position.
        gather - Handles gathering the resource when clicked.
        update_image - Refreshes the sprite's image to display the current amount.
    Buildings - Represents a building icon and its current value.
        __init__ - Initializes the building sprite with player reference and position.
        purchase - Handles purchasing the building when clicked.
        update_image - Refreshes the sprite's image to display the current amount.
"""

# Standard Library Imports

# Third Party Imports
import pygame

# My Imports
from sprites import Entity
from globals import *
from interaction import check_interaction
from tooltip import BUILDINGCOSTS


class Resources(Entity):
    """Represents a resource icon and its current value."""
    
    def __init__(self, groups, player, scene, name=None, image=None, position=(0, 0)):
        """
        Initializes a resource sprite for a specific resource type.
        -------------------------------------------------------------
        Inherited : Entity

        Parameters:
            - groups : list of pygame.sprite.Group to add this sprite to
            - player : Player object, used for resource tracking
            - scene : Scene object, used for interaction checks
            - name : Name of the resource (wood, stone, etc.)
            - image : Optional pygame.Surface for the sprite
            - position : Top-left coordinates for placement
        """
        self.name = name
        self.player = player
        self.scene = scene
        self.value = self.player.resources[self.name.lower()]
        self.font = pygame.font.SysFont(None, 32)
        
        if image is None and name is not None:
            image = pygame.Surface((RESOURCEWIDTH, RESOURCEHEIGHT))
            image.fill('black')

        self.image = image
        self.rect = self.image.get_rect(topleft=position)

        super().__init__(groups, image=image, position=position)
        self.update_image()

    def gather(self):
        """
        Handles gathering resources when clicked.
        Updates the player's resources, decrements actions, and refreshes the image.
        -------------------------------------------------------------
        Called in:
            - Scene update loop when player interacts with resource
        """
        if check_interaction(self, self.scene):
            if self.player.actions_left <= 0:
                return False
            
            bonus = self.player.buildings['house']
            amount = 1 + bonus

            self.player.resources[self.name] += amount
            self.player.actions_left -= 1

            self.value = self.player.resources[self.name]
            self.update_image()
    
    def update_image(self):
        """
        Refreshes the resource sprite's image to display current value.
        -------------------------------------------------------------
        Called when the resource amount changes.
        """
        image = pygame.image.load(f'res/{self.name.lower()}.png')
        image = pygame.transform.scale(image, (RESOURCEWIDTH, RESOURCEHEIGHT))
        text_surf = self.font.render(f"{self.name.capitalize()} : {self.value}", True, 'black')
        text_rect = text_surf.get_rect(midright=(RESOURCEWIDTH - 25, RESOURCEHEIGHT // 2))
        image.blit(text_surf, text_rect)

        self.image = image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


class Buildings(Entity):
    """Represents a building icon and its current value."""
    
    def __init__(self, groups, player, scene, name=None, image=None, position=(0, 0), value=0):
        """
        Initializes a building sprite for a specific building type.
        -------------------------------------------------------------
        Inherited : Entity

        Parameters:
            - groups : list of pygame.sprite.Group to add this sprite to
            - player : Player object, used for building tracking
            - scene : Scene object, used for interaction checks
            - name : Name of the building (lumber_yard, mine, etc.)
            - image : Optional pygame.Surface for the sprite
            - position : Top-left coordinates for placement
            - value : Current amount of this building
        """
        self.name = name
        self.player = player
        self.scene = scene
        self.position = position
        self.value = value
        self.font = pygame.font.SysFont(None, 20)

        if image is None and name is not None:
            image = pygame.Surface((BUILDINGWIDTH, BUILDINGHEIGHT))

        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        super().__init__(groups, image, position)
        self.update_image()

    def purchase(self):
        if not check_interaction(self, self.scene):
            return False

        cost_dict = BUILDINGCOSTS[self.name]

        if self.player.actions_left <= 0 or not self.player.can_afford(cost_dict):
            return False

        self.player.spend(cost_dict)
        self.player.buildings[self.name] += 1
        self.player.actions_left -= 1
        self.value = self.player.buildings[self.name]

        self.update_image()
        for resource_sprite in self.scene.resource_group:
            self.scene.update_resource(resource_sprite)



    def update_image(self):
        """
        Refreshes the building sprite's image to display current value.
        -------------------------------------------------------------
        Called when the building amount changes.
        """
        image = pygame.image.load(f'res/{self.name.lower()}.png')
        image = pygame.transform.scale(image, (BUILDINGWIDTH, BUILDINGHEIGHT))
        text_surf = self.font.render(f"{self.name.replace('_', ' ').title()} : {self.value}", True, 'black')
        text_rect = text_surf.get_rect(midright=(BUILDINGWIDTH - 25, BUILDINGHEIGHT // 2))
        image.blit(text_surf, text_rect)

        self.image = image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
