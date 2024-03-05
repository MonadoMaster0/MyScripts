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
GRAV = 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.size = (20,40)
        self.surf = pygame.Surface(self.size)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(midbottom=pos)
        self.vel = vec2(0,0)
        self.ddx = 0
        self.dx = 0
        self.dy = 0
        self.canJump = True
        self.kickR = 30  
    
    def Jump(self, event):
        if self.canJump:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.dy+= -15
            if event.type == pygame.KEYUP:
                self.canJump = False
                if event.key == pygame.K_SPACE:
                    self.dy *= 0.5
                # if event.key == pygame.K_a:
                #     self.dxx = 1
                # if event.key == pygame.K_d:
                #     self.dxx = -1


    def update(self, key, floor: pygame.sprite.Sprite, bombs: pygame.sprite.Sprite, screen):
        kickmode = False

        ### Gravity
        # self.rect.center += self.vel
        self.dy+=GRAV

        ### Movement
        if key[pygame.K_a]:
            self.dx=-5
        elif key[pygame.K_d]:
            self.dx=+5

        # ### JUMP
        # if key[pygame.K_SPACE] and self.canJump:
        #     self.dy += -15
        #     self.canJump = False

        ### Collisions
        for tile in floor:
            # y direction
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                # # Collision with cieling
                # if self.vel.y < 0:
                #     self.dy = tile.rect.bottom - self.rect.top
                #     self.vel.y = 0
                # Collision with ground
                if self.vel.y > 0:
                    self.dy = tile.rect.top - self.rect.bottom
                    self.canJump = True
            # x direction
            if tile.rect.colliderect(self.rect.x+self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0

        ### Stay in screen
        if self.rect.left + self.dx < 0 or self.rect.right + self.dx > W:
            self.dx=0
        
        ### Kick
        for b in bombs:
            m = pygame.mouse.get_pos()
            mk = pygame.mouse.get_pressed(3)

            inKickRange = (vec2(self.rect.center)-vec2(b.rect.center)).length() < self.kickR
            if inKickRange and mk[0]:
                kickmode = True
                b.switch()
                self.dy = 0.1
                self.dx *= 0.1
                pygame.draw.line(screen, (255,100,0), b.rect.center, m)
                if mk[2]:
                    b.vel = (vec2(m)-vec2(b.rect.center)).normalize()*10
            elif inKickRange and not mk[0]:
                b.switch(revert=1)
                kickmode = False

        ### Updates
        self.dx+=self.ddx
        self.vel.y=self.dy
        self.vel.x=self.dx
        self.rect.center+=self.vel

        return kickmode

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
        self.type = "basic"
        self.pos = (random.randint(10,W-10), -20)
        self.size = (20,20)
        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surf.convert_alpha()
        self.surf.fill((255,255,255,0))
        self.rect = self.surf.get_rect(center=self.pos)
        self.vel = vec2(0,1)
        self.detR = 21
        self._switch = False
    
    def switch(self, revert = False):
        self.vel.y = 0
        self._switch = True
        if revert:
            self.vel.y = 1
            self._switch = False

    def update(self, mode, bombs, floor):
        if not self._switch:
            if mode:
                self.vel.y = 0.1
            elif not mode:
                self.vel.y = 1
        pygame.draw.circle(self.surf, (255,0,0,255), (10,10), 10)
        if self.rect.top > H:
            self.kill()
        
        ## Bombs collision
        for b in bombs:
            for bb in bombs:
                if bb != b:
                    if b.rect.colliderect(bb):
                        b.kill()
                        bb.kill()
            f = pygame.sprite.spritecollideany(b,floor)
            if f:
                f.kill()
                b.kill()

        self.rect.center+=self.vel

### pre-loop variables
bricks = [Ground((i,j)) for i in range(0,W,20) for j in range(H-6*20,H,20)]
floor = pygame.sprite.Group()
floor.add(bricks)
floor.add(Ground((W//4,H-7*20)))

bombs = pygame.sprite.Group()
# bombs.add(Bomb())

all_sprites = pygame.sprite.Group()
player = Player((W//2,H-6*20))
all_sprites.add(player)
all_sprites.add(floor)
all_sprites.add(bombs)

clock = pygame.time.Clock()
pygame.time.set_timer(ADDBOMB, 2000)

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
            player.Jump(event)
        
        
        keys = pygame.key.get_pressed()
        SCREEN.fill(COLOR1)
        for ent in all_sprites:
            SCREEN.blit(ent.surf, ent.rect)
        for b in bombs:
            SCREEN.blit(b.surf,b.rect)


        
        bombMode = player.update(keys, floor, bombs, SCREEN)
        bombs.update(bombMode, bombs, floor)
        


        pygame.display.update()
mainLoop()
pygame.quit()