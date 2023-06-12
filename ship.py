import pygame
from laser import Laser


class Ship:
    COOLDOWN = 30
    MAX_HEALTH = 100
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_skin = None
        self.laser_of_ship = None
        self.lasers = []
        self.shooting_frequency = 0

    def draw(self, window):
        window.blit(self.ship_skin, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.health_of_the_ship(window)

    def move_lasers(self, vel):
        self.cooldown_timer()
        for laser in self.lasers:
            laser.move(vel)
            if laser.behind_the_screen(1200):
                self.lasers.remove(laser)

    def cooldown_timer(self):
        if self.shooting_frequency >= self.COOLDOWN:
            self.shooting_frequency = 0
        elif self.shooting_frequency > 0:
            self.shooting_frequency += 1

    def shooting(self):
        if self.shooting_frequency == 0:
            laser = Laser(x=self.x + 30, y=self.y - 50, laser_skin=self.laser_of_ship)
            self.lasers.append(laser)
            self.shooting_frequency = 1

    def health_of_the_ship(self, window):
        pygame.draw.rect(window, (189, 8, 77), (self.x, self.y + self.ship_skin.get_height() + 15, self.ship_skin.get_width(), 10))
        pygame.draw.rect(window, (8, 189, 117), (self.x, self.y + self.ship_skin.get_height() + 15, self.ship_skin.get_width() * (self.health/self.MAX_HEALTH), 10))
