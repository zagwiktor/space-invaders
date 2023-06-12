from ship import Ship
from pathlib import Path
import json

import pygame
import os
PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("images", "player-space.png"))
PLAYER_LASER = pygame.image.load(os.path.join("images", "player-laser.png"))

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=100)
        self.ship_skin = PLAYER_SPACE_SHIP
        self.laser_of_ship = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_skin)
        self.health = health
        self.username = None
        self.level = 0
        self.difficulty = "Easy"

    def get_width(self):
        return self.ship_skin.get_width()

    def get_height(self):
        return self.ship_skin.get_height()


    def save_score(self):
        path = Path('Scores.json')
        scores = []
        need_to_be_append = True
        try:
            file = path.open('r')
            scores = json.load(file)
            if f"{self.username}" in scores:
                index = -1
                for x in scores[self.username]["Difficulty"]:
                    index += 1
                    if x[0] == self.difficulty:
                        need_to_be_append = False
                        if x[1] < self.level:
                            scores[self.username]["Difficulty"][index][1] = self.level
                            break
                if need_to_be_append:
                    scores[self.username]["Difficulty"].append([self.difficulty, self.level])
            else:
                scores[self.username] = {
                    "Difficulty": [(self.difficulty, self.level)],
                }
        except FileNotFoundError:
            scores = {
                f"{self.username}": {
                    "Difficulty": [(self.difficulty, self.level)],
                }
            }
        finally:
            file = path.open('w')
            json.dump(scores, file, indent=4)
            file.close()






