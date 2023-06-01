import pygame
import random
import math
from pygame import mixer

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png")

pygame.init()

mixer.music.load("background.wav")
mixer.music.play(-1)


screen = pygame.display.set_mode((800, 600))


playerImg = pygame.image.load("user2.png")
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
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(10, 700))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


# score

score_value = 0
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10
#
# Game over text

over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollisio(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        False



running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
            playerY_change = 0


    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 1:
        playerX = 1
    elif playerX >= 725:
        playerX = 725
    if playerY <= 0:
        playerY = 0
    elif playerY >= 520:
        playerY = 520


    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 1:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 725:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY[i] = 0
        elif enemyY[i] >= 520:
            enemyY[i] = 520

        collision = isCollisio(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exo_sound = mixer.Sound("explosion.wav")
            exo_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(10, 700)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)

    show_score(textX, textY)
    pygame.display.update()