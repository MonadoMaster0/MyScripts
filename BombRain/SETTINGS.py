import pygame

RES = W,H = 800,600
SCREEN = pygame.display.set_mode(RES)
COLOR1 = (100,100,100)
COLOR2 = (200,200,0)
FPS = 60

# Player variables
START_POS = (W//2,H-6*20)
GRAV = 15
JUMP_ACC = -800
MOVE_VEL = 500
BASE_KICKRANGE = 40

# Bomb variables
BASIC_BOMB_SPEED = 60

# Events
ADDBOMB = pygame.USEREVENT+1