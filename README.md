# Colony Planner Game

**Colony Planner** is a turn-based simulation game built with Python and Pygame. Players manage resources, construct buildings, and plan their colony's growth over time using a calendar-based system.

---

## Table of Contents
- [Gameplay](#gameplay)
- [Features](#features)
- [Controls](#controls)
- [Game Mechanics](#game-mechanics)
- [Save and Reset](#save-and-reset)
- [Installation](#installation)
- [File Structure](#file-structure)

---

## Gameplay

Players start with basic resources and a few available actions per day. The goal is to expand your colony by constructing buildings, gathering resources, and optimizing productivity. Each building contributes to resource generation or improves your colony in other ways.

---

## Features

- **Dynamic Calendar:** Track days, weeks, and months. Each day, resources from buildings are automatically collected.  
- **Resource Management:** Manage wood, stone, iron, gold, and food to construct buildings.  
- **Building Construction:** Each building has a cost and can increase resource production, workforce, or available actions.  
- **Actions per Day:** Limited actions per day that can be spent on gathering or building. Actions reset when sleeping.  
- **Tooltips:** Hover over resources or buildings to see detailed info, including current quantities and costs.  
- **Reset Confirmation:** Clear save data safely with a multi-click confirmation system.  

---

## Controls

- **Left Click:** Interact with resources, buildings, or UI buttons.  
- **Mouse Hover:** Displays tooltips for resources and buildings.  
- **Month Navigation:** Click arrows to move forward or backward in the calendar.  
- **Sleep Button:** Advances the day and resets available actions.  
- **Clear Save Button:** Click multiple times to confirm save reset.  

---

## Game Mechanics

### Resources
- **Wood, Stone, Iron, Gold, Food**: Gathered from corresponding buildings or manually.
- Buildings like **Lumber Yard**, **Quarry**, **Mines**, and **Farm** produce resources automatically each day.  

### Buildings
- **Lumber Yard:** Produces wood daily.  
- **Quarry:** Produces stone daily.  
- **Iron Mine / Gold Mine:** Produces iron or gold daily.  
- **Farm:** Produces food daily.  
- **House:** Increases gathering efficiency.  
- **Town Hall:** Increases daily action limit.  

### Actions
- Each day, the player has a limited number of actions to gather resources or construct buildings.  
- Actions reset automatically when using the sleep button.  

---

## Save and Reset

- The game automatically saves progress.  
- **Clear Save:** Click the clear save button 5 times to reset your game.  
  - On the second-to-last click, a confirmation message appears.  
  - Countdown resets if not clicked within 5 seconds.  

---

## Installation

1. Install Python 3.10+  
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Clone the repository
  ```bash
  git clone https://github.com/DJIGNITE/calendar-resource-clicker.git
  ```
4. Run the game
  ```bash
  python main.py
  ```
