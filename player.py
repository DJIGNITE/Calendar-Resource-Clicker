"""
player.py
-------------------------------------------------------
Player class that represents the player's current state, 
including available actions, resources, and constructed buildings.

Player:
    Represents the player and tracks resources, buildings, and actions left per turn.

    - reset_actions(self):
        Resets the player's available actions to the default number (3) plus
        any bonus from town_hall buildings.

    - can_afford(self, cost):
        Checks if the player has enough resources to afford a given cost tuple
        (wood, stone, iron, gold, food). Returns True if affordable, False otherwise.

    - spend(self, cost):
        Deducts resources from the player according to the given cost tuple.

    - add_building(self, name):
        Increments the count of a specified building in the player's buildings dictionary
        if it exists.
"""

class Player:
    """Represents the player, tracking actions, resources, and buildings."""

    def __init__(self):
        """
        Initializes a Player instance with default actions, resources, and buildings.
        -----------------------------------------------------------------------------
        Attributes:
            - actions_left : int
                Number of actions the player can take (3 + town_hall bonus)
            - resources : dict
                Dictionary tracking the player's current resources:
                    * wood   : int
                    * stone  : int
                    * iron   : int
                    * gold   : int
                    * food   : int
            - buildings : dict
                Dictionary tracking the player's buildings:
                    * lumber_yard
                    * quarry
                    * gold_mine
                    * iron_mine
                    * farm
                    * house
                    * town_hall
        """
        self.resources = {
            'wood': 0,
            'stone': 0,
            'iron': 0,
            'gold': 0,
            'food': 0
        }
        self.buildings = {
            'lumber_yard': 0,
            'quarry': 0,
            'gold_mine': 0,
            'iron_mine': 0,
            'farm': 0,
            'house': 0,
            'town_hall': 0
        }
        self.actions_left = 3 + (1 * self.buildings['town_hall'])

    def reset_actions(self):
        """
        Resets the player's available actions to the default number (3)
        plus any bonus from town_hall buildings.
        """
        self.actions_left = 3 + (1 * self.buildings['town_hall'])

    def can_afford(self, cost):
        """
        Checks if the player has enough resources to afford a cost tuple.
        -----------------------------------------------------------------------------
        Parameters:
            - cost : dict (wood, stone, iron, gold, food)
        
        Returns:
            - True if the player has enough resources, False otherwise
        """
        return (self.resources['wood'] >= cost.get('Wood', 0) and
                self.resources['stone'] >= cost.get('Stone', 0) and
                self.resources['iron'] >= cost.get('Iron', 0) and
                self.resources['gold'] >= cost.get('Gold', 0) and
                self.resources['food'] >= cost.get('Food', 0))

    def spend(self, cost):
        """
        Deducts resources from the player according to the given cost tuple.
        -----------------------------------------------------------------------------
        Parameters:
            - cost : dict (wood, stone, iron, gold, food)
        """
        self.resources['wood'] -= cost.get('wood',0)
        self.resources['stone'] -= cost.get('stone',0)
        self.resources['iron'] -= cost.get('iron',0)
        self.resources['gold'] -= cost.get('gold',0)
        self.resources['food'] -= cost.get('food',0)

    def add_building(self, name):
        """
        Adds a building to the player's collection if it exists.
        -----------------------------------------------------------------------------
        Parameters:
            - name : string
                Name of the building to add
        
        Updates:
            - self.buildings[name] : increments by 1 if the building exists
        """
        if name in self.buildings:
            self.buildings[name] += 1
