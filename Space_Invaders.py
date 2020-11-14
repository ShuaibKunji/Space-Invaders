# Attributes for sprites/icons:
# Icons made by <a href="http://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# Icons made by <a href="https://www.flaticon.com/free-icon/spaceship_2240745?term=spaceship&page=3&position=30" title="smalllikeart">smalllikeart</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# <a href="https://www.freepik.com/vectors/background">Background vector created by freepik - www.freepik.com</a>
# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

import pygame
import random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1280, 720))  # Create a screen of specified resolution

# Title bar
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')  # icon for title bar
pygame.display.set_icon(icon)

# Background setup
bg = pygame.image.load('bg.jpg')
mixer.music.load('bgloop.wav')
mixer.music.play(-1)

# Player setup
PlayerImg = pygame.image.load('Player.png')
PlayerX = 608
PlayerY = 582
PlaUpd = 0

# Aliens setup
AlienImg = []
AlienX = []
AlienY = []
AlienUpdX = []
AlienUpdY = []
num = 6

for x in range(num):
    AlienImg.append(pygame.image.load('alien.png'))
    AlienX.append(random.randint(0, 1216))
    AlienY.append(random.randint(0, 100))
    AlienUpdX.append(3)
    AlienUpdY.append(64)

# Bullet setup
BulletImg = pygame.image.load('bullet.png')
BulletX = PlayerX + 56
BulletY = PlayerY - 16
BullUpdY = 8
BulletState = 'ready'  # ready->Bullet is invisible and stationary & fired->Bullet is visible and moving

score = 0
font = pygame.font.Font('freesansbold.ttf', 40)
scoreX = 20
scoreY = 20


def player(ax, ay):
    screen.blit(PlayerImg, (ax, ay))


def alien(ax, ay, ai):
    screen.blit(AlienImg[ai], (ax, ay))


def fire_bullet(bx, by):
    if BulletState == 'fired':
        screen.blit(BulletImg, (bx, by))


def detect_collision(ax, ay, bx, by):
    global BulletState
    if BulletState == 'fired':
        if by in range(ay - 64, ay) and bx in range(ax, ax + 64):
            return True
        else:
            return False


def drawScore(sx, sy):
    scorel = font.render("SCORE : " + str(score), True, (255, 0, 0))
    screen.blit(scorel, (sx, sy))


# Game Over
GOfont = pygame.font.Font('freesansbold.ttf', 80)
GOX = 400
GOY = 300


def gameOver():
    GO = GOfont.render("GAME OVER", True, (255, 0, 0))
    screen.blit(GO, (GOX, GOY))


# Game Window loop
running = True
while running:
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        # Event handler for clicking the close button
        if event.type == pygame.QUIT:
            running = False

        # Event handlers for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlaUpd = -10
            if event.key == pygame.K_RIGHT:
                PlaUpd = 10
            if event.key == pygame.K_SPACE:
                if BulletState == 'ready':
                    BulletY = PlayerY - 16
                    BulletX = PlayerX + 56
                    BulletState = 'fired'
                    fired = mixer.Sound('bullet.wav')
                    fired.play()
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            PlaUpd = 0

    # Boundary conditions and position update for spaceship
    if PlayerX <= 0:
        PlayerX = 0
    if PlayerX >= 1152:
        PlayerX = 1152
    PlayerX += PlaUpd

    for i in range(num):
        # Boundary conditions and position update for Alien
        if AlienX[i] <= 0:
            AlienUpdX[i] = 3
            AlienY[i] += AlienUpdY[i]
        if AlienX[i] >= 1216:
            AlienUpdX[i] = -3
            AlienY[i] += AlienUpdY[i]
        AlienX[i] += AlienUpdX[i]

        # Check for collision between bullet and alien
        colDet = detect_collision(AlienX[i], AlienY[i], BulletX, BulletY)
        if colDet:
            explosion = mixer.Sound('collision.wav')
            explosion.play()
            BulletY = PlayerY - 16
            BulletState = 'ready'
            score += 1
            AlienX[i] = random.randint(0, 1216)
            AlienY[i] = random.randint(0, 100)

        # Check if any alien has gone below the player
        if AlienY[i] >= PlayerY:
            for j in range(num):
                AlienY[j] = 2000
            gameOver()
            break

    # Boundary conditions and position update for bullet
    if BulletY <= 0:
        BulletY = PlayerY - 16
        BulletState = 'ready'
    if BulletState == 'fired':
        BulletY -= BullUpdY

    fire_bullet(BulletX, BulletY)
    player(PlayerX, PlayerY)
    for i in range(num):
        alien(AlienX[i], AlienY[i], i)
    drawScore(scoreX, scoreY)
    pygame.display.update()  # Update the changes to the display
