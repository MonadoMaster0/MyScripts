import pygame, sys
from pygame.math import Vector2 as vec2
import random, time
from debug import debug

from objects import *
from SETTINGS import *

pygame.init()


bricks = [Ground((i,j)) for i in range(0,W,20) for j in range(H-6*20,H,20)]
floor = pygame.sprite.Group()
floor.add(bricks)
floor.add(Ground((W//4,H-7*20)))

bombs = pygame.sprite.Group()
bombs.add(Bomb())

all_sprites = pygame.sprite.Group()
player = Player(START_POS)
all_sprites.add(player)
all_sprites.add(floor)
all_sprites.add(bombs)

clock = pygame.time.Clock()
pygame.time.set_timer(ADDBOMB, 500)

def mainLoop():

    run = True
    prev_time = time.time()

    while run:
        clock.tick(FPS)
        Dt = time.time() - prev_time
        prev_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == ADDBOMB:
                bombs.add(Bomb())
                pass
            player.jump(Dt, event)
        
        
        keys = pygame.key.get_pressed()
        SCREEN.fill(COLOR1)
        for ent in all_sprites:
            SCREEN.blit(ent.surf, ent.rect)
        for b in bombs:
            SCREEN.blit(b.surf,b.rect)

        for b in bombs:
            f = pygame.sprite.spritecollideany(b,floor)
            if f:
                f.kill()
                b.kill()
        
        debug(SCREEN, ("y-speed: ",player.dy), ("x-speed: ",player.dx))
        player.update(Dt, keys, floor, bombs, SCREEN)
        bombs.update(Dt, bombs, floor)
        
        


        pygame.display.update()
mainLoop()
pygame.quit()