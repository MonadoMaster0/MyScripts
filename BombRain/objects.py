import pygame
import random
from pygame.math import Vector2 as vec2
from SETTINGS import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.size = (20,20)
        self.surf = pygame.Surface(self.size)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(topleft=pos)
        
# class Bomb(pygame.sprite.Sprite):
#     def __init__(self) -> None:
#         super().__init__()
#         self.pos = (random.randint(10,W-10), -20)
#         self.size = (20,20)
#         self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
#         self.surf.convert_alpha()
#         self.surf.fill((255,255,255,0))
#         self.rect = self.surf.get_rect(center=self.pos)
#         self.vel = vec2(0,1)
    
#     def switch(self, mode):
#         if mode:
#             self.dy = 0

#     def update(self):
#         self.rect.center+=self.vel
#         pygame.draw.circle(self.surf, (255,0,0,255), (10,10), 10)
#         if self.rect.top > H:
#             self.kill()

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
        self.baseSpeed = BASIC_BOMB_SPEED
        self.pos = vec2(self.rect.topleft)
        self.dy = self.baseSpeed
        self.dx = 0
        self.detR = 21
        self._switch = False
        self.act = vec2()
        self.detonate = False
    
    def switch(self, revert = False):
        self._switch = True
        if revert:
            self._switch = False
    
    def activate(self, vec: vec2):
        self.act = vec
        self.detonate = True


    def update(self, Dt, bombs, floor):
        self.dy = self.baseSpeed * Dt
        if self._switch:
            self.dy = 0
        
        if self.detonate:
            self.dy = self.act.y * 100 * Dt
            self.dx = self.act.x * 100 * Dt

        # kill if out of bounds
        if self.rect.top > H or self.rect.right > W or self.rect.left < 0:
            self.kill()
        
        ## Bombs collision
        for b in bombs:
            # Collide with bomb
            for bb in bombs:
                if bb != b:
                    if b.rect.colliderect(bb):
                        b.kill()
                        bb.kill()
            # Collide with floor
            f = pygame.sprite.spritecollideany(b,floor)
            if f:
                f.kill()
                b.kill()
        
        # Update position
        self.pos.y += round(self.dy)
        self.pos.x += round(self.dx)
        self.rect.topleft = self.pos
        pygame.draw.circle(self.surf, (255,0,0,255), (10,10), 10)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.size = (20,40)
        self.surf = pygame.Surface(self.size)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(midbottom=pos)
        self.vel = vec2(0,0)
        self.grav = True
        self.canJump = True
        self.dx = 0
        self.dy = 0
        self.dyy = 0
        self.dxx = 0
        self.pos = vec2(self.rect.topleft)
        self.x_vel = MOVE_VEL
        self.j_vel = JUMP_ACC
        
    def jump(self, Dt, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and self.canJump:
            if event.key == pygame.K_SPACE:
                self.canJump = False
                self.x_vel *= 0.5
                self.dy += self.j_vel *Dt
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.dy < 0:
                self.dy = self.dy*0.5
    
    def _collBlock(self, Dt, floor: pygame.sprite.Group):
        onG = False
        for b in floor:
            if b.rect.colliderect(self.rect.x+self.dx,self.rect.y+self.dy,self.rect.width,self.rect.height):
                ### Colliding with ground
                if self.dy >= 0:
                    self.x_vel = MOVE_VEL
                    onG = True
                    self.canJump = True
                    # if (b.rect.top - self.rect.bottom) > -5:
                    self.dy = (b.rect.top -self.rect.bottom) * Dt
                ### Colliding with block side
                if abs(self.dx) > 0:
                    self.dx = 0
        ### Colliding with screen side
        if W < self.rect.right + self.dx:
            self.dx = (W-self.rect.right)
        elif self.rect.left + self.dx <= 0:
            self.dx = self.rect.left
        return onG
    
    def kick(self, Dt, screen, bombs: pygame.sprite.Group):
        ### Kick
        for b in bombs:
            m = pygame.mouse.get_pos()
            mk = pygame.mouse.get_pressed(3)

            inKickRange = (vec2(self.rect.center)-vec2(b.rect.center)).length() < BASE_KICKRANGE
            if inKickRange and mk[0]:
                b.switch()
                for o in bombs:
                    o.switch()
                self.dy = 0
                self.dx = 0
                pygame.draw.line(screen, (255,100,0), b.rect.center, m)
                if mk[2]:
                    vel = (vec2(m)-vec2(b.rect.center)).normalize()*10
                    b.activate(vel)
                    for o in bombs:
                        o.switch(revert=1)
            # elif inKickRange and not mk[0]:
                
            
            

    def update(self, Dt, key, floor, bombs, screen):
        
        if key[pygame.K_a]:
            self.dx = -self.x_vel *Dt
        if key[pygame.K_d]:
            self.dx = self.x_vel *Dt
        
        onGround = self._collBlock(Dt, floor)

        if not onGround:
            self.dy += GRAV * Dt

        self.kick(Dt, screen, bombs)
        self.pos.x += round(self.dx)
        self.pos.y += round(self.dy)
        self.rect.topleft = self.pos