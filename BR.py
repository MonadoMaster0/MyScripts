import pygame
from pygame.math import Vector2 as vec2
import random

### Constants
pygame.init()
RES = W,H = 800,600
SCREEN = pygame.display.set_mode(RES)
COLOR1 = (100,100,100)
COLOR2 = (200,200,0)
FPS = 60
relScr = rW,rH = W//2, H//2
ADDBOMB = pygame.USEREVENT+1


class Ground(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.size = (20,20)
        self.surf = pygame.Surface(self.size)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(topleft=pos)
        
class Bomb(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.pos = (random.randint(10,W-10), -20)
        self.size = (20,20)
        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surf.convert_alpha()
        self.surf.fill((255,255,255,0))
        self.rect = self.surf.get_rect(center=self.pos)
        self.vel = vec2(0,1)
        
    def update(self):
        self.rect.center+=self.vel
        pygame.draw.circle(self.surf, (255,0,0,255), (10,10), 10)
        if self.rect.top > H:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.size = (20,40)
        self.surf = pygame.Surface(self.size)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(midbottom=pos)
        self.vel = vec2(0,0)
        self.grav = vec2(0,1)
        self.canJump = True
        self.R = True
        self.L = True
        self.yAcc = 0
        self.onGround = True
        
    
    def update(self, key):
        self.rect.center += self.vel
        if not self.onGround:
            self.vel+=self.grav
        if key[pygame.K_a] and self.L:
            self.vel.x=-5
        if key[pygame.K_d] and self.R:
            self.vel.x=+5

        ##JUMP
        if key[pygame.K_w] and self.canJump:
            self.onGround = False
            self.canJump = False
            self.vel.y = -15
        self.L = True
        self.R = True

        
        if W < self.rect.right:
            self.rect.right = W
        elif self.rect.left < 0:
            self.rect.left = 0

        ### Slowdown after release
        if self.vel.x<0:
            self.vel.x+=1
        if self.vel.x>0:
            self.vel.x-=1

    def collideWall(self, floor: pygame.sprite.Group):
        for f in floor:
            if pygame.sprite.collide_rect(f,self):
                self.rect.center-=self.vel
                self.canJump = True
                self.onGround = True
                self.vel.y=0


### pre-loop variables
bricks = [Ground((i,j)) for i in range(0,W,20) for j in range(H-6*20,H,20)]
floor = pygame.sprite.Group()
floor.add(bricks)
floor.add(Ground((W//4,H-7*20)))

bombs = pygame.sprite.Group()
bombs.add(Bomb())

all_sprites = pygame.sprite.Group()
player = Player((W//2,H-6*20))
all_sprites.add(player)
all_sprites.add(floor)
all_sprites.add(bombs)

clock = pygame.time.Clock()
pygame.time.set_timer(ADDBOMB, 500)

def mainLoop():

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == ADDBOMB:
                bombs.add(Bomb())
                # pass
        
        
        keys = pygame.key.get_pressed()
        SCREEN.fill(COLOR1)
        bombs.update()
        for ent in all_sprites:
            SCREEN.blit(ent.surf, ent.rect)
        for b in bombs:
            SCREEN.blit(b.surf,b.rect)

        for b in bombs:
            f = pygame.sprite.spritecollideany(b,floor)
            if f:
                f.kill()
                b.kill()
        
        player.update(keys)
        player.collideWall(floor)
        


        pygame.display.update()
mainLoop()
pygame.quit()