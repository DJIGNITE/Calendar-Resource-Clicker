"""
scene.py
-------------------------------------------------------------
Manages the game scene including calendar display, resource bar,
player actions, and menus. Handles input, drawing, and updating
all interactive and static elements within the game window.
"""

# Standard Library Imports
import calendar
from datetime import datetime, date, timedelta

# Third-Party Imports
import pygame

# Personal Imports
from sprites import Entity
from calendar_sprites import DateBlock, WeekDay, Month, MonthButton
from player_sprites import Resources, Buildings
from interaction_sprites import SleepButton, Tooltip, ClearSave
from player import Player
from tooltip import TOOLTIPS
from globals import *
from events import EventHandler
from save_load import save_game, load_game


class Scene:
    """
    Main class for managing the game scene.
    -------------------------------------------------------------
    Attributes:
        - app : main app instance containing screen and game loop
        - sprites : pygame.sprite.Group containing all sprites
        - button_group : group for interactive buttons
        - resource_group : group for resource sprites
        - date_block_group : group for calendar day blocks
        - menus : group for active menus
        - building_group : group for building sprites
        - tooltip_group : group for tooltip sprites
        - today : datetime object for the current game date
        - year, month : current displayed year and month
        - weeks : calendar weeks for the current month
        - player : Player object for resources, buildings, and actions
    """

    def __init__(self, app):
        """
        Initializes the Scene, generates calendar, resource bar, building bar, tooltips,
        and loads any saved game state.
        -------------------------------------------------------------
        Parameters:
            - app : main app instance containing screen and game loop
        """
        self.app = app

        self.sprites = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()
        self.resource_group = pygame.sprite.Group()
        self.date_block_group = pygame.sprite.Group()
        self.menus = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.tooltip_group = pygame.sprite.Group()
        self.interaction_group = pygame.sprite.Group()

        self.today = datetime.today()
        self.year, self.month = 2025, 11
        self.weeks = calendar.Calendar().monthdayscalendar(self.year, self.month)
        _, self.days_in_month = calendar.monthrange(self.year, self.month)
        
        self.player = Player()
        
        
        self.gen_cal()
        self.gen_resource_bar()
        self.gen_building_bar()
        self.gen_tooltips()
        self.create_clear_save_button()
        
        
        self.sleeping = False
        load_game(self)

    def gen_cal(self):
        """
        Builds the calendar by generating month, weekdays, and date blocks.
        -------------------------------------------------------------
        Called during initialization and calendar refresh.
        """
        font = pygame.font.SysFont(None, 28)
        self.gen_month()
        self.gen_weekdays(font)
        self.gen_date_blocks(font)

    def gen_weekdays(self, font):
        """
        Generates WeekDay sprites for each day of the week.
        -------------------------------------------------------------
        Parameters:
            - font : pygame.font.Font instance for text rendering
        """
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for col, name in enumerate(day_names):
            x = col * (DATEWIDTH + 4) + CALENDAROFFSETX
            y = CALENDAROFFSETY - 40
            WeekDay([self.sprites], name=name, position=(x, y))

    def gen_date_blocks(self, font):
        """
        Generates DateBlock sprites for each day in the current month.
        -------------------------------------------------------------
        Parameters:
            - font : pygame.font.Font instance for day numbers
        """
        for row, week in enumerate(self.weeks):
            for col, day in enumerate(week):
                if day == 0:
                    continue

                block_date = date(self.year, self.month, day)
                x = col * (DATEWIDTH + 4) + CALENDAROFFSETX
                y = row * (DATEHEIGHT + 4) + CALENDAROFFSETY

                if block_date == self.today.date():
                    image = pygame.image.load('res/dateblock_present.png')
                elif block_date < self.today.date():
                    image = pygame.image.load('res/dateblock_past.png')
                else:
                    image = pygame.image.load('res/dateblock.png')

                image = pygame.transform.scale(image, (DATEWIDTH, DATEHEIGHT))
                block = DateBlock([self.date_block_group], image=image, position=(x, y))

                text = font.render(str(day), True, 'black')
                block.image.blit(text, (10, 10))

    def gen_month(self):
        """
        Generates Month display and month navigation buttons.
        -------------------------------------------------------------
        """
        month_name = calendar.month_name[self.month] + ' ' + str(self.year)
        x = SCREENWIDTH // 4
        y = int(CALENDAROFFSETY - DATEHEIGHT - 15)

        month = Month([self.sprites], name=month_name, position=(x, y))
        MonthButton([self.sprites, self.button_group], name='month_forward',
                    image=pygame.image.load('res/forward_arrow.png'),
                    position=(month.rect.right + MONTHBUTTONOFFSET, month.rect.centery))
        MonthButton([self.sprites, self.button_group], name='month_back',
                    image=pygame.image.load('res/back_arrow.png'),
                    position=(month.rect.left - MONTHBUTTONOFFSET, month.rect.centery))

    def gen_resource_bar(self):
        """
        Generates the top resource bar with icons and current values.
        -------------------------------------------------------------
        Called during initialization.
        """
        resources = [name for name in self.player.resources]
        font = pygame.font.SysFont(None, 32)
        for col, name in enumerate(resources):
            x = col * (RESOURCEWIDTH + RESOURCEPADDING) + RESOURCEOFFSETX
            y = RESOURCEOFFSETY
            image = pygame.image.load(f'res/{name.lower()}.png')
            image = pygame.transform.scale(image, (RESOURCEWIDTH, RESOURCEHEIGHT))
            value = self.player.resources[name.lower()]
            text_surf = font.render(f"{name} :    {value}", True, 'black')
            text_rect = text_surf.get_rect(midright=(RESOURCEWIDTH - 25, RESOURCEHEIGHT // 2))
            image.blit(text_surf, text_rect)

            Resources([self.resource_group], scene=self, player=self.player,
                      name=name.lower(), image=image, position=(x, y))

    def gen_building_bar(self):
        """
        Generates the building bar with all player's building icons and values.
        -------------------------------------------------------------
        """
        buildings = [name for name in self.player.buildings]
        font = pygame.font.SysFont(None, 20)
        for col, name in enumerate(buildings):
            x = col * (BUILDINGWIDTH + BUILDINGPADDING) + BUILDINGOFFSETX
            y = (RESOURCEHEIGHT + RESOURCEOFFSETY) + BUILDINGOFFSETY
            image = pygame.image.load(f'res/{name.lower()}.png')
            image = pygame.transform.scale(image, (BUILDINGWIDTH, BUILDINGHEIGHT))
            value = self.player.buildings[name.lower()]
            text_surf = font.render(f'{name} :    {value}', True, 'black')
            text_rect = text_surf.get_rect(midright=(BUILDINGWIDTH - 25, BUILDINGHEIGHT // 2))
            image.blit(text_surf, text_rect)

            Buildings([self.building_group], player=self.player, scene=self,
                      name=name.lower(), image=image, position=(x, y), value=value)

    def gen_tooltips(self):
        """
        Generates Tooltip sprites for all resources and buildings.
        -------------------------------------------------------------
        Called during scene setup after sprites are created.
        """
        self.tooltip_group = pygame.sprite.Group()

        for resource_icon in self.resource_group:
            tooltip_callable = TOOLTIPS['resource'].get(resource_icon.name.lower())
            if tooltip_callable:
                Tooltip(groups=[self.tooltip_group], icon=resource_icon,
                        text=tooltip_callable, player=self.player)

        for building_icon in getattr(self, 'building_group', []):
            tooltip_callable = TOOLTIPS['building'].get(building_icon.name.lower())
            if tooltip_callable:
                Tooltip(groups=[self.tooltip_group], icon=building_icon,
                        text=tooltip_callable, player=self.player)
                
    def create_clear_save_button(self):
        for sprite in self.building_group:
            if sprite.name == 'lumber_yard':
                lumber_yard_sprite = sprite
                break
        clear_save_x = lumber_yard_sprite.rect.left
        clear_save_y = lumber_yard_sprite.rect.bottom + 10

        self.clear_save_button = ClearSave([self.interaction_group], scene=self, position=(clear_save_x, clear_save_y))


    def change_month(self):
        """
        Handles month navigation input (forward/back) and refreshes the calendar.
        -------------------------------------------------------------
        Uses EventHandler for mouse click detection.
        """
        if hasattr(self, 'build_menu'):
            return
        mouse_pos = pygame.mouse.get_pos()
        if not EventHandler.clicked_any():
            return
        for button in self.button_group:
            if not button.rect.collidepoint(mouse_pos):
                continue
            if button.name == 'month_forward' and EventHandler.clicked(1):
                if self.month < 12:
                    self.month += 1
                else:
                    self.month = 1
                    self.year += 1
                self.refresh_calendar()
            if button.name == 'month_back' and EventHandler.clicked(1):
                if self.month > 1:
                    self.month -= 1
                else:
                    self.month = 12
                    self.year -= 1
                self.refresh_calendar()

    def refresh_calendar(self):
        """
        Rebuilds calendar sprites for the current month.
        -------------------------------------------------------------
        Clears old sprites and regenerates the calendar.
        """
        self.sprites.empty()
        self.button_group.empty()
        self.date_block_group.empty()
        self.weeks = calendar.Calendar().monthdayscalendar(self.year, self.month)
        self.gen_cal()
        self.sleeping = False

    def gather_resource(self):
        """
        Processes clicks on resource sprites to collect them.
        -------------------------------------------------------------
        """
        for resource in self.resource_group:
            resource.gather()

    def purchase_building(self):
        """
        Processes clicks on building sprites to purchase them.
        -------------------------------------------------------------
        """
        for building in self.building_group:
            building.purchase()
        

    def update_resource(self, resource):
        """
        Updates a single resource sprite to match player's current value.
        -------------------------------------------------------------
        Parameters:
            - resource : Resource sprite
        """
        resource.value = self.player.resources[resource.name]
        resource.update_image()

    def update_sleep_button(self):
        """
        Shows or hides the sleep button depending on remaining player actions.
        -------------------------------------------------------------
        """
        if self.player.actions_left <= 0:
            image = pygame.image.load('res/sleep.png')
            image = pygame.transform.scale(image, (RESOURCEWIDTH, RESOURCEHEIGHT))
            if not hasattr(self, 'sleep_button'):
                self.sleep_button = SleepButton([self.sprites], image=image,
                                                position=(SCREENWIDTH // 2, SCREENHEIGHT * .8))
        else:
            if hasattr(self, 'sleep_button'):
                self.sleep_button.kill()
                del self.sleep_button

    def handle_sleep(self):
        """
        Handles sleep button click to advance the day and reset actions.
        -------------------------------------------------------------
        """
        if hasattr(self, 'sleep_button'):
            mouse_pos = pygame.mouse.get_pos()
            if self.sleep_button.rect.collidepoint(mouse_pos) and EventHandler.clicked(1):
                if hasattr(self, 'build_menu'):
                    self.build_menu.kill()
                    del self.build_menu
                print(f"Player slept, day advanced. {self.month}, {self.today}")
                self.advance_day()
                save_game(self)
                print(self.player.resources)

    def advance_day(self):
        """
        Advances the game day by one, updates resources from buildings,
        refreshes the calendar, and resets player actions.
        -------------------------------------------------------------
        """
        self.sleeping = True
        self.today += timedelta(days=1)
        self.year, self.month, self.day = self.today.year, self.today.month, self.today.day
        self.weeks = calendar.Calendar().monthdayscalendar(self.year, self.month)

        r = self.player.resources
        b = self.player.buildings
        r['wood'] += 1 * b['lumber_yard']
        r['stone'] += 1 * b['quarry']
        r['iron'] += 1 * b['iron_mine']
        r['gold'] += 1 * b['gold_mine']
        r['food'] += 1 * b['farm']

        self.refresh_calendar()

        for resource_sprite in self.resource_group:
            resource_sprite.value = r[resource_sprite.name]
            resource_sprite.update_image()

        self.player.reset_actions()

    def clear_save(self):
        self.clear_save_button.on_click()

    def reset(self):
        """Fully resets the game state after clearing save data."""
        
        # Reset date
        from datetime import datetime
        self.today = datetime.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day

        # Brand-new player
        self.player = Player()

        # Clear all existing sprite groups
        self.sprites.empty()
        self.resource_group.empty()
        self.building_group.empty()
        self.date_block_group.empty()
        self.button_group.empty()
        self.tooltip_group.empty()
        self.menus.empty()

        # Regenerate everything
        self.gen_cal()
        self.gen_resource_bar()
        self.gen_building_bar()
        self.gen_tooltips()

        # Recreate clear save button
        self.clear_save_button = ClearSave([self.interaction_group], scene=self,position=self.clear_save_button.rect.topleft)

    print("Game state reset.")



    def update(self):
        """
        Updates the scene and all interactive elements each frame.
        -------------------------------------------------------------
        Responsibilities:
            - Handles resource and building clicks
            - Updates month navigation
            - Updates sprites, sleep button, and menus
            - Updates tooltips
        """
        EventHandler.click_consumed = False
        self.gather_resource()
        self.purchase_building()
        self.change_month()
        self.sprites.update()
        self.update_sleep_button()
        self.handle_sleep()
        self.menus.update()
        self.tooltip_group.update()
        self.clear_save()

    def draw(self):
        """
        Draws the scene and all sprites to the screen.
        -------------------------------------------------------------
        """
        self.app.screen.fill('lightblue')
        self.date_block_group.draw(self.app.screen)
        self.sprites.draw(self.app.screen)
        self.resource_group.draw(self.app.screen)
        self.building_group.draw(self.app.screen)
        self.interaction_group.draw(self.app.screen)
        self.tooltip_group.draw(self.app.screen)
        self.menus.draw(self.app.screen)
        
        
