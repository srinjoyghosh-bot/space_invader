import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# make screen
screen = pygame.display.set_mode((800, 600))  # width and height respectively given in tuple
# 0,0 is top left corner
# top to bottom y increase , left to right x increases

# Background

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 so that it plays on loop continously

# title and icon
pygame.display.set_caption("Space Invaders")
# pygame icon must be 32 px by 32 px
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship_player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('space_enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0.3
bulletY_change = 0.5
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # 32 is text size
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250)) # middle of screen


# Ready- you can't see the bullet on screen
# Fire - the bullet is currently moving


def player(x, y):
    # blit means to draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # +16 and 10 to make bullet at mid of spaceship and at top


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# events control all happening in game window eg pressing any button etc

# game loop
running = True
while running:
    screen.fill((0, 0, 0))  # rgb in tuple for background color but won't work if display not added
    # any keystroke is an event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # press cross button
            running = False  # window closes
        # if keystroke is pressed check whether left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            # if event.type == pygame.K_SPACE:

        # key-down is pressing, keyup is releasing
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get current x coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # checking for boundaries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800-64 as image is 64 px
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800-64 as image is 64 px
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # this statement  must be after screen.fill otherwise player drawn underneath screen
    show_score(textX, textY)
    pygame.display.update()
