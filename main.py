import pygame
import sys

from scene import Scene
from events import EventHandler
from globals import *

class Calendar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = Scene(self)

    def run(self):
        while self.running:
            self.update()
            self.draw()

    def update(self):
        EventHandler.poll_events()
        for event in EventHandler.events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.clock.tick(60)
        self.scene.update()
        pygame.display.update()

    def draw(self):
        self.scene.draw()

    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    calendar = Calendar()
    calendar.run()
