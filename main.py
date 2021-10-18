import pygame
import random
import math
from pygame import mixer
from pygame.font import Font

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background setup
background = pygame.image.load("background.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon setup
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("spaceship.png")
player_pos_x = 370
player_pos_y = 480
player_pos_x_change = 0

def player(x, y):
    screen.blit(playerimg, (x, y))

# Enemy
enemyimg = []
enemy_pos_x = []
enemy_pos_y = []
enemy_pos_x_change = []
enemy_pos_y_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load("ufo.png"))
    enemy_pos_x.append(random.randint(0, 736))
    enemy_pos_y.append(random.randint(50, 150))
    enemy_pos_x_change.append(5)
    enemy_pos_y_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Bullet
bulletimg = pygame.image.load("bullet.png")
bullet_pos_x = 0
bullet_pos_y = 480
bullet_pos_y_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))

# Collosion
def isCollosion(enemy_pos_x, enemy_pos_y, bullet_pos_x, bullet_pos_y):
    distance = math.sqrt(math.pow(enemy_pos_x-bullet_pos_x,2) + math.pow(enemy_pos_y-bullet_pos_y,2))
    if distance < 27:
        return True
    else:
        return False

# Score card
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Running game loop
game_running = True
while game_running:

    # Background color (RGB)
    screen.fill((0, 0, 0))
    
    # Backgorund image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # For closing the window
        if event.type == pygame.QUIT:
            game_running = False

        # Keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_pos_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_pos_x = player_pos_x
                    fire_bullet(bullet_pos_x, bullet_pos_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_pos_x_change = 0.0

    # Player movement
    player_pos_x += player_pos_x_change
    
    if player_pos_x <= 0:
        player_pos_x = 0
    elif player_pos_x >= 736:
        player_pos_x = 736

    player(player_pos_x, player_pos_y)

    # Enemy movement
    for i in range(num_of_enemy):
        enemy_pos_x[i] += enemy_pos_x_change[i]

        if enemy_pos_x[i] <= 0:
            enemy_pos_x_change[i] = 4
            enemy_pos_y[i] += enemy_pos_y_change[i]
        elif enemy_pos_x[i] >= 736:
            enemy_pos_x_change[i] = -4
            enemy_pos_y[i] += enemy_pos_y_change[i]

        # Game over
        if enemy_pos_y[i] > 440:
            for j in range(num_of_enemy):
                enemy_pos_y[j] = 2000
            game_over_text()
            break
        
        # Collosion
        collosion = isCollosion(enemy_pos_x[i], enemy_pos_y[i], bullet_pos_x, bullet_pos_y)
        if collosion:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_pos_y = 480
            bullet_state = "ready"
            score_value += 1
            
            enemy_pos_x[i] = random.randint(0, 735)
            enemy_pos_y[i] = random.randint(50, 150)

        enemy(enemy_pos_x[i], enemy_pos_y[i], i)

    # Bullet movement
    if bullet_pos_y <= 0:
        bullet_pos_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_pos_x, bullet_pos_y)
        bullet_pos_y -= bullet_pos_y_change

    # Display Score
    show_score(textX, textY)

    # Screen update
    pygame.display.update()