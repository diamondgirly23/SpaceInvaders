import pygame
import random
import math
from pygame import mixer
pygame.init()
collision = False
# Screen creation
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load("stuff//background.png")
#background sound
#Dont need to initialize mixer because the pygame.init() does it for me.
mixer.music.load("stuff//background.wav")
mixer.music.set_volume(.4)
mixer.music.play(-1)
# Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("stuff//ufo.png")
pygame.display.set_icon(icon)
# Player
playerimg = pygame.image.load("stuff//player.png")
playerx = 370
playery = 480
playerx_change = 0
# enemy
enemyimg = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemy_y_change = []
num_of_enemies = 7
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("stuff//alien.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(2)
    enemy_y_change.append(40)
# bullet
# ready - u cant see bullet
# fire, bullet moving
bulletimg = pygame.image.load("stuff//bullet.png")
bullet_x = 0
bullet_y = 480
bulletx_change = 0
bullety_change = 10
#This variable is being used more as a ENUM than as an actual string value.
bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10
clock = pygame.time.Clock()
#game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)
# Positioning starting position of player
def showscore(x, y):
    score = font.render("score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))
def game_over_text():
    over_text = font.render("GAME OVER: SCORE WAS:" + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    pygame.mixer.pause()
#blit means moving the image based on the new x y values it is given, if its 3,3 it will move the character 3 on the x 3 on the y than where it currently is.
def player(x, y):
    screen.blit(playerimg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))
    
#This function isntd used.
def aliencollision(enemyx1,enemyx2,enemyy1,enemyy2):
    
    distance1 = math.sqrt((math.pow(enemyx1 - enemyx2, 2)) + (math.pow(enemyy1 - enemyy2, 2)))
    if distance1 < 29:
        return True
    else:
        return False
def iscollision(enemyx, enemyy, bulletx, bullety):
    #determining if the bullet touches the enemy hitbox
    distance = math.sqrt((math.pow(bulletx - enemyx, 2)) + (math.pow(bullety - enemyy, 2)))
    if bullet_state is not "fire":
        return False
    if distance < 40:
        return True
    else:
        return False
# Game Loop
running = True
while running:
    clock.tick(60)
    # RGB - red green blue
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))
    #There are a series of events that always run in pygame depending on the input, this will check for specific ones that trigger.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #KEYDOWN means when someone presses a key.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left arrow pressed")
                playerx_change = -3
            if event.key == pygame.K_RIGHT:
                print("Right arrow pressed")
                playerx_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("stuff//laser.wav")
                    bullet_sound.set_volume(.4)
                    bullet_sound.play()
                    bullet_x = playerx
                    fire_bullet(bullet_x, bullet_y)
        #KEYUP is when you stop pressing a key.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if playerx_change == -3:
                    playerx_change = 0
            if event.key == pygame.K_RIGHT:
                if playerx_change == 3:
                      playerx_change = 0
    # boundry check
    playerx += playerx_change
    if playerx <= -10:
        playerx = 750
    elif playerx >= 751:
        playerx = -9
    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change
    # enemy movement
    #all enemies are located in a single list, this allows me to be able to loop through the list each frame to determine the collision checks for each enemy.
    for i in range(num_of_enemies):
        #game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        enemy_x[i] += enemyx_change[i]
        #These if and elif statements check if the enemy has reached the edge of the screen, if they have it will reverse the direction and move them down
        #according to the enemy_y change variable.
        if enemy_x[i] <= 0:
            enemy_x[i] = 0
            enemyx_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x[i] = 736
            enemyx_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]
            # collision with bullet. send the current enemy in the loop coordinate and the bullet coordinate to compare distances with.
        collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            #Makes the sound then adds the points to the score.
            explosion_sound = mixer.Sound("stuff//explosion.wav")
            explosion_sound.set_volume(.4)
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 50
            print(score_value)
            #Inserts the enemy into a new random location between specific coordinates on each axis.
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
            #This makes it so each time you kill an enemy it gets slightly faster.
            enemyx_change[i] *= 1.05
        enemy(enemy_x[i], enemy_y[i], i)
    player(playerx, playery)
    showscore(textx,texty)
    pygame.display.update()