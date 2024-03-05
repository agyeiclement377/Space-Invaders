import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('background.jpg')
#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('battleship.png')
pygame.display.set_icon(icon)
# Player
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


# Enemy class
class Enemy:
    def __init__(self,enemyimg,enemyX,enemyY,enemyX_change,enemyY_change,enemy_power):
        self.enemyimg = enemyimg
        self.enemyX = enemyX
        self.enemyY = enemyY
        self.enemyX_change = enemyX_change
        self.enemyY_change = enemyY_change
        self.enemy_power = enemy_power
    def enemy(self,x, y):
        screen.blit(self.enemyimg, (x, y))
    def isCollision(self,bulletX, bulletY):
        distance = math.sqrt(math.pow(bulletX - self.enemyX, 2) + math.pow(bulletY - self.enemyY, 2))
        if distance < 27:
            return True
        else:
            return False


enemies = []
num_of_enemies = 6

for i in range(num_of_enemies - 3):
    enemies.append(Enemy(pygame.image.load('ufo.png'),random.randint(0, 736), random.randint(50, 150), 0.1, 40, 5 ))
    enemies.append(Enemy(pygame.image.load('ufo2.png'), random.randint(0, 736), random.randint(50, 150), 0.1, 40, 10))

# Bullet
# ready : not firing state
# fire : fired state
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10
#game over
game_over = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether it's right or left || KeyDown means pressing that button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # update the X position of the player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #update the Y position of the Player
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # update the X position of the enemy
    for enemy in enemies:
        #Game over
        collision_with_player = enemy.isCollision(playerX, playerY)
        if collision_with_player:
            game_over_text()
            break
        enemy.enemyX += enemy.enemyX_change
        if enemy.enemyX <= 0:
            enemy.enemyX_change = 0.1
            enemy.enemyY += enemy.enemyY_change
        elif enemy.enemyX >= 736:
            enemy.enemyX_change = -0.1
            enemy.enemyY += enemy.enemyY_change

        # collision
        collision = enemy.isCollision(bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemy.enemy_power -= 1
            if enemy.enemy_power == 0:
                enemy.enemyX = -15
                enemy.enemyY = 1000

        enemy.enemy(enemy.enemyX, enemy.enemyY)


    # Bullet Movement
    if bulletY <= 0:
        bulletY = 0
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

