import pygame
import sys
import random
from collections import deque
import heapq
import os
import math

pygame.init()

# DFS со стеком для создания лабиринта
def labyrynth(x, y):
    stack = [(x, y)]
    matrix[x][y] = white
    while stack:
        cx, cy = stack[-1]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < r - 1 and 1 <= ny < c - 1 and matrix[nx][ny] == gray:
                matrix[nx][ny] = white
                matrix[cx + dx // 2][cy + dy // 2] = white
                stack.append((nx, ny))
                break
        else:
            stack.pop()

# BFS для проверки выхода
def exit_possible(startx, starty, exitx, exity):
    visited = [[False] * c for i in range(r)]
    queue = deque([(startx, starty)])
    visited[startx][starty] = True

    while queue:
        x, y = queue.popleft()
        if x == exitx and y == exity:
            return True
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and not visited[nx][ny] and matrix[nx][ny] == white:
                visited[nx][ny] = True
                queue.append((nx, ny))
    return False

# Дейкстра для врага
def deikstra(start, goal, grid):
    queue = []
    heapq.heappush(queue, (0, start))
    fromp = {}
    cost = {start: 0}

    while queue:
        curr = heapq.heappop(queue)[1]

        if curr == goal:
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = fromp[node]
            path.append(start)
            path.reverse()
            return path

        x, y = curr
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and grid[nx][ny] != gray:
                neighbors.append((nx, ny))

        for neighbor in neighbors:
            ncost = cost[curr] + 1
            if neighbor not in cost or ncost < cost[neighbor]:
                cost[neighbor] = ncost
                priority = ncost
                heapq.heappush(queue, (priority, neighbor))
                fromp[neighbor] = curr

    return []

def newRoom(startx, starty, size, coinsnum, spikesnum, enemiesnum):
    global playerx, playery, matrix, coins, spikes, enemies, coins_count, HP_count, exitx, exity, random_wall, random_coin, golems, golemd1, golemd2, golemu1, golemu2, golemr1, golemr2, goleml1, goleml2, golemr, goleml, golemd, golemu, spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9, spikes_img, eye, keyx, keyy, random_key, key_collected, random_chest, random_chest_open, heart, heartx, hearty
    playerx, playery = startx, starty
    playerx, playery = 1, 0
    matrix = [[gray for i in range(c)] for j in range(r)]
    matrix[startx][starty] = white
    labyrynth(startx, starty)
    key_collected = False
    if flag2 == False:
        pygame.mixer.music.load("Game music.mp3")
        pygame.mixer.music.play(loops=-1)

    for i in range(size // 2):
        cycx, cycy = random.randint(2, c - 3), random.randint(2, r - 3)
        matrix[cycx][cycy] = white

    exitx, exity = None, None

    exits = []
    for i in range(1, r - 1):
        if matrix[i][c - 2] == white:
            exits.append(i)
    if exits:
        exitx = random.choice(exits)
    else:
        exitx = random.randint(1, r - 2)
        i = 2
    exity = c - 1
    if exitx is not None and exity is not None:
        matrix[exitx][exity] = white
        matrix[exitx][exity - 1] = white
    matrix[exitx][exity - 2]
    matrix[exitx][exity - 3]

    coins = []
    for i in range(coinsnum):
        while True:
            coinx, coiny = random.randint(1, r - 2), random.randint(1, c - 2)
            if matrix[coinx][coiny] == white and [coinx, coiny] not in coins:
                coins.append([coinx, coiny])
                break

    spikes = []
    for i in range(spikesnum):
        while True:
            spikex, spikey = random.randint(1, r - 2), random.randint(1, c - 2)
            if matrix[spikex][spikey] == white and [spikex, spikey] not in spikes and [spikex, spikey] not in coins:
                spikes.append([spikex, spikey])
                break

    while True:
        keyxm, keyym = random.randint(1, r - 2), random.randint(1, c - 2)
        if matrix[keyxm][keyym] == white and [keyxm, keyym] not in spikes and [keyxm, keyym] not in coins:
            keyx, keyy = keyxm, keyym
            break

    if random.randint(1, 2) == 1:
        while True:
            heartxm, heartym = random.randint(1, r - 2), random.randint(1, c - 2)
            if matrix[heartxm][heartym] == white and [heartxm, heartym] not in spikes and [heartxm, heartym] not in coins and heartxm != keyx and heartym != keyy:
                heartx, hearty = heartxm, heartym
                break
    else:
        heartx, hearty = -1, -1

    enemies = []
    for i in range(enemiesnum):
        enemyx, enemyy = random.randint(1, r - 2), random.randint(1, c - 2)
        while matrix[enemyx][enemyy] != white:
            enemyx, enemyy = random.randint(1, r - 2), random.randint(1, c - 2)
        enemies.append([enemyx, enemyy, [], count, "s"])

    random_wall = random.choice(walls)
    random_wall = pygame.transform.scale(random_wall, (size, size))

    random_coin = random.choice([coin1, coin2])
    random_coin = pygame.transform.scale(random_coin, (size, size))

    golemd1 = pygame.transform.scale(golemd1, (size, size))
    golemd2 = pygame.transform.scale(golemd2, (size, size))
    golemu1 = pygame.transform.scale(golemu1, (size, size))
    golemu2 = pygame.transform.scale(golemu2, (size, size))
    golemr1 = pygame.transform.scale(golemr1, (size, size))
    golemr2 = pygame.transform.scale(golemr2, (size, size))
    goleml1 = pygame.transform.scale(goleml1, (size, size))
    goleml2 = pygame.transform.scale(goleml2, (size, size))
    golems = pygame.transform.scale(golems, (size, size))

    spike1 = pygame.transform.scale(spike1, (size, size))
    spike2 = pygame.transform.scale(spike2, (size, size))
    spike3 = pygame.transform.scale(spike3, (size, size))
    spike4 = pygame.transform.scale(spike4, (size, size))
    spike5 = pygame.transform.scale(spike5, (size, size))
    spike6 = pygame.transform.scale(spike6, (size, size))
    spike7 = pygame.transform.scale(spike7, (size, size))
    spike8 = pygame.transform.scale(spike8, (size, size))
    spike9 = pygame.transform.scale(spike9, (size, size))

    eye = pygame.transform.scale(eye, (size, size))

    random_key = random.choice([key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, key11, key12])
    random_key = pygame.transform.scale(random_key, (size, size))

    heart = pygame.transform.scale(heart, (size, size))

    pairs = [[chest1, chest1_open], [chest2, chest2_open], [chest3, chest3_open], [chest4, chest4_open], [chest5, chest5_open], [chest6, chest6_open], [chest7, chest7_open], [chest8, chest8_open], [chest9, chest9_open], [chest10, chest10_open], [chest11, chest11_open], [chest12, chest12_open]]
    random_chest, random_chest_open = random.choice(pairs)
    random_chest = pygame.transform.scale(random_chest, (size, size))
    random_chest_open = pygame.transform.scale(random_chest_open, (size, size))

    spikes_img = [spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9]
    golemr = [golemr1, golemr2]
    goleml = [goleml1, goleml2]
    golemu = [golemu1, golemu2]
    golemd = [golemd1, golemd2]

def menu():
    pygame.mixer.init()
    pygame.mixer.music.load("Menu music.mp3")
    pygame.mixer.music.play(loops=-1)
    n = 20
    count_frames = 0
    texty = 60
    dr = -1
    guide = False
    with open("Best Score.txt", "r") as file:
        best_score = int(file.read())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    Book_snd.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Game music.mp3")
                    pygame.mixer.music.play(loops=-1)
                    flag2 = True
                    return
                elif guide_button.collidepoint(event.pos):
                    Book_snd.play()
                    guide = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Book_snd.play()
                    guide = False

        if guide:
            screen.blit(BG_menu, (0, 0))
            font = pygame.font.Font("Jacquard12-Regular.ttf", 30)
            guide_text = [
                "You are a golem. ",
                "Your goal is to reach the end of the dungeon.",
                "There will be many rooms with ",
                "obstacles and coins     on your way, and",
                "at the end there wil     be a   chest with a power-up that can",
                "be obtained for                     the   collected key.",
                "GOOD luck!"
            ]

            for i, j in enumerate(guide_text):
                text = font.render(j, True, black)
                screen.blit(text, (105, 40 + i * 40))

        else:
            screen.blit(BG_menu, (0, 0))
            font = pygame.font.Font("Jacquard12-Regular.ttf", 87)
            title_text = font.render("GOLEM rush", True, black)
            screen.blit(title_text, ((width // 2) - 20 - title_text.get_width() // 2, texty))

            font = pygame.font.Font("Jacquard12-Regular.ttf", 48)

            start_text = font.render("Start", True, black)
            start_button = button_menu.get_rect(center=(width // 2 + 130, height // 2 - 50))
            screen.blit(button_menu, start_button)
            screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))

            guide_text = font.render("Guide", True, black)
            guide_button = button_menu.get_rect(center=(width // 2 + 130, height // 2 + 50))
            screen.blit(button_menu, guide_button)
            screen.blit(guide_text, (guide_button.centerx - guide_text.get_width() // 2, guide_button.centery - guide_text.get_height() // 2))

            font_score = pygame.font.Font("Jacquard12-Regular.ttf", 36)
            best_score_text = font_score.render(f"Best Score: {best_score}", True, white)
            screen.blit(best_score_text, (20, height - 50))

            count_frames += 1
            if count_frames % n == 0:
                texty += 10 * dr
                if texty <= 50:
                    dr = 1
                elif texty >= 60:
                    dr = -1

        pygame.display.flip()
        clock.tick(30)

def powerup_help(random_powerup):
    global HP_count, max_HP
    if random_powerup == "More Coins":
        global coinsnum
        coinsnum += 1
    elif random_powerup == "Slower enemie":
        global speed
        speed += 2
    elif random_powerup == "Coins boost":
        global boost_coins
        boost_coins += 0.5
    elif random_powerup == "Heal HP":
        if HP_count == max_HP:
            max_HP += 2
            HP_count += 2
        else:
            HP_count = max_HP
    elif random_powerup == "Less Damage":
        global boost_damage
        boost_damage += 0.1
    elif random_powerup == "Rebirth":
        global rebirth
        rebirth = True
    elif random_powerup == "Heal 1 HP":
        if HP_count < max_HP:
            HP_count += 1
    elif random_powerup == "Immunity":
        global immunity, immune_room
        immunity = True
        immune_room = roomnum + 1
    elif random_powerup == "Destroy Column (K1)":
        global destroy_column
        destroy_column += 1
    elif random_powerup == "Destroy Row (K2)":
        global destroy_row
        destroy_row += 1

def powerup():
    global HP_count, speed, coinsnum, on_spike, enemiesnum, boost

    Chest_snd.play()
    random_powerups = random.sample(powerups, 2)
    screen.blit(BG_treasure, (0, 0))
    font1 = pygame.font.Font("Jacquard12-Regular.ttf", 58)
    text0 = font1.render("Choose a Powerup!", True, white)
    screen.blit(text0, (width // 2 - 70, 50))

    font1 = pygame.font.Font("Jacquard12-Regular.ttf", 36)
    text01 = font1.render("(costs 1 coin)", True, white)
    screen.blit(text01, (width // 2 + 50, 110))

    text1 = font1.render(random_powerups[0], True, black)
    text2 = font1.render(random_powerups[1], True, black)
    text3 = font1.render("Heal 1 HP", True, black)

    button = pygame.transform.scale(button_menu, (320, 130))
    powerup1_button = pygame.Rect(width // 2, height // 2 - 100, 320, 130)
    powerup2_button = pygame.Rect(width // 2, height // 2 + 50, 320, 130)
    powerup3_button = pygame.Rect(width // 2, height // 2 + 200, 320, 130)

    screen.blit(button, powerup1_button.topleft)
    screen.blit(button, powerup2_button.topleft)
    screen.blit(button, powerup3_button.topleft)

    text1_rect = text1.get_rect(center=powerup1_button.center)
    text2_rect = text2.get_rect(center=powerup2_button.center)
    text3_rect = text3.get_rect(center=powerup3_button.center)

    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    screen.blit(text3, text3_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if powerup1_button.collidepoint(event.pos):
                    powerup_help(random_powerups[0])
                    return
                elif powerup2_button.collidepoint(event.pos):
                    powerup_help(random_powerups[1])
                    return
                elif powerup3_button.collidepoint(event.pos):
                    powerup_help("Heal 1 HP")
                    return

divisors = [10, 14, 20, 25, 28, 35, 50, 70, 100]
div = 0
width, height = 700, 700
r = divisors[div]
c = r
size = width // c
coinsnum = 1
spikesnum = 0
enemiesnum = 0
coins_count = 0
max_HP = 30
HP_count = max_HP
on_spike = False
on_enemie = False
speed = 5
count = 0
roomnum = 1
rotate_count = 0
curr_spike = 0
key_collected = False
boost_coins = 0
boost_damage = 0
rebirth = False
immunity = True
immune_room = -1
destroy_column = 0
destroy_row = 0
win = False
flag2 = False

white = (255, 255, 255)
black = (0, 0, 0)
gray = (125, 125, 125)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 215, 0)
brown = (111, 62, 67)
darkgray = (64, 74, 95)

screen = pygame.display.set_mode((width + 300, height))
pygame.display.set_caption("GOLEM rush")
clock = pygame.time.Clock()

Chest_snd = pygame.mixer.Sound("Chest sound.mp3")
Coin_snd = pygame.mixer.Sound("Coin sound.mp3")
Damage_snd = pygame.mixer.Sound("Damage sound.mp3")
Laser_snd = pygame.mixer.Sound("Laser.mp3")
Step_snd = pygame.mixer.Sound("Step.mp3")
Book_snd = pygame.mixer.Sound("Book.mp3")
Key_snd = pygame.mixer.Sound("Key.mp3")

BG_menu = pygame.image.load("BG menu.png")
BG_treasure = pygame.image.load("Treasure.png")
BG_win = pygame.image.load("Winning BG.png")
button_menu = pygame.image.load("Button menu.png")
heart = pygame.image.load("Heart.png")
wall0 = pygame.image.load("Wall 0.png")
wall1 = pygame.image.load("Wall 1.png")
wall2 = pygame.image.load("Wall 2.png")
wall3 = pygame.image.load("Wall 3.png")
wall4 = pygame.image.load("Wall 4.png")
wall5 = pygame.image.load("Wall 5.png")
wall6 = pygame.image.load("Wall 6.png")
wall7 = pygame.image.load("Wall 7.png")
tile = pygame.image.load("tile.png")
coin1 = pygame.image.load("Coin 1.png")
coin2 = pygame.image.load("Coin 2.png")
eye = pygame.image.load("Eye 1.png")
spike1 = pygame.image.load("newspike 1.png")
spike2 = pygame.image.load("newspike 2.png")
spike3 = pygame.image.load("newspike 3.png")
spike4 = pygame.image.load("newspike 4.png")
spike5 = pygame.image.load("newspike 5.png")
spike6 = pygame.image.load("newspike 6.png")
spike7 = pygame.image.load("newspike 7.png")
spike8 = pygame.image.load("newspike 8.png")
spike9 = pygame.image.load("newspike 9.png")
golems = pygame.image.load("Golem 1.png")
golemr1 = pygame.image.load("Golem 10.png")
golemr2 = pygame.image.load("Golem 11.png")
goleml1 = pygame.image.load("Golem 8.png")
goleml2 = pygame.image.load("Golem 9.png")
golemd1 = pygame.image.load("Golem 2.png")
golemd2 = pygame.image.load("Golem 3.png")
golemu1 = pygame.image.load("Golem 12.png")
golemu2 = pygame.image.load("Golem 13.png")
key1 = pygame.image.load("Key 1.png")
key2 = pygame.image.load("Key 2.png")
key3 = pygame.image.load("Key 3.png")
key4 = pygame.image.load("Key 4.png")
key5 = pygame.image.load("Key 5.png")
key6 = pygame.image.load("Key 6.png")
key7 = pygame.image.load("Key 7.png")
key8 = pygame.image.load("Key 8.png")
key9 = pygame.image.load("Key 9.png")
key10 = pygame.image.load("Key 10.png")
key11 = pygame.image.load("Key 11.png")
key12 = pygame.image.load("Key 12.png")
chest1 = pygame.image.load("Chest 1.png")
chest2 = pygame.image.load("Chest 2.png")
chest3 = pygame.image.load("Chest 3.png")
chest4 = pygame.image.load("Chest 4.png")
chest5 = pygame.image.load("Chest 5.png")
chest6 = pygame.image.load("Chest 6.png")
chest7 = pygame.image.load("Chest 7.png")
chest8 = pygame.image.load("Chest 8.png")
chest9 = pygame.image.load("Chest 9.png")
chest10 = pygame.image.load("Chest 10.png")
chest11 = pygame.image.load("Chest 11.png")
chest12 = pygame.image.load("Chest 12.png")
chest1_open = pygame.image.load("Chest 1 open.png")
chest2_open = pygame.image.load("Chest 2 open.png")
chest3_open = pygame.image.load("Chest 3 open.png")
chest4_open = pygame.image.load("Chest 4 open.png")
chest5_open = pygame.image.load("Chest 5 open.png")
chest6_open = pygame.image.load("Chest 6 open.png")
chest7_open = pygame.image.load("Chest 7 open.png")
chest8_open = pygame.image.load("Chest 8 open.png")
chest9_open = pygame.image.load("Chest 9 open.png")
chest10_open = pygame.image.load("Chest 10 open.png")
chest11_open = pygame.image.load("Chest 11 open.png")
chest12_open = pygame.image.load("Chest 12 open.png")

golemr = [golemr1, golemr2]
goleml = [goleml1, goleml2]
golemu = [golemu1, golemu2]
golemd = [golemd1, golemd2]
spikes_img = [spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9]
walls = [wall0, wall1, wall2, wall3, wall4, wall5, wall6, wall7]
frames_golem_over = []
curr_golem_over = 0
for i in range(1, 21):
    frame = pygame.image.load(f"Golem Over {i}.png")
    frame = pygame.transform.scale(frame, (width + 300, height))
    frames_golem_over.append(frame)

BG_menu = pygame.transform.scale(BG_menu, (width + 300, height))
BG_treasure = pygame.transform.scale(BG_treasure, (width + 300, height))
BG_win = pygame.transform.scale(BG_win, (width + 300, height))
button_menu = pygame.transform.scale(button_menu, (180, 95))

powerups = ["Heal HP", "Coins boost", "More Coins", "Slower enemie", "Less Damage", "Rebirth", "Immunity", "Destroy Column (K1)", "Destroy Row (K2)"]


playerx, playery = 1, 0
goalx, goaly = playerx, playery
direction = "s"
golem_frame = 0
move = False

menu()
flag2 = True
newRoom(1, 0, size, coinsnum, spikesnum, enemiesnum)

running = True
time = 0
timed = 10
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and matrix[playerx - 1][playery] == white and HP_count > 0:
                Step_snd.play()
                goalx, goaly = playerx - 1, playery
                direction = "u"
                playerx -= 1
                move = True
                time = timed
            elif event.key == pygame.K_DOWN and matrix[playerx + 1][playery] == white and HP_count > 0:
                Step_snd.play()
                goalx, goaly = playerx + 1, playery
                direction = "d"
                playerx += 1
                move = True
                time = timed
            elif event.key == pygame.K_LEFT and matrix[playerx][playery - 1] == white and HP_count > 0:
                Step_snd.play()
                goalx, goaly = playerx, playery - 1
                playery -= 1
                direction = "l"
                move = True
                time = timed
            elif event.key == pygame.K_RIGHT and matrix[playerx][playery + 1] == white and HP_count > 0:
                Step_snd.play()
                goalx, goaly = playerx, playery + 1
                playery += 1
                direction = "r"
                move = True
                time = timed
            elif event.key == pygame.K_1 and destroy_column > 0:
                for i in range(r):
                    matrix[i][playery] = white
                destroy_column -= 1
                Laser_snd.play()
            elif event.key == pygame.K_2 and destroy_row > 0:
                for i in range(c):
                    matrix[playerx][i] = white
                destroy_row -= 1
                Laser_snd.play()
            else:
                move = False
            if event.key == pygame.K_ESCAPE:
                running = False


    if HP_count <= 0 and rebirth:
        playerx, playery = 1, 0
        HP_count = max_HP // 5
        rebirth = False

    if roomnum == 15:
        win = True
        running = False

    if HP_count <= 0:
        score = (int(coins_count) - (15 - roomnum) // 2)
        with open("Best Score.txt", "r") as file:
            best_score = int(file.read())
        if score > best_score:
            with open("Best Score.txt", "w") as file:
                file.write(str(score))
            best_score = score

        if score < 0:
            score = 0

        pygame.mixer.music.load("Game over music.mp3")
        pygame.mixer.music.play(loops=-1)
        screen = pygame.display.set_mode((width, height))

        for i in range(len(frames_golem_over) * 10):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        playerx, playery = 1, 0
                        coins_count = 0
                        HP_count = max_HP
                        roomnum = 1
                        key_collected = False
                        coinsnum = 1
                        spikesnum = 0
                        enemiesnum = 0
                        div = 0
                        r = divisors[div]
                        c = r
                        size = width // c
                        flag = False
                        flag2 = False
                        screen = pygame.display.set_mode((width + 300, height))
                        menu()
                        newRoom(1, 0, size, coinsnum, spikesnum, enemiesnum)
                        pygame.mixer.music.stop()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

            screen.fill((0, 0, 0))
            screen.blit(frames_golem_over[curr_golem_over], (width // 2 - frames_golem_over[curr_golem_over].get_width() // 2, height // 2 - frames_golem_over[curr_golem_over].get_height() // 2))
            curr_golem_over = (curr_golem_over + 1) % len(frames_golem_over)
            font = pygame.font.Font("Jacquard12-Regular.ttf", 90)
            text1 = font.render("Game", True, black)
            text2 = font.render("Over", True, black)
            screen.blit(text1, (width // 2 + 70, 80))
            screen.blit(text2, (width // 2 + 70, 150))

            font2 = pygame.font.Font("Jacquard12-Regular.ttf", 36)
            text2 = font2.render("press ENTER to restart", True, white)
            text_rect2 = text2.get_rect(center=(width // 2, height // 2 + 280))
            screen.blit(text2, text_rect2)

            font3 = pygame.font.Font("Jacquard12-Regular.ttf", 36)
            text3 = font3.render("press ESC to quit", True, white)
            text_rect3 = text3.get_rect(center=(width // 2, height // 2 + 310))
            screen.blit(text3, text_rect3)

            font4 = pygame.font.Font("Jacquard12-Regular.ttf", 30)
            text4 = font4.render(f"Score: {score}", True, white)
            text_rect4 = text4.get_rect(center=(50, height // 2 + 280))
            screen.blit(text4, text_rect4)

            font5 = pygame.font.Font("Jacquard12-Regular.ttf", 30)
            text5 = font5.render(f"Best Score: {best_score}", True, white)
            text_rect5 = text5.get_rect(center=(80, height // 2 + 310))
            screen.blit(text5, text_rect5)

            pygame.display.flip()
            clock.tick(17)

    if [playerx, playery] in coins:
        coins.remove([playerx, playery])
        coins_count += 1 + boost_coins
        Coin_snd.play()

    if playerx == heartx and playery == hearty:
        HP_count = max_HP
        heartx, hearty = -1, -1

    if playerx == keyx and playery == keyy and not key_collected:
        Key_snd.play()
        key_collected = True
        keyx, keyy = -1, -1

    if [playerx, playery] in spikes:
        if not on_spike and not (immunity and immune_room >= roomnum):
            HP_count -= 1 + boost_damage
            Damage_snd.play()
            on_spike = True
    else:
        on_spike = False

    for i in range(enemiesnum):
        enemyx, enemyy, path, count, enemy_direction = enemies[i]
        count += 1
        if count >= speed:
            if not path:
                path = deikstra((enemyx, enemyy), (playerx, playery), matrix)
            else:
                new = path.pop(0)
                if new[0] > enemyx:
                    enemy_direction = "d"
                elif new[0] < enemyx:
                    enemy_direction = "u"
                elif new[1] > enemyy:
                    enemy_direction = "r"
                elif new[1] < enemyy:
                    enemy_direction = "l"
                enemyx, enemyy = new[0], new[1]
            count = 0
        enemies[i] = [enemyx, enemyy, path, count, enemy_direction]

        if playerx == enemyx and playery == enemyy:
            if not on_enemie and not (immunity and immune_room >= roomnum):
                HP_count -= 1 + boost_damage
                Damage_snd.play()
                on_enemie = True
        else:
            on_enemie = False

    if playerx == exitx and playery == exity:
        if key_collected and coins_count >= 1:
            powerup()
            coins_count -= 1
        r = divisors[div]
        c = r
        size = width // c
        if roomnum in [3, 5, 7, 10, 13]:
            div += 1
        if roomnum % 2 == 0:
            coinsnum += 1
        if roomnum % 2 != 0:
            spikesnum += 1
        if roomnum % 4 == 0:
            enemiesnum += 1

        if immunity and roomnum >= immune_room:
            immunity = False
            immune_room = -1

        newRoom(1, 0, size, coinsnum, spikesnum, enemiesnum)
        roomnum += 1

    tile = pygame.transform.scale(tile, (size, size))
    for row in range(r):
        for col in range(c):
            if matrix[row][col] == white:
                screen.blit(tile, (col * size, row * size))
            elif matrix[row][col] == gray:
                screen.blit(random_wall, (col * size, row * size))

    rotate_count += 1
    if rotate_count >= 5:
        curr_spike = (curr_spike + 1) % len(spikes_img)
        rotate_count = 0

    for i in spikes:
        rect = pygame.Rect(i[1] * (size - 1.1), i[0] * (size - 0.6), size + 10, size + 10)
        a = spikes_img[curr_spike]
        a = pygame.transform.scale(a, (size + 10, size + 10))
        screen.blit(a, rect.topleft)

    for i in coins:
        screen.blit(random_coin, (i[1] * size, i[0] * size))

    screen.blit(random_key, (keyy * size, keyx * size))
    if heartx != -1 and hearty != -1:
        screen.blit(heart, (heartx * size, hearty * size))

    for i in enemies:
        enemyx, enemyy, path, count, enemy_direction = i
        if enemy_direction == "u":
            rotated_eye = pygame.transform.rotate(eye, 0)
        elif enemy_direction == "d":
            rotated_eye = pygame.transform.rotate(eye, 180)
        elif enemy_direction == "l":
            rotated_eye = pygame.transform.rotate(eye, 90)
        elif enemy_direction == "r":
            rotated_eye = pygame.transform.rotate(eye, -90)
        else:
            rotated_eye = eye
        screen.blit(rotated_eye, (i[1] * size, i[0] * size))

    if HP_count > 0:
        if move or time > 0:
            if direction == "r":
                screen.blit(golemr[(golem_frame // 2) % len(golemr)], (playery * size, playerx * size))
            elif direction == "l":
                screen.blit(goleml[(golem_frame // 2) % len(goleml)], (playery * size, playerx * size))
            elif direction == "u":
                screen.blit(golemu[(golem_frame // 2) % len(golemu)], (playery * size, playerx * size))
            elif direction == "d":
                screen.blit(golemd[(golem_frame // 2) % len(golemd)], (playery * size, playerx * size))

            if move:
                golem_frame += 1
                if golem_frame >= 4:
                    golem_frame = 0
            if not move:
                time -= 1
        else:
            screen.blit(golems, (playery * size, playerx * size))

    font = pygame.font.Font("Jacquard12-Regular.ttf", 36)
    pygame.draw.rect(screen, white, (width, 0, 300, height))
    textroom = font.render(f"Room {roomnum}", True, black)
    textcoins = font.render(f"Coins: {coins_count}", True, black)
    texthp = font.render(f"HP: {HP_count}", True, black)
    screen.blit(textroom, (width + 10, 10))
    screen.blit(textcoins, (width + 10, 50))
    screen.blit(texthp, (width + 10, 90))
    if key_collected:
        textkey = font.render("Key Collected!", True, black)
        screen.blit(textkey, (width + 10, 130))
        screen.blit(random_chest_open, (exity * size, exitx * size))
    else:
        screen.blit(random_chest, (exity * size, exitx * size))

    pygame.display.flip()
    clock.tick(30)

def color_change(color_time):
    r = int((math.sin(color_time / 100) + 1) * 127.5)
    g = int((math.sin(color_time / 100 + 2 * math.pi / 3) + 1) * 127.5)
    b = int((math.sin(color_time / 100 + 4 * math.pi / 3) + 1) * 127.5)
    return (r, g, b)

if win:
    with open("Best Score.txt", "r") as file:
        best_score = int(file.read())
    if coins_count > best_score:
        with open("Best Score.txt", "w") as file:
            file.write(str(coins_count))
        best_score = coins_count

    color_time = 0
    pygame.mixer.music.load("Winning music.ogg")
    pygame.mixer.music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(BG_win, (0, 0))
        color = color_change(color_time)
        font = pygame.font.Font("Jacquard12-Regular.ttf", 90)
        text = font.render("You Win!", True, color)
        text_rect = text.get_rect(center=(width // 2 + 150, height // 2 + 40))
        screen.blit(text, text_rect)
        color_time += 1

        font1 = pygame.font.Font("Jacquard12-Regular.ttf", 50)
        text1 = font1.render(f"Score: {coins_count}", True, (255 - color[0], 255 - color[1], 255 - color[2]))
        text_rect1 = text1.get_rect(center=(width // 2 + 150, height // 2 + 100))
        screen.blit(text1, text_rect1)

        font2 = pygame.font.Font("Jacquard12-Regular.ttf", 50)
        text2 = font2.render(f"Best Score: {best_score}", True, (255 - color[0], 255 - color[1], 255 - color[2]))
        text_rect2 = text2.get_rect(center=(width // 2 + 150, height // 2 + 150))
        screen.blit(text2, text_rect2)

        font3 = pygame.font.Font("Jacquard12-Regular.ttf", 36)
        text3 = font3.render("press ESC to quit", True, white)
        text_rect3 = text3.get_rect(center=(width // 2 + 150, height // 2 + 310))
        screen.blit(text3, text_rect3)

        pygame.display.flip()
        clock.tick(1000)

pygame.quit()
sys.exit()
