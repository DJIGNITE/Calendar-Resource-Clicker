"""
save_load.py
-------------------------------------------------------
Provides functions for saving and loading the current
game state, including the current date, player resources,
buildings, and actions left.

Functions:

save_game(game):
    Saves the current game state to a JSON file.

load_game(game):
    Loads a saved game state from a JSON file and updates
    the game and sprite values.
"""

import os
import json

FILEPATH = "savegame.json"

def save_game(game):
    """
    Saves the current game state to a JSON file.
    -------------------------------------------------------
    Parameters:
        - game : Scene or main game object containing
                 current date, player state, and sprites.
    
    Saves:
        - game.year, game.month, game.today.day
        - game.player.resources
        - game.player.buildings
        - game.player.actions_left
    """
    data = {
        'date' : {
            'year'  : game.year,
            'month' : game.month,
            'day'   : game.today.day
        },
        'player' : {
            'resources'    : game.player.resources,
            'buildings'    : game.player.buildings,
            'actions_left' : game.player.actions_left
        }
    }
    with open(FILEPATH, 'w') as f:
        json.dump(data, f, indent=4)

    print("Game saved.")


def load_game(game):
    """
    Loads a saved game state from a JSON file and updates
    the game object and its sprites accordingly.
    -------------------------------------------------------
    Parameters:
        - game : Scene or main game object to update.
    
    Returns:
        - True if a save file was found and loaded, False otherwise.
    
    Updates:
        - game.today, game.year, game.month, game.day
        - game.player.resources
        - game.player.buildings
        - game.player.actions_left
        - Resource and building sprites' values and images
        - Refreshes the calendar
    """
    if not os.path.exists(FILEPATH):
        print("No save file found.")
        return False

    with open(FILEPATH, 'r') as f:
        data = json.load(f)

    date = data.get("date", {})

    # Extract saved values (fallback to current)
    year  = date.get("year",  game.today.year)
    month = date.get("month", game.today.month)
    day   = date.get("day",   game.today.day)

    from datetime import datetime
    game.today = datetime(year, month, day)
    game.year  = year
    game.month = month
    game.day   = day  # stored separately if needed

    # Load player data
    player_data = data.get("player", {})
    game.player.resources    = player_data.get("resources", game.player.resources)
    game.player.buildings    = player_data.get("buildings", game.player.buildings)
    game.player.actions_left = player_data.get("actions_left", game.player.actions_left)

    # Update sprites
    game.refresh_calendar()
    for resource_sprite in game.resource_group:
        name = resource_sprite.name.lower()
        resource_sprite.value = game.player.resources[name]
        resource_sprite.update_image()

    for building_sprite in game.building_group:
        name = building_sprite.name.lower()
        building_sprite.value = game.player.buildings[name]
        building_sprite.update_image()
        
    print("Game Loaded.")
    return True

def clear_save():
    if os.path.exists(FILEPATH):
        os.remove(FILEPATH)
