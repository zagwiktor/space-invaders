import pygame
from laser import Laser
from ship import Ship
import os
GREEN_ONE = (pygame.image.load(os.path.join("images", "alien-green-1.png")),
             pygame.image.load(os.path.join("images", "laser.png")))

GREEN_TWO = (pygame.image.load(os.path.join("images", "alien-green-2.png")),
             pygame.image.load(os.path.join("images", "laser.png")))

PINK = (pygame.image.load(os.path.join("images", "alien-pink.png")),
        pygame.image.load(os.path.join("images", "laser.png")))

YELLOW = (pygame.image.load(os.path.join("images", "alien-yellow.png")),
          pygame.image.load(os.path.join("images", "laser.png")))

ENEMY_SKINS = [GREEN_ONE, GREEN_TWO, PINK, YELLOW]

class Enemy(Ship):
    def __init__(self, x, y, enemy_skin, heatlh=100):
        super().__init__(x, y, heatlh)
        self.x = x
        self.y = y
        self.enemy_skin, self.laser_of_ship = ENEMY_SKINS[enemy_skin]
        self.mask = pygame.mask.from_surface(self.enemy_skin)

    def get_width(self):
        return self.enemy_skin.get_width()

    def get_height(self):
        return self.enemy_skin.get_height()



    def draw(self, window):
        window.blit(self.enemy_skin, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)


    def move(self, vel):
        self.y += vel

    def shooting(self):
        if self.shooting_frequency == 0:
            laser = Laser(x=self.x + 20, y=self.y + 70, laser_skin=self.laser_of_ship)
            self.lasers.append(laser)
            self.shooting_frequency = 1
