import pygame
import sys
import random
from collections import deque
import heapq
import math
import os


class Help:
    def __init__(self):
        self.sounds = {}
        self.images = {}
        self.fonts = {}
        self.load_all()

    def load_all(self):
        self.load_sound("coin", "Coin sound.mp3")
        self.load_sound("chest", "Chest sound.mp3")
        self.load_sound("damage", "Damage sound.mp3")
        self.load_sound("laser", "Laser.mp3")
        self.load_sound("step", "Step.mp3")
        self.load_sound("book", "Book.mp3")
        self.load_sound("key", "Key.mp3")
        self.load_sound("game_music", "Game music.mp3")
        self.load_sound("menu_music", "Menu music.mp3")
        self.load_sound("win_music", "Winning music.ogg")
        self.load_sound("game_over_music", "Game over music.mp3")

        self.load_image("bg_menu", "BG menu.png")
        self.load_image("bg_treasure", "Treasure.png")
        self.load_image("bg_win", "Winning BG.png")
        self.load_image("button_menu", "Button menu.png")
        self.load_image("heart", "Heart.png")

        for i in range(8):
            self.load_image(f"wall{i}", f"Wall {i}.png")

        self.load_image("tile", "tile.png")
        self.load_image("coin1", "Coin 1.png")
        self.load_image("coin2", "Coin 2.png")
        self.load_image("eye", "Eye 1.png")

        for i in range(1, 10):
            self.load_image(f"spike{i}", f"newspike {i}.png")

        self.load_image("golem_s", "Golem 1.png")
        self.load_image("golem_right1", "Golem 10.png")
        self.load_image("golem_right2", "Golem 11.png")
        self.load_image("golem_left1", "Golem 8.png")
        self.load_image("golem_left2", "Golem 9.png")
        self.load_image("golem_down1", "Golem 2.png")
        self.load_image("golem_down2", "Golem 3.png")
        self.load_image("golem_up1", "Golem 12.png")
        self.load_image("golem_up2", "Golem 13.png")

        for i in range(1, 13):
            self.load_image(f"key{i}", f"Key {i}.png")

        for i in range(1, 13):
            self.load_image(f"chest{i}", f"Chest {i}.png")
            self.load_image(f"chest{i}_open", f"Chest {i} open.png")

        self.frames_golem_over = []
        for i in range(1, 21):
            frame = pygame.image.load(f"Golem Over {i}.png")
            frame = pygame.transform.scale(frame, (700 + 300, 700))
            self.frames_golem_over.append(frame)

        self.load_font("menu_title", "Jacquard12-Regular.ttf", 87)
        self.load_font("menu_button", "Jacquard12-Regular.ttf", 48)
        self.load_font("menu_guide", "Jacquard12-Regular.ttf", 30)
        self.load_font("game_ui", "Jacquard12-Regular.ttf", 36)
        self.load_font("powerup_title", "Jacquard12-Regular.ttf", 58)
        self.load_font("win_title", "Jacquard12-Regular.ttf", 90)

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def load_image(self, name, path):
        self.images[name] = pygame.image.load(path)

    def load_font(self, name, path, size):
        self.fonts[name] = pygame.font.Font(path, size)

    def get_sound(self, name):
        return self.sounds.get(name)

    def get_image(self, name):
        return self.images.get(name)

    def get_font(self, name):
        return self.fonts.get(name)


class Button:
    def __init__(self, x, y, width, height, text, font, image, scale=1.0):
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.font = font
        self.scale = scale

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Player:
    def __init__(self, x, y, size, helper):
        self.x = x
        self.y = y
        self.size = size
        self.direction = "s"
        self.frame = 0
        self.move = False
        self.time = 0
        self.timed = 10
        self.max_HP = 1
        self.HP_count = self.max_HP
        self.coins_count = 0
        self.key_collected = False
        self.on_spike = False
        self.on_enemy = False
        self.helper = helper

        self.animations = {
            "s": helper.get_image("golem_s"),
            "right": [
                helper.get_image("golem_right1"),
                helper.get_image("golem_right2")
            ],
            "left": [
                helper.get_image("golem_left1"),
                helper.get_image("golem_left2")
            ],
            "up": [
                helper.get_image("golem_up1"),
                helper.get_image("golem_up2")
            ],
            "down": [
                helper.get_image("golem_down1"),
                helper.get_image("golem_down2")
            ]
        }

        for key in self.animations:
            if isinstance(self.animations[key], list):
                self.animations[key] = [pygame.transform.scale(img, (size, size)) for img in self.animations[key]]
            else:
                self.animations[key] = pygame.transform.scale(self.animations[key], (size, size))

    def move_player(self, dx, dy, direction):
        self.x += dx
        self.y += dy
        self.direction = direction
        self.move = True
        self.time = self.timed
        self.helper.get_sound("step").play()

    def update(self):
        if self.move or self.time > 0:
            if self.move:
                self.frame += 1
                if self.frame >= 4:
                    self.frame = 0
            if not self.move:
                self.time -= 1

    def draw(self, screen):
        if self.HP_count > 0:
            if self.move or self.time > 0:
                if self.direction == "r":
                    screen.blit(self.animations["right"][(self.frame // 2) % len(self.animations["right"])], (self.y * self.size, self.x * self.size))
                elif self.direction == "l":
                    screen.blit(self.animations["left"][(self.frame // 2) % len(self.animations["left"])], (self.y * self.size, self.x * self.size))
                elif self.direction == "u":
                    screen.blit(self.animations["up"][(self.frame // 2) % len(self.animations["up"])], (self.y * self.size, self.x * self.size))
                elif self.direction == "d":
                    screen.blit(self.animations["down"][(self.frame // 2) % len(self.animations["down"])], (self.y * self.size, self.x * self.size))
            else:
                screen.blit(self.animations["s"], (self.y * self.size, self.x * self.size))


class Enemy:
    def __init__(self, x, y, size, helper):
        self.x = x
        self.y = y
        self.size = size
        self.path = []
        self.count = 0
        self.direction = "s"
        self.speed = 5
        self.helper = helper
        self.eye_image = pygame.transform.scale(helper.get_image("eye"), (size, size))

    def update(self, player_x, player_y, maze):
        self.count += 1
        if self.count >= self.speed:
            if not self.path:
                self.path = self.deikstra((self.x, self.y), (player_x, player_y), maze)
            else:
                new = self.path.pop(0)
                if new[0] > self.x:
                    self.direction = "d"
                elif new[0] < self.x:
                    self.direction = "u"
                elif new[1] > self.y:
                    self.direction = "r"
                elif new[1] < self.y:
                    self.direction = "l"
                self.x, self.y = new[0], new[1]
            self.count = 0

    def draw(self, screen):
        rotated_eye = self.eye_image
        if self.direction == "u":
            rotated_eye = pygame.transform.rotate(self.eye_image, 0)
        elif self.direction == "d":
            rotated_eye = pygame.transform.rotate(self.eye_image, 180)
        elif self.direction == "l":
            rotated_eye = pygame.transform.rotate(self.eye_image, 90)
        elif self.direction == "r":
            rotated_eye = pygame.transform.rotate(self.eye_image, -90)
        screen.blit(rotated_eye, (self.y * self.size, self.x * self.size))

    def deikstra(self, start, goal, grid):
        queue = []
        heapq.heappush(queue, (0, start))
        fromd = {}
        cost = {start: 0}

        while queue:
            current = heapq.heappop(queue)[1]

            if current == goal:
                path = []
                node = goal
                while node != start:
                    path.append(node)
                    node = fromd[node]
                path.append(start)
                path.reverse()
                return path

            x, y = current
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
                    neighbors.append((nx, ny))

            for neighbor in neighbors:
                ncost = cost[current] + 1
                if neighbor not in cost or ncost < cost[neighbor]:
                    cost[neighbor] = ncost
                    priority = ncost
                    heapq.heappush(queue, (priority, neighbor))
                    fromd[neighbor] = current

        return []


class Labyrynth:
    def __init__(self, width, height, size, helper):
        self.width = width
        self.height = height
        self.size = size
        self.helper = helper
        self.matrix = [[1 for _ in range(width)] for _ in range(height)]
        self.walls = [helper.get_image(f"wall{i}") for i in range(8)]
        self.random_wall = random.choice(self.walls)
        self.random_wall = pygame.transform.scale(self.random_wall, (size, size))
        self.tile = pygame.transform.scale(helper.get_image("tile"), (size, size))
        self.generate_maze(1, 0)

    def generate_maze(self, x, y):
        stack = [(x, y)]
        self.matrix[x][y] = 0
        while stack:
            cx, cy = stack[-1]
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and self.matrix[nx][ny] == 1:
                    self.matrix[nx][ny] = 0
                    self.matrix[cx + dx // 2][cy + dy // 2] = 0
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

    def draw(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.matrix[row][col] == 0:
                    screen.blit(self.tile, (col * self.size, row * self.size))
                elif self.matrix[row][col] == 1:
                    screen.blit(self.random_wall, (col * self.size, row * self.size))


class Room:
    def __init__(self, width, height, size, room_num, helper):
        self.width = width
        self.height = height
        self.size = size
        self.room_num = room_num
        self.helper = helper
        self.maze = Labyrynth(width, height, size, helper)
        self.coins = []
        self.spikes = []
        self.enemies = []
        self.exit_x = None
        self.exit_y = None
        self.key_x = None
        self.key_y = None
        self.heart_x = -1
        self.heart_y = -1
        self.key_collected = False
        self.rotate_count = 0
        self.curr_spike = 0

        self.coins_num = 1 + (room_num // 2)
        self.spikes_num = room_num // 2
        self.enemies_num = room_num // 4

        self.random_coin = random.choice([
            helper.get_image("coin1"),
            helper.get_image("coin2")
        ])
        self.random_coin = pygame.transform.scale(self.random_coin, (size, size))

        self.spikes_img = [
            pygame.transform.scale(helper.get_image(f"spike{i}"), (size + 10, size + 10))
            for i in range(1, 10)
        ]

        self.random_key = random.choice([
            helper.get_image(f"key{i}") for i in range(1, 13)
        ])
        self.random_key = pygame.transform.scale(self.random_key, (size, size))

        self.heart_img = pygame.transform.scale(helper.get_image("heart"), (size, size))

        chest_pair = random.choice([
            [f"chest{i}", f"chest{i}_open"] for i in range(1, 13)
        ])
        self.random_chest = pygame.transform.scale(
            helper.get_image(chest_pair[0]), (size, size))
        self.random_chest_open = pygame.transform.scale(
            helper.get_image(chest_pair[1]), (size, size))

        self.new_room()

    def new_room(self):
        exits = []
        for i in range(1, self.height - 1):
            if self.maze.matrix[i][self.width - 2] == 0:
                exits.append(i)

        self.exit_x = random.choice(exits) if exits else random.randint(1, self.height - 2)
        self.exit_y = self.width - 1
        self.maze.matrix[self.exit_x][self.exit_y] = 0
        self.maze.matrix[self.exit_x][self.exit_y - 1] = 0

        self.coins = []
        for i in range(self.coins_num):
            while True:
                x, y = random.randint(1, self.height - 2), random.randint(1, self.width - 2)
                if self.maze.matrix[x][y] == 0 and (x, y) not in self.coins:
                    self.coins.append((x, y))
                    break

        self.spikes = []
        for i in range(self.spikes_num):
            while True:
                x, y = random.randint(1, self.height - 2), random.randint(1, self.width - 2)
                if (self.maze.matrix[x][y] == 0 and (x, y) not in self.spikes and
                        (x, y) not in self.coins):
                    self.spikes.append((x, y))
                    break

        while True:
            x, y = random.randint(1, self.height - 2), random.randint(1, self.width - 2)
            if (self.maze.matrix[x][y] == 0 and (x, y) not in self.spikes and
                    (x, y) not in self.coins):
                self.key_x, self.key_y = x, y
                break

        if random.randint(1, 10) == 1:
            while True:
                x, y = random.randint(1, self.height - 2), random.randint(1, self.width - 2)
                if (self.maze.matrix[x][y] == 0 and (x, y) not in self.spikes and
                        (x, y) not in self.coins and (x, y) != (self.key_x, self.key_y)):
                    self.heart_x, self.heart_y = x, y
                    break

        self.enemies = []
        for i in range(self.enemies_num):
            while True:
                x, y = random.randint(1, self.height - 2), random.randint(1, self.width - 2)
                if self.maze.matrix[x][y] == 0:
                    self.enemies.append(Enemy(x, y, self.size, self.helper))
                    break

    def draw(self, screen):
        self.maze.draw(screen)

        for x, y in self.coins:
            screen.blit(self.random_coin, (y * self.size, x * self.size))

        self.rotate_count += 1
        if self.rotate_count >= 5:
            self.curr_spike = (self.curr_spike + 1) % len(self.spikes_img)
            self.rotate_count = 0

        for x, y in self.spikes:
            rect = pygame.Rect(y * (self.size - 1.1), x * (self.size - 0.6), self.size + 10, self.size + 10)
            screen.blit(self.spikes_img[self.curr_spike], rect.topleft)

        if not self.key_collected and self.key_x is not None and self.key_y is not None:
            screen.blit(self.random_key, (self.key_y * self.size, self.key_x * self.size))

        if self.heart_x != -1 and self.heart_y != -1:
            screen.blit(self.heart_img, (self.heart_y * self.size, self.heart_x * self.size))

        for enemy in self.enemies:
            enemy.draw(screen)

        if self.key_collected:
            screen.blit(self.random_chest_open, (self.exit_y * self.size, self.exit_x * self.size))
        else:
            screen.blit(self.random_chest, (self.exit_y * self.size, self.exit_x * self.size))


class Game:
    def __init__(self, width, height, helper):
        self.width = width
        self.height = height
        self.helper = helper
        self.divisors = [10, 14, 20, 25, 28, 35, 50, 70, 100]
        self.div = 0
        self.r = self.divisors[self.div]
        self.c = self.r
        self.size = width // self.c
        self.screen = pygame.display.set_mode((width + 300, height))
        pygame.display.set_caption("GOLEM rush")
        self.clock = pygame.time.Clock()

        self.room_num = 1
        self.player = Player(1, 0, self.size, helper)
        self.current_room = Room(self.r, self.c, self.size, self.room_num, helper)

        self.max_HP = 1
        self.boost_coins = 0
        self.boost_damage = 0
        self.rebirth = False
        self.immunity = False
        self.immune_room = -1
        self.destroy_column = 0
        self.destroy_row = 0
        self.win = False

        self.powerups = ["Heal HP", "Coins boost", "More Coins", "Slower enemie", "Less Damage", "Rebirth", "Immunity", "Destroy Column (K1)", "Destroy Row (K2)"]

        pygame.mixer.music.stop()
        self.helper.get_sound("game_music").play(loops=-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if (event.key == pygame.K_UP and
                        self.current_room.maze.matrix[self.player.x - 1][self.player.y] == 0 and
                        self.player.HP_count > 0):
                    self.player.move_player(-1, 0, "u")
                elif (event.key == pygame.K_DOWN and
                      self.current_room.maze.matrix[self.player.x + 1][self.player.y] == 0 and
                      self.player.HP_count > 0):
                    self.player.move_player(1, 0, "d")
                elif (event.key == pygame.K_LEFT and
                      self.current_room.maze.matrix[self.player.x][self.player.y - 1] == 0 and
                      self.player.HP_count > 0):
                    self.player.move_player(0, -1, "l")
                elif (event.key == pygame.K_RIGHT and
                      self.current_room.maze.matrix[self.player.x][self.player.y + 1] == 0 and
                      self.player.HP_count > 0):
                    self.player.move_player(0, 1, "r")

                elif event.key == pygame.K_1 and self.destroy_column > 0:
                    for i in range(self.r):
                        self.current_room.maze.matrix[i][self.player.y] = 0
                    self.destroy_column -= 1
                    self.helper.get_sound("laser").play()
                elif event.key == pygame.K_2 and self.destroy_row > 0:
                    for i in range(self.c):
                        self.current_room.maze.matrix[self.player.x][i] = 0
                    self.destroy_row -= 1
                    self.helper.get_sound("laser").play()

        return True

    def update(self):
        self.player.update()

        for enemy in self.current_room.enemies:
            enemy.update(self.player.x, self.player.y, self.current_room.maze.matrix)

        for coin in self.current_room.coins[:]:
            if self.player.x == coin[0] and self.player.y == coin[1]:
                self.current_room.coins.remove(coin)
                self.player.coins_count += 1 + self.boost_coins
                self.helper.get_sound("coin").play()

        if (self.player.x == self.current_room.heart_x and self.player.y == self.current_room.heart_y):
            self.player.HP_count = self.max_HP
            self.current_room.heart_x, self.current_room.heart_y = -1, -1

        if (not self.current_room.key_collected and self.player.x == self.current_room.key_x and self.player.y == self.current_room.key_y):
            self.current_room.key_collected = True
            self.player.key_collected = True
            self.helper.get_sound("key").play()

        for spike in self.current_room.spikes:
            if (self.player.x == spike[0] and self.player.y == spike[1] and not self.player.on_spike and not (self.immunity and self.room_num >= self.immune_room)):
                self.player.HP_count -= 1 + self.boost_damage
                self.helper.get_sound("damage").play()
                self.player.on_spike = True
            elif self.player.x != spike[0] or self.player.y != spike[1]:
                self.player.on_spike = False

        for enemy in self.current_room.enemies:
            if (self.player.x == enemy.x and self.player.y == enemy.y and not self.player.on_enemy and not (self.immunity and self.room_num >= self.immune_room)):
                self.player.HP_count -= 1 + self.boost_damage
                self.helper.get_sound("damage").play()
                self.player.on_enemy = True
            elif self.player.x != enemy.x or self.player.y != enemy.y:
                self.player.on_enemy = False

        if (self.player.x == self.current_room.exit_x and self.player.y == self.current_room.exit_y):

            if self.player.key_collected and self.player.coins_count >= 1:
                self.powerup()
                self.player.coins_count -= 1

            self.room_num += 1
            self.player.key_collected = False

            if self.room_num == 15:
                self.win = True
                return

            if self.room_num in [3, 5, 7, 10, 13]:
                self.div += 1

            self.r = self.divisors[self.div]
            self.c = self.r
            self.size = self.width // self.c

            self.player.size = self.size
            for key in self.player.animations:
                if isinstance(self.player.animations[key], list):
                    self.player.animations[key] = [pygame.transform.scale(img, (self.size, self.size)) for img in self.player.animations[key]]
                else:
                    self.player.animations[key] = pygame.transform.scale(self.player.animations[key], (self.size, self.size))

            self.player.x, self.player.y = 1, 0

            self.current_room = Room(self.r, self.c, self.size, self.room_num, self.helper)

            if self.player.HP_count <= 0 and self.rebirth:
                self.player.HP_count = self.max_HP // 5
                self.rebirth = False

            if self.immunity and self.room_num >= self.immune_room:
                self.immunity = False
                self.immune_room = -1

    def powerup(self):
        pygame.mixer.music.pause()
        self.helper.get_sound("chest").play()
        pygame.mixer.music.unpause()
        random_powerups = random.sample(self.powerups, 2)

        button_width, button_height = 320, 130
        powerup1_button = Button(self.width // 2, self.height // 2 - 100, button_width, button_height, random_powerups[0], self.helper.get_font("game_ui"), self.helper.get_image("button_menu"),1.0)

        powerup2_button = Button(self.width // 2, self.height // 2 + 50, button_width, button_height, random_powerups[1], self.helper.get_font("game_ui"), self.helper.get_image("button_menu"), 1.0)

        powerup3_button = Button(self.width // 2, self.height // 2 + 200, button_width, button_height, "Heal 1 HP", self.helper.get_font("game_ui"), self.helper.get_image("button_menu"), 1.0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if powerup1_button.is_clicked(event.pos):
                        self.poweruphelp(random_powerups[0])
                        return
                    elif powerup2_button.is_clicked(event.pos):
                        self.poweruphelp(random_powerups[1])
                        return
                    elif powerup3_button.is_clicked(event.pos):
                        self.poweruphelp("Heal 1 HP")
                        return

            bg = pygame.transform.scale(self.helper.get_image("bg_treasure"), (self.width + 300, self.height))
            self.screen.blit(bg, (0, 0))

            title_font = self.helper.get_font("powerup_title")
            title_text = title_font.render("Choose a Powerup!", True, (255, 255, 255))
            self.screen.blit(title_text, (self.width // 2 - 70, 50))

            subtitle_font = self.helper.get_font("game_ui")
            subtitle_text = subtitle_font.render("(costs 1 coin)", True, (255, 255, 255))
            self.screen.blit(subtitle_text, (self.width // 2 + 50, 110))

            powerup1_button.draw(self.screen)
            powerup2_button.draw(self.screen)
            powerup3_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

    def poweruphelp(self, powerup):
        if powerup == "More Coins":
            self.current_room.coins_num += 1
        elif powerup == "Slower enemie":
            for enemy in self.current_room.enemies:
                enemy.speed += 2
        elif powerup == "Coins boost":
            self.boost_coins += 0.5
        elif powerup == "Heal HP":
            if self.player.HP_count == self.max_HP:
                self.max_HP += 2
                self.player.HP_count += 2
            else:
                self.player.HP_count = self.max_HP
        elif powerup == "Less Damage":
            self.boost_damage += 0.1
        elif powerup == "Rebirth":
            self.rebirth = True
        elif powerup == "Heal 1 HP":
            if self.player.HP_count < self.max_HP:
                self.player.HP_count += 1
        elif powerup == "Immunity":
            self.immunity = True
            self.immune_room = self.room_num + 1
        elif powerup == "Destroy Column (K1)":
            self.destroy_column += 1
        elif powerup == "Destroy Row (K2)":
            self.destroy_row += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.current_room.draw(self.screen)
        self.player.draw(self.screen)

        pygame.draw.rect(self.screen, (255, 255, 255), (self.width, 0, 300, self.height))

        font = self.helper.get_font("game_ui")
        room_text = font.render(f"Room {self.room_num}", True, (0, 0, 0))
        coins_text = font.render(f"Coins: {self.player.coins_count}", True, (0, 0, 0))
        hp_text = font.render(f"HP: {self.player.HP_count}", True, (0, 0, 0))

        self.screen.blit(room_text, (self.width + 10, 10))
        self.screen.blit(coins_text, (self.width + 10, 50))
        self.screen.blit(hp_text, (self.width + 10, 90))

        if self.player.key_collected:
            key_text = font.render("Key Collected!", True, (0, 0, 0))
            self.screen.blit(key_text, (self.width + 10, 130))
        pygame.display.flip()

    def gameover(self):
        self.helper.get_sound("game_music").stop()
        score = max(0, int(self.player.coins_count - (15 - self.room_num) // 2))
        with open("Best Score.txt", "r") as file:
            best_score = int(file.read())

        if score > best_score:
            with open("Best Score.txt", "w") as file:
                file.write(str(score))
            best_score = score

        pygame.mixer.music.stop()
        self.helper.get_sound("game_over_music").play(loops=-1)

        title_font = self.helper.get_font("win_title")
        title_text = title_font.render("You Win!", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2, self.height // 2 - 10))

        curr_frame = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__init__(self.width, self.height, self.helper)
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()

            self.screen.fill((0, 0, 0))

            frame = self.helper.frames_golem_over[curr_frame]
            self.screen.blit(frame, (0, 0))
            curr_frame = (curr_frame + 1) % len(self.helper.frames_golem_over)

            black = (0, 0, 0)
            white = (255, 255, 255)

            font = pygame.font.Font("Jacquard12-Regular.ttf", 90)
            text1 = font.render("Game", True, black)
            text2 = font.render("Over", True, black)
            self.screen.blit(text1, (self.width // 2 + 220, 80))
            self.screen.blit(text2, (self.width // 2 + 220, 150))

            font2 = pygame.font.Font("Jacquard12-Regular.ttf", 36)
            text2 = font2.render("press ENTER to restart", True, white)
            text_rect2 = text2.get_rect(center=(self.width // 2 + 110, self.height // 2 + 280))
            self.screen.blit(text2, text_rect2)

            font3 = pygame.font.Font("Jacquard12-Regular.ttf", 36)
            text3 = font3.render("press ESC to quit", True, white)
            text_rect3 = text3.get_rect(center=(self.width // 2 + 110, self.height // 2 + 310))
            self.screen.blit(text3, text_rect3)

            font4 = pygame.font.Font("Jacquard12-Regular.ttf", 30)
            text4 = font4.render(f"Score: {score}", True, white)
            text_rect4 = text4.get_rect(center=(50, self.height // 2 + 280))
            self.screen.blit(text4, text_rect4)

            font5 = pygame.font.Font("Jacquard12-Regular.ttf", 30)
            text5 = font5.render(f"Best Score: {best_score}", True, white)
            text_rect5 = text5.get_rect(center=(80, self.height // 2 + 310))
            self.screen.blit(text5, text_rect5)

            pygame.display.flip()
            self.clock.tick(10)

        return False

    def win_scr(self):
        self.helper.get_sound("game_music").stop()
        try:
            with open("Best Score.txt", "r") as file:
                best_score = int(file.read())
        except:
            best_score = 0

        if self.player.coins_count > best_score:
            with open("Best Score.txt", "w") as file:
                file.write(str(self.player.coins_count))
            best_score = self.player.coins_count

        pygame.mixer.music.stop()
        self.helper.get_sound("win_music").play(loops=-1)

        color_time = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
            r = int((math.sin(color_time / 100) + 1) * 127.5)
            g = int((math.sin(color_time / 100 + 2 * math.pi / 3) + 1) * 127.5)
            b = int((math.sin(color_time / 100 + 4 * math.pi / 3) + 1) * 127.5)
            color = (r, g, b)
            color_time += 1

            self.screen.blit(
                pygame.transform.scale(self.helper.get_image("bg_win"),
                                       (self.width + 300, self.height)),
                (0, 0))

            title_font = self.helper.get_font("win_title")
            title_text = title_font.render("You Win!", True, color)
            self.screen.blit(title_text, (self.width // 2, self.height // 2 - 10))

            score_font = self.helper.get_font("powerup_title")
            score_text = score_font.render(f"Score: {self.player.coins_count}", True, (255 - r, 255 - g, 255 - b))
            best_text = score_font.render(f"Best Score: {best_score}", True, (255 - r, 255 - g, 255 - b))

            self.screen.blit(score_text, (self.width // 2 + 80, self.height // 2 + 70))
            self.screen.blit(best_text, (self.width // 2, self.height // 2 + 130))

            font = self.helper.get_font("game_ui")
            instruction = font.render("press ESC to quit", True, (255, 255, 255))
            self.screen.blit(instruction, (self.width // 2 + 50, self.height // 2 + 310))

            pygame.display.flip()
            self.clock.tick(60)

        return False

    def run(self):
        running = True

        while running:
            running = self.handle_events()

            if not self.win and self.player.HP_count > 0:
                self.update()
            elif self.player.HP_count <= 0:
                if self.gameover():
                    continue
                else:
                    break
            elif self.win:
                self.win_scr()
                break

            self.draw()
            self.clock.tick(30)


class Menu:
    def __init__(self, width, height, helper):
        self.width = width
        self.height = height
        self.helper = helper
        self.screen = pygame.display.set_mode((width + 300, height))
        pygame.display.set_caption("GOLEM rush")
        self.clock = pygame.time.Clock()
        self.guide = False
        self.text_y = 60
        self.direction = -1
        self.frame_count = 0
        self.animation_speed = 20

        try:
            with open("Best Score.txt", "r") as file:
                self.best_score = int(file.read())
        except:
            self.best_score = 0

        button_width, button_height = 180, 95
        self.start_button = Button(
            width // 2 + 130 - button_width // 2,
            height // 2 - 50 - button_height // 2,
            button_width, button_height,
            "Start",
            self.helper.get_font("menu_button"),
            self.helper.get_image("button_menu")
        )

        self.guide_button = Button(
            width // 2 + 130 - button_width // 2,
            height // 2 + 50 - button_height // 2,
            button_width, button_height,
            "Guide",
            self.helper.get_font("menu_button"),
            self.helper.get_image("button_menu")
        )

        self.helper.get_sound("menu_music").play(loops=-1)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_clicked(event.pos):
                        self.helper.get_sound("book").play()
                        pygame.mixer.music.stop()
                        self.helper.get_sound("menu_music").stop()
                        self.helper.get_sound("game_over_music").stop()
                        return True
                    elif self.guide_button.is_clicked(event.pos):
                        self.helper.get_sound("book").play()
                        self.guide = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.helper.get_sound("book").play()
                        self.guide = False

            self.frame_count += 1
            if self.frame_count % self.animation_speed == 0:
                self.text_y += 10 * self.direction
                if self.text_y <= 50:
                    self.direction = 1
                elif self.text_y >= 60:
                    self.direction = -1

            self.draw()

            self.clock.tick(30)

        return False

    def draw(self):
        bg_image = self.helper.get_image("bg_menu")
        scaled_bg = pygame.transform.scale(bg_image, (self.width + 300, self.height))
        self.screen.blit(scaled_bg, (0, 0))

        if self.guide:
            font = self.helper.get_font("menu_guide")
            guide_text = [
                "You are a golem. ",
                "Your goal is to reach the end of the dungeon.",
                "There will be many rooms with ",
                "obstacles and coins     on your way, and",
                "at the end there wil     be a   chest with a power-up that can",
                "be obtained for                     the   collected key.",
                "GOOD luck!"
            ]

            for i, line in enumerate(guide_text):
                text = font.render(line, True, (0, 0, 0))
                self.screen.blit(text, (105, 40 + i * 40))
        else:
            font = self.helper.get_font("menu_title")
            title_text = font.render("GOLEM rush", True, (0, 0, 0))
            self.screen.blit(
                title_text,
                ((self.width // 2) - 20 - title_text.get_width() // 2, self.text_y))

            self.start_button.draw(self.screen)
            self.guide_button.draw(self.screen)

            font_score = self.helper.get_font("menu_guide")
            best_score_text = font_score.render(
                f"Best Score: {self.best_score}", True, (255, 255, 255))
            self.screen.blit(best_score_text, (20, self.height - 50))

        pygame.display.flip()


def main():
    pygame.init()
    width, height = 700, 700

    helper = Help()

    menu = Menu(width, height, helper)
    if menu.run():
        game = Game(width, height, helper)
        game.run()

    pygame.quit()
    sys.exit()

main()
