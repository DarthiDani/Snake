# Snake
import pygame
import sys
import time
import random

# Pygame Init
init_status = pygame.init()
if init_status[1] > 0:
print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
sys.exit()
else:
print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 320
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)
blue = pygame.Color(0, 0, 255) # Color for the enemy snake

# FPS controller
fpsController = pygame.time.Clock()

# Game settings
delta = 10
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]
foodPos = [400, 50]
foodSpawn = True
direction = 'RIGHT'
changeto = ''
score = 0
difficulty = 1 # 1: Easy, 2: Medium, 3: Hard

# Enemy snake settings
enemyPos = [0, 0] # Starting at top-left corner
enemyBody = [[0, 0], [10, 0], [20, 0]] # Initial size of the enemy snake
enemyDirection = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

# Game Over
def gameOver():
myFont = pygame.font.SysFont('monaco', 72)
GOsurf = myFont.render("Game Over", True, red)
GOrect = GOsurf.get_rect()
GOrect.midtop = (320, 25)
playSurface.blit(GOsurf, GOrect)
showScore(0)
pygame.display.flip()
time.sleep(4)
mainMenu()

# Show Score
def showScore(choice=1):
SFont = pygame.font.SysFont('monaco', 32)
Ssurf = SFont.render("Score : {0}".format(score), True, black)
Srect = Ssurf.get_rect()
if choice == 1:
Srect.midtop = (80, 10)
else:
Srect.midtop = (320, 100)
playSurface.blit(Ssurf, Srect)

# Main Menu
def mainMenu():
while True:
playSurface.fill(green)
myFont = pygame.font.SysFont('monaco', 50)
titleSurf = myFont.render("Snake Game", True, black)
playSurface.blit(titleSurf, (200, 50))

menuFont = pygame.font.SysFont('monaco', 30)
playSurf = menuFont.render("Press P to Play", True, black)
exitSurf = menuFont.render("Press E to Exit", True, black)
settingsSurf = menuFont.render("Press S for Settings", True, black)

playSurface.blit(playSurf, (200, 150))
playSurface.blit(exitSurf, (200, 200))
playSurface.blit(settingsSurf, (200, 250))

pygame.display.flip()

for event in pygame.event.get():
if event.type == pygame.QUIT:
pygame.quit()
sys.exit()
if event.type == pygame.KEYDOWN:
if event.key == pygame.K_p:
gameLoop()
if event.key == pygame.K_e:
pygame.quit()
sys.exit()
if event.key == pygame.K_s:
settingsMenu()

# Settings Menu
def settingsMenu():
global difficulty
while True:
playSurface.fill(white)
myFont = pygame.font.SysFont('monaco', 50)
settingsSurf = myFont.render("Settings", True, black)
playSurface.blit(settingsSurf, (220, 50))

menuFont = pygame.font.SysFont('monaco', 30)
easySurf = menuFont.render("Press 1 for Easy", True, black)
mediumSurf = menuFont.render("Press 2 for Medium", True, black)
hardSurf = menuFont.render("Press 3 for Hard", True, black)
backSurf = menuFont.render("Press B to go Back", True, black)

playSurface.blit(easySurf, (200, 150))
playSurface.blit(mediumSurf, (200, 200))
playSurface.blit(hardSurf, (200, 250))
playSurface.blit(backSurf, (200, 300))

pygame.display.flip()

for event in pygame.event.get():
if event.type == pygame.QUIT:
pygame.quit()
sys.exit()
if event.type == pygame.KEYDOWN:
if event.key == pygame.K_1:
difficulty = 1
elif event.key == pygame.K_2:
difficulty = 2
elif event.key == pygame.K_3:
