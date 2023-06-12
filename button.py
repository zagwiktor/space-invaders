import pygame


class Button:
    def __init__(self, x, y, button_image):
        self.x = x
        self.y = y
        self.button_image = button_image
        self.rectangle = self.button_image.get_rect()
        self.rectangle.topleft = (self.x, self.y)
        self.active = False

    def draw(self, window):
        window.blit(self.button_image, (self.rectangle.x, self.rectangle.y))

    def clicked(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rectangle.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.active == False:
                self.active = True
                return True
            else:
                return False
        if pygame.mouse.get_pressed()[0] == 0:
            self.active = False
