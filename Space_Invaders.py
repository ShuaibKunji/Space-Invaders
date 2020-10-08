# Attributes for sprites/icons:
# Icons made by <a href="http://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# Icons made by <a href="https://www.flaticon.com/free-icon/spaceship_2240745?term=spaceship&page=3&position=30" title="smalllikeart">smalllikeart</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# <a href="https://www.freepik.com/vectors/background">Background vector created by freepik - www.freepik.com</a>
# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1280, 720))

# Title bar
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')  # icon for title bar
pygame.display.set_icon(icon)

# Background setup
bg = pygame.image.load('bg.jpg')

# Player setup
PlayerImg = pygame.image.load('Player.png')
PlayerX = 608
PlayerY = 582
PlaUpd = 0

# Alien setup
AlienImg = pygame.image.load('alien.png')
AlienX = random.randint(0, 1216)
AlienY = random.randint(0, 100)
AlienUpdX = 3
AlienUpdY = 64

# Bullet setup
BulletImg = pygame.image.load('bullet.png')
BulletX = PlayerX + 56
BulletY = PlayerY - 16
BullUpdY = 8
BulletState = 'ready'  # ready->Bullet is invisible and stationary & fired->Bullet is visible and moving

score = 0


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def alien(x, y):
    screen.blit(AlienImg, (AlienX, AlienY))


def fire_bullet(x, y):
    global BulletState
    if BulletState == 'fired':
        screen.blit(BulletImg, (x, y))


def detect_collision(ax, ay, bx, by):
    global BulletState
    if BulletState == 'fired':
        if by in range(ay - 64, ay) and bx in range(ax, ax + 64):
            return True
        else:
            return False


# Game Window loop
running = True
while running:
    screen.fill((0, 0, 128))  # Values in parenthesis are RGB, given combination is for Navy
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
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            PlaUpd = 0

    # Boundary conditions and position update for spaceship
    if PlayerX <= 0:
        PlayerX = 0
    if PlayerX >= 1152:
        PlayerX = 1152
    PlayerX += PlaUpd

    # Boundary conditions and position update for Alien
    if AlienX <= 0:
        AlienUpdX = 3
        AlienY += AlienUpdY
    if AlienX >= 1216:
        AlienUpdX = -3
        AlienY += AlienUpdY
    AlienX += AlienUpdX

    # Boundary conditions and position update for bullet
    if BulletY <= 0:
        BulletY = PlayerY - 16
        BulletState = 'ready'
    if BulletState == 'fired':
        BulletY -= BullUpdY

    # Check for collision between bullet and alien
    colDet = detect_collision(AlienX, AlienY, BulletX, BulletY)
    if colDet:
        BulletY = PlayerY - 16
        BulletState = 'ready'
        score += 1
        print(score)
        AlienX = random.randint(0, 1216)
        AlienY = random.randint(0, 100)

    fire_bullet(BulletX, BulletY)
    player(PlayerX, PlayerY)
    alien(AlienX, AlienY)
    pygame.display.update()  # Update the changes to the display
