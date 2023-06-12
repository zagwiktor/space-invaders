import pygame
import re
import os
pygame.font.init()
class Username():
    COLOR_ACTIVE = pygame.Color(66, 245, 69)
    COLOR_INACTIVE = pygame.Color(245, 66, 117)
    USERNAME_FONT = pygame.font.Font(os.path.join("font", "GameSansSerif7-oPGx.ttf"), 70)
    def __init__(self, x, y, width, height, width_screen, username=''):
        self.x = x
        self.y = y
        self.width_screen = width_screen
        self.color = self.COLOR_INACTIVE
        self.username = username
        self.final_username = None
        self.rectangle = pygame.Rect(x, y, width, height)
        self.txt_surface = self.USERNAME_FONT.render(username, True, self.color)
        self.active = False

    def typing(self, event):
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(mouse_position):
                self.active = not self.active
            else:
                self.active = False
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.validate_username():
                        self.final_username = self.username
                    self.username = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
                self.txt_surface = self.USERNAME_FONT.render(self.username, True, self.color)

    def update(self):
        width = max(250, self.txt_surface.get_width() + 10)
        self.rectangle.w = width
        self.rectangle.x = self.width_screen/2 - self.rectangle.w/2


    def draw(self, window):
        window.blit(self.txt_surface, (self.rectangle.x + 5, self.rectangle.y + 5))
        pygame.draw.rect(window, self.color, self.rectangle, 2)

    def get_width(self):
        return self.rectangle.w

    def validate_username(self):
        if not re.search(r'[A-Z]', self.username):
            return False
        if not re.match(r'^[\w]+$', self.username):
            return False
        return True
