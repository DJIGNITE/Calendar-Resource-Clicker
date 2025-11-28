
"""
globals.py
-------------------------------------------------------
This file defines all the global constants used throughout
the game, including screen dimensions, calendar layout,
resource display, and build menu layout.

Constants:

Screen:
    - SCREENWIDTH: Width of the game window in pixels.
    - SCREENHEIGHT: Height of the game window in pixels.

Date Block:
    - DATEWIDTH: Width of each calendar date block.
    - DATEHEIGHT: Height of each calendar date block.

Calendar:
    - CALENDAROFFSETX: Horizontal offset of the calendar.
    - CALENDAROFFSETY: Vertical offset of the calendar.
    - MONTHBUTTONOFFSET: Spacing for month navigation buttons.

Resources:
    - RESOURCEPADDING: Padding between resource icons.
    - RESOURCEWIDTH: Width of each resource display icon.
    - RESOURCEHEIGHT: Height of each resource display icon.
    - RESOURCEOFFSETX: Horizontal offset for resource bar.
    - RESOURCEOFFSETY: Vertical offset for resource bar.

Build Menu:
    - BUILDMENUPADDING: Padding around build menu.
    - BUILDMENUWIDTH: Width of the build menu.
    - BUILDMENUHEIGHT: Height of the build menu.
    - BUILDMENUOFFSETX: Horizontal offset of build menu.
    - BUILDMENUOFFSETY: Vertical offset of build menu.
    - OPTIONHEIGHT: Height of each build option.
    - OPTIONSPACING: Vertical spacing between build options.
"""

SCREENWIDTH = 1280
SCREENHEIGHT = 720

# Date Block
DATEWIDTH = (SCREENWIDTH // 7) - 5
DATEHEIGHT = SCREENHEIGHT / 10

# Calendar
CALENDAROFFSETX = 18 // 2
CALENDAROFFSETY = SCREENHEIGHT - (DATEHEIGHT + 4) * 6
MONTHBUTTONOFFSET = 25

# Resources
RESOURCEPADDING = 10
RESOURCEWIDTH = SCREENWIDTH // 5 - RESOURCEPADDING - 5
RESOURCEHEIGHT = 75
RESOURCEOFFSETY = 5
RESOURCEOFFSETX = 35 // 2

# Buildings
BUILDINGPADDING = 10
BUILDINGWIDTH = SCREENWIDTH // 7 - BUILDINGPADDING - 5
BUILDINGHEIGHT = 50
BUILDINGOFFSETX = 35 // 2
BUILDINGOFFSETY = 5

# BuildMenu
BUILDMENUPADDING = 50
BUILDMENUWIDTH = SCREENWIDTH // 2 - BUILDMENUPADDING
BUILDMENUHEIGHT = SCREENHEIGHT - BUILDMENUPADDING
BUILDMENUOFFSETX = 25
BUILDMENUOFFSETY = 25
OPTIONHEIGHT = 75
OPTIONSPACING = 10


