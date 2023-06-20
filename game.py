import pygame
import os
from player import Player
from enemy import Enemy
from button import Button
import random
from username import Username
from pathlib import Path
import json
pygame.font.init()

class Game():
    WIDTH = 1300
    HEIGHT = 1000
    GAME_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background_1.png")),
                                             (WIDTH, HEIGHT))
    PLAY_BUTTON = pygame.image.load(os.path.join("images", "button.png"))
    OPTIONS_BUTTON = pygame.image.load(os.path.join("images", "options_button.png"))
    QUIT_BUTTON = pygame.image.load(os.path.join("images", "quit_button.png"))
    EASY_BUTTON = pygame.image.load(os.path.join("images", "easy_button.png"))
    MEDIUM_BUTTON = pygame.image.load(os.path.join("images", "medium_button.png"))
    HARD_BUTTON = pygame.image.load(os.path.join("images", "hard_button.png"))
    SCORES_BUTTON = pygame.image.load(os.path.join("images", "scores-button.png"))
    BACK_BUTTON = pygame.image.load(os.path.join("images", "back_button.png"))
    GUIDE_BUTTON = pygame.image.load(os.path.join("images", "guide_button.png"))
    WINDOW = pygame.display.set_mode(size=(WIDTH, HEIGHT))

    def __init__(self):
        self.enemy_laser_velocity = 5
        self.enemies = []
        self.wave = 5
        self.enemy_velocity = 1
        self.level = 0
        self.lives = 4
        self.lost_timer = 0
        self.FPS = 60
        self.lost_message = False
        self.velocity_of_ship = 5
        self.font = pygame.font.Font(os.path.join("font", "GameSansSerif7-oPGx.ttf"), 70)
        self.clock = pygame.time.Clock()
        self.username_passed = False
        self.player = Player(600, 850)
        self.player_damage = 100
        self.player_scores = None

    def collision(self, first_object, second_object):
        offset_x = second_object.x - first_object.x
        offset_y = second_object.y - first_object.y
        result = first_object.mask.overlap(second_object.mask, (offset_x, offset_y))
        if result is not None:
            return result

    def redraw_window(self):
        self.WINDOW.blit(self.GAME_BACKGROUND, (0, 0))
        lives_label = self.font.render(f"LIVES: {self.lives}", 1, (255, 255, 255))
        level_label = self.font.render(f"LEVEL: {self.level}", 1, (255, 255, 255))
        self.WINDOW.blit(level_label, (10, 10))
        self.WINDOW.blit(lives_label, (self.WIDTH - lives_label.get_width(), 10))
        self.player.draw(self.WINDOW)
        for enemy in self.enemies:
            enemy.draw(self.WINDOW)

        if self.lost_message:
            lost_label = self.font.render("You Lost!", 1, (255, 255, 255))
            self.WINDOW.blit(lost_label, (self.WIDTH / 2 - lost_label.get_width() / 2, self.HEIGHT / 2))

        pygame.display.update()

    def game(self):
        game_is_on = True
        self.lost_message = False
        self.player.health = 100
        if self.player.difficulty == "Medium":
            self.lives = 3
        else:
            self.lives = 4
        self.level = 0
        self.player.x = 600
        self.player.y = 850
        self.lost_timer = 0
        self.enemies = []
        self.wave = 5

        while game_is_on:
            self.clock.tick(self.FPS)

            if self.lives <= 0 or self.player.health <= 0:
                self.lost_message = True
                self.redraw_window()
                self.lost_timer += 1

            if self.lost_message:
                if self.lost_timer >= self.FPS * 5:
                    game_is_on = False
                    self.player.save_score()
                else:
                    continue

            if len(self.enemies) == 0:
                self.level += 1
                self.player.level = self.level
                self.wave += 5
                for x in range(self.wave):
                    enemy = Enemy(random.randrange(100, self.WIDTH - 100), random.randrange(-1500, -100),
                                  random.randint(0, 3))
                    self.enemies.append(enemy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_is_on = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.player.x + self.velocity_of_ship > 0:
                self.player.x -= self.velocity_of_ship
            if keys[pygame.K_w] and self.player.y + self.velocity_of_ship > 0:
                self.player.y -= self.velocity_of_ship
            if keys[pygame.K_s] and self.player.y + self.velocity_of_ship + self.player.get_width() < self.HEIGHT:
                self.player.y += self.velocity_of_ship
            if keys[pygame.K_d] and self.player.x + self.velocity_of_ship + self.player.get_height() < self.WIDTH:
                self.player.x += self.velocity_of_ship
            if keys[pygame.K_SPACE]:
                self.player.shooting()

            for enemy in self.enemies[:]:
                enemy.move(self.enemy_velocity)
                enemy.move_lasers(self.enemy_laser_velocity)
                if random.randrange(0, 4 * 60) == 1:
                    enemy.shooting()
                if enemy.y + enemy.get_height() > self.HEIGHT:
                    self.lives -= 1
                    self.enemies.remove(enemy)
                if self.collision(enemy, self.player):
                    self.player.health -= 25
                    self.enemies.remove(enemy)
                for laser in enemy.lasers:
                    if self.collision(laser, self.player):
                        self.player.health -= 10
                        enemy.lasers.remove(laser)
            self.redraw_window()

            self.player.move_lasers(-5)

            for laser in self.player.lasers[:]:
                for enemy in self.enemies:
                    if self.collision(laser, enemy):
                        enemy.health -= self.player_damage
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)
                        self.player.lasers.remove(laser)

    def menu(self):
        menu_is_open = True

        username = Username((self.WIDTH / 2) - 125, 340, 250, 80, self.WIDTH)

        play_button = Button(self.WIDTH / 2 - self.PLAY_BUTTON.get_width() / 2,
                             self.HEIGHT / 2 - self.PLAY_BUTTON.get_height() / 2, self.PLAY_BUTTON)
        positioning_1 = (self.OPTIONS_BUTTON.get_width() - self.PLAY_BUTTON.get_width()) / 2
        positioning_2 = (self.QUIT_BUTTON.get_width() - self.PLAY_BUTTON.get_width()) / 2
        options_button = Button((self.WIDTH / 2 - self.PLAY_BUTTON.get_width() / 2) - positioning_1,
                                self.HEIGHT / 2 - self.PLAY_BUTTON.get_height() / 2 + 150, self.OPTIONS_BUTTON)
        quit_button = Button(self.WIDTH / 2 - self.PLAY_BUTTON.get_width() / 2 - positioning_2,
                             self.HEIGHT / 2 - self.PLAY_BUTTON.get_height() / 2 + 450, self.QUIT_BUTTON)
        scores_button = Button((self.WIDTH / 2 - self.PLAY_BUTTON.get_width() / 2),
                               (self.HEIGHT / 2 - self.PLAY_BUTTON.get_height() / 2) + 300, self.SCORES_BUTTON)
        info_button = Button(self.WIDTH - self.GUIDE_BUTTON.get_width() - 30,
                             self.HEIGHT - self.GUIDE_BUTTON.get_height() - 15, self.GUIDE_BUTTON)
        while menu_is_open:
            self.WINDOW.blit(self.GAME_BACKGROUND, (0, 0))
            menu_label = self.font.render("MENU", 1, (255, 255, 255))
            username_label = self.font.render("USERNAME: ", 1, (255, 255, 255))
            if not self.username_passed:
                username.update()
                username.draw(self.WINDOW)
            else:
                player_username_label = self.font.render(f"{self.player.username}", 1, (255, 255, 255))
                self.WINDOW.blit(player_username_label, (self.WIDTH / 2 - player_username_label.get_width() / 2, 350))
            self.WINDOW.blit(menu_label, (self.WIDTH / 2 - menu_label.get_width() / 2, 50))
            self.WINDOW.blit(username_label, (self.WIDTH / 2 - username_label.get_width() / 2 + 30, 250))
            play_button.draw(self.WINDOW)
            scores_button.draw(self.WINDOW)
            options_button.draw(self.WINDOW)
            quit_button.draw(self.WINDOW)
            info_button.draw(self.WINDOW)
            pygame.display.update()
            for event in pygame.event.get():
                if play_button.clicked() and self.username_passed:
                    self.game()
                if options_button.clicked() and self.username_passed:
                    self.player.difficulty = self.options()
                if scores_button.clicked() and self.username_passed:
                    self.scores()
                if info_button.clicked():
                    self.guide()
                if quit_button.clicked() or event.type == pygame.QUIT:
                    menu_is_open = False
                username.typing(event)
            if username.final_username is not None:
                self.username_passed = True
                self.player.username = username.final_username
        pygame.quit()

    def options(self):
        options_are_open = True
        medium_x = (self.WIDTH / 2 - self.MEDIUM_BUTTON.get_width() / 2)
        medium_y = (self.HEIGHT / 2 - self.MEDIUM_BUTTON.get_height() / 2)
        medium_button = Button(medium_x, medium_y, self.MEDIUM_BUTTON)
        easy_button = Button(medium_x - 300, medium_y, self.EASY_BUTTON)
        hard_button = Button(medium_x + 360, medium_y, self.HARD_BUTTON)

        while options_are_open:
            self.WINDOW.blit(self.GAME_BACKGROUND, (0, 0))
            options_label = self.font.render("OPTIONS", 1, (255, 255, 255))
            self.WINDOW.blit(options_label, (self.WIDTH / 2 - options_label.get_width() / 2, 50))
            easy_button.draw(self.WINDOW)
            medium_button.draw(self.WINDOW)
            hard_button.draw(self.WINDOW)
            pygame.display.update()

            for event in pygame.event.get():
                if easy_button.clicked():
                    options_are_open = False
                    return "Easy"
                if medium_button.clicked():
                    self.lives = 3
                    self.enemy_velocity = 2
                    self.enemy_laser_velocity = 6
                    options_are_open = False
                    return "Medium"
                if hard_button.clicked():
                    self.lives = 4
                    self.enemy_velocity = 2
                    self.enemy_laser_velocity = 6
                    self.velocity_of_ship = 7
                    self.player_damage = 50
                    options_are_open = False
                    return "Hard"
                if event.type == pygame.QUIT:
                    options_are_open = False

    def scores(self):
        scores_are_open = True
        back_button = Button((self.WIDTH / 2 - self.BACK_BUTTON.get_width() / 2), self.HEIGHT - 170, self.BACK_BUTTON)
        scores_label = self.font.render(f"{self.player.username} scores", 1, (255, 255, 255))

        def check_scores(self):
            path = Path('Scores.json')
            try:
                file = path.open('r')
                scores = json.load(file)
                if f"{self.player.username}" in scores:
                    self.player_scores = scores[self.player.username]
                    return True
                else:
                    return False
            except FileNotFoundError:
                return False

        while scores_are_open:
            self.WINDOW.blit(self.GAME_BACKGROUND, (0, 0))
            back_button.draw(self.WINDOW)
            self.WINDOW.blit(scores_label, (self.WIDTH / 2 - scores_label.get_width() / 2, 50))
            if check_scores(self):
                labels_height = 200
                for x in self.player_scores["Difficulty"]:
                    difficulty_label = self.font.render(f"Difficulty: {x[0]}", 1, (255, 255, 255))
                    self.WINDOW.blit(difficulty_label,
                                     (self.WIDTH / 2 - difficulty_label.get_width() / 2, labels_height))
                    labels_height += 80
                    level_label = self.font.render(f"Level: {x[1]}", 1, (255, 255, 255))
                    self.WINDOW.blit(level_label,
                                     (self.WIDTH / 2 - level_label.get_width() / 2, labels_height))
                    labels_height += 150
            pygame.display.update()

            for event in pygame.event.get():
                if back_button.clicked():
                    scores_are_open = False
                if event.type == pygame.QUIT:
                    scores_are_open = False

    def guide(self):
        guide_is_open = True
        back_button = Button((self.WIDTH / 2 - self.BACK_BUTTON.get_width() / 2), self.HEIGHT - 170, self.BACK_BUTTON)
        guide_label = self.font.render("GUIDE", 1, (255, 255, 255))
        rules_font = pygame.font.Font(os.path.join("font", "GameSansSerif7-oPGx.ttf"), 20)
        rule_1_label = rules_font.render("1. To use the play/options/scores features, you must first enter a username.", 1, (255, 255, 255))
        rule_2_label = rules_font.render("The username must contain 4 to 15 characters, including 1 uppercase letter, and cannot contain special characters.", 1,(255, 255, 255))
        rule_3_label = rules_font.render("2. To change the difficulty level, click on the options button.", 1, (255, 255, 255))
        rule_4_label = rules_font.render("Easy - monsters are slow, can be defeated with a single laser hit, player has 4 lives.", 1, (255, 255, 255))
        rule_5_label = rules_font.render("Medium - monsters are faster, can be defeated with a single laser hit, player has 3 lives.", 1, (255, 255, 255))
        rule_6_label = rules_font.render("Hard - monsters are faster, can be defeated with two laser hits, player is also faster and has 4 lives.", 1, (255, 255, 255))
        rule_7_label = rules_font.render("3. To start the gameplay, press the play button.", 1, (255, 255, 255))
        rule_8_label = rules_font.render("The game involves shooting down incoming monsters. After defeating all the monsters, the level and", 1, (255, 255, 255))
        rule_9_label = rules_font.render("the number of monsters appearing in the next wave increase. The player loses health if they collide", 1, (255, 255, 255))
        rule_10_label = rules_font.render("with a monster or get hit by its laser.The player loses the game when their spaceship's health bar", 1, (255, 255, 255))
        rule_11_label = rules_font.render("is depleted or when a specific number of monsters reach the bottom of the screen. The information", 1, (255, 255, 255))
        rule_12_label = rules_font.render("about how many monsters can reach the end of the screen is displayed in the top right corner", 1, (255, 255, 255))
        rule_13_label = rules_font.render("and is called lives. You can move the spaceship using the W, S, A, D keys.", 1, (255, 255, 255))
        rule_14_label = rules_font.render("4. To see the best scores achieved, click the scores button.", 1, (255, 255, 255))

        while guide_is_open:
            self.WINDOW.blit(self.GAME_BACKGROUND, (0, 0))
            self.WINDOW.blit(guide_label, (self.WIDTH / 2 - guide_label.get_width() / 2, 50))
            self.WINDOW.blit(rule_1_label, (self.WIDTH / 2 - rule_1_label.get_width() / 2, 150))
            self.WINDOW.blit(rule_2_label, (self.WIDTH / 2 - rule_2_label.get_width() / 2, 190))
            self.WINDOW.blit(rule_3_label, (self.WIDTH / 2 - rule_3_label.get_width() / 2, 265))
            self.WINDOW.blit(rule_4_label, (self.WIDTH / 2 - rule_4_label.get_width() / 2, 305))
            self.WINDOW.blit(rule_5_label, (self.WIDTH / 2 - rule_5_label.get_width() / 2, 345))
            self.WINDOW.blit(rule_6_label, (self.WIDTH / 2 - rule_6_label.get_width() / 2, 385))
            self.WINDOW.blit(rule_7_label, (self.WIDTH / 2 - rule_7_label.get_width() / 2, 460))
            self.WINDOW.blit(rule_8_label, (self.WIDTH / 2 - rule_8_label.get_width() / 2, 500))
            self.WINDOW.blit(rule_9_label, (self.WIDTH / 2 - rule_9_label.get_width() / 2, 540))
            self.WINDOW.blit(rule_10_label, (self.WIDTH / 2 - rule_10_label.get_width() / 2, 580))
            self.WINDOW.blit(rule_11_label, (self.WIDTH / 2 - rule_11_label.get_width() / 2, 620))
            self.WINDOW.blit(rule_12_label, (self.WIDTH / 2 - rule_12_label.get_width() / 2, 660))
            self.WINDOW.blit(rule_13_label, (self.WIDTH / 2 - rule_13_label.get_width() / 2, 700))
            self.WINDOW.blit(rule_14_label, (self.WIDTH / 2 - rule_14_label.get_width() / 2, 775))
            back_button.draw(self.WINDOW)
            pygame.display.update()

            for event in pygame.event.get():
                if back_button.clicked():
                    guide_is_open = False
                if event.type == pygame.QUIT:
                    guide_is_open = False
