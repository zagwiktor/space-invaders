import pygame
class Laser:
    def __init__(self, x, y, laser_skin):
        self.x = x
        self.y = y
        self.laser_skin = laser_skin
        self.mask = pygame.mask.from_surface(self.laser_skin)

    def draw(self, window):
        window.blit(self.laser_skin, (self.x, self.y))

    def move(self, velocity_of_laser):
        self.y += velocity_of_laser

    def behind_the_screen(self, height_of_screen):
        if self.y <= height_of_screen and self.y >= 0:
            return False
        else:
            return True

