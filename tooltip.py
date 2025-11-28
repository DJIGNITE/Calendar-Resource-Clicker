"""
Tooltips Module
-----------------------------
Stores tooltip definitions for resources, buildings, and UI elements.
Some tooltips are static text, while others are dynamic and
reference current player values at runtime.
"""

# Define the resource costs for each building
BUILDINGCOSTS = {
    'lumber_yard': {'wood': 5, 'stone': 0, 'iron': 0, 'gold': 0, 'food': 2},
    'quarry': {'wood': 2, 'stone': 5, 'iron': 0, 'gold': 0, 'food': 2},
    'iron_mine': {'wood': 2, 'stone': 3, 'iron': 0, 'gold': 0, 'food': 2},
    'gold_mine': {'wood': 3, 'stone': 0, 'iron': 0, 'gold': 5, 'food': 2},
    'farm': {'wood': 2, 'stone': 2, 'iron': 0, 'gold': 0, 'food': 0},
    'house': {'wood': 5, 'stone': 3, 'iron': 0, 'gold': 0, 'food': 5},
    'town_hall': {'wood': 10, 'stone': 5, 'iron': 2, 'gold': 5, 'food': 10},
}

def format_cost(cost):
    """Return a compact single-line string showing non-zero costs."""
    return " | ".join(f"{k.capitalize()}: {v}" for k, v in cost.items() if v > 0)

TOOLTIPS = {
    'resource': {
        'wood': lambda player: (
            "Wood:\n"
            "Used for crafting basic buildings.\n"
            f"Current Wood: {player.resources['wood']}"
        ),
        'stone': lambda player: (
            "Stone:\n"
            "Used for crafting basic buildings.\n"
            f"Current Stone: {player.resources['stone']}"
        ),
        'iron': lambda player: (
            "Iron:\n"
            "Used for crafting basic buildings.\n"
            f"Current Iron: {player.resources['iron']}"
        ),
        'gold': lambda player: (
            "Gold:\n"
            "Used to pay workers for creating buildings.\n"
            f"Current Gold: {player.resources['gold']}"
        ),
        'food': lambda player: (
            "Food:\n"
            "Used to feed workers creating buildings.\n"
            f"Current Food: {player.resources['food']}"
        ),
    },

    'building': {
        'lumber_yard': lambda player: (
            "Lumber Yard\n"
            "Produces one wood per day.\n"
            f"Current Lumber Yards: {player.buildings['lumber_yard']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['lumber_yard'])} |"
        ),
        'quarry': lambda player: (
            "Quarry\n"
            "Produces one stone per day.\n"
            f"Current Quarries: {player.buildings['quarry']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['quarry'])} |"
        ),
        'iron_mine': lambda player: (
            "Iron Mine\n"
            "Produces one iron per day.\n"
            f"Current Iron Mines: {player.buildings['iron_mine']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['iron_mine'])} |"
        ),
        'gold_mine': lambda player: (
            "Gold Mine\n"
            "Produces one gold per day.\n"
            f"Current Gold Mines: {player.buildings['gold_mine']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['gold_mine'])} |"
        ),
        'farm': lambda player: (
            "Farm\n"
            "Produces one food per day.\n"
            f"Current Farms: {player.buildings['farm']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['farm'])} |"
        ),
        'house': lambda player: (
            "House\n"
            "Provides more workers.\n"
            "Gathering resources yields one extra resource.\n"
            f"Current Houses: {player.buildings['house']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['house'])} |"
        ),
        'town_hall': lambda player: (
            "Town Hall\n"
            "Improves morale.\n"
            "Increases your actions per day by one.\n"
            f"Current Town Halls: {player.buildings['town_hall']}\n"
            f"Cost:\n | {format_cost(BUILDINGCOSTS['town_hall'])} |"
        ),
    }
}
