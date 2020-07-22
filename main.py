import pygame
from pygame import mixer
import random
import math

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((800, 600))  # (width,height)  create screen

# Background, Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
background = pygame.image.load('background.png').convert()
pygame.display.set_icon(icon)

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# player
playerImg = pygame.image.load('player.png')
playerX = 375
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.65)
    enemyY_change.append(35)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 2
bullet_state = 'ready'


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y - 15))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 25:
        return True
    return False


# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font_X = 10
font_Y = 10


def show_score(x, y):
    Score = font.render('Score : ' + str(score), True, (245, 245, 245))
    screen.blit(Score, (x, y))


# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    over_text = over_font.render('Game Over', True, (210, 210, 210))
    screen.blit(over_text, (230, 240))


# Game loop
running = True
while running:
    screen.fill((10, 128, 128))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.85

            if event.key == pygame.K_RIGHT:
                playerX_change += 0.85

            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                fire_bullet(playerX, bulletY)
                bulletX = playerX  # get the current X co-ordinate of the spaceship

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # checking for boundary
    playerX += playerX_change
    if playerX <= -4:
        playerX = -4
    elif playerX >= 740:
        playerX = 740

    # enemy movement
    for i in range(num_enemies):

        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 1000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -4:
            enemyX_change[i] = 0.65
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 740:
            enemyX_change[i] = -0.65
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 200)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement

    if bullet_state == 'fire':
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)

    if bulletY <= 50:
        bulletY = 480
        bullet_state = 'ready'
        bulletX = 0

    player(playerX, playerY)
    show_score(font_X, font_Y)
    pygame.display.update()
