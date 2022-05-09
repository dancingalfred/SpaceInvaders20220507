import random
import math
import pygame
from pygame import mixer


#Initialize the pygame
pygame.init()

#Background
background = pygame.image.load("background.png")

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Create a screen
screen = pygame.display.set_mode((800,600))

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0


#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.25)
    enemyY_change.append(40)


#Laser
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 0.5
#ready - You cant see the laser on the screen
#fire - The laser is currently moving
laser_state = "ready"

#Font
score_value = 0
font = pygame.font.Font('VECTRO-Bold.otf', 42)
textX = 600
textY = 10

#Game Over text
game_over_font = pygame.font.Font('VECTRO-Bold.otf', 64)



#Functions

def show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text, (270,250))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x,y))
    
def fire_laser(x,y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))



def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.hypot(enemyX - laserX, enemyY - laserY)
    # distance = math.sqrt(math.pow(enemyX - laserX, 2) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False





#Game loop
running = True
while running:

    #RGB - red, Green, Blue
    screen.fill((0,0,0))
    #Background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if keystroke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            # print("Left arrow is pressed")
            playerX_change = -0.2
        if event.key == pygame.K_RIGHT:
            # print("Right arrow is pressed")
            playerX_change = 0.2   
        if event.key == pygame.K_UP:
            if laser_state == "ready":
                laser_sound = mixer.Sound('laser.wav')
                laser_sound.play()
                laserX = playerX
                fire_laser(laserX,laserY)    
        
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            # print("Keystroke has been released")
            playerX_change = 0  


    #player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0       
    elif playerX >= 736:
        playerX = 736

    #enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i] 

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.25
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.25
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #Laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

 
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


