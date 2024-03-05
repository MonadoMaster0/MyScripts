import pygame, sys, random
from pygame import Vector2 as vector

pygame.init()

SCREEN = WIDTH, HEIGHT = 800, 600
FPS = 60
B_SIZE = 20
BALL_VEL = 6
PLAYER_VEL = BALL_VEL+4

def dist2(rect_1:tuple, rect_2:tuple):
    return ((rect_1[0]-rect_2[0])**2 + (rect_1[1]-rect_2[1])**2)

class game:
    def __init__(self) -> None:
        self.fullscreen = False
        self.screen = pygame.display.set_mode(SCREEN)
        self.clock = pygame.time.Clock()
        self.bricks = pygame.sprite.Group()
        self.gen = True
    
    def brickGen(self):
        if self.gen:
            for row in range(HEIGHT//B_SIZE//3):
                for col in range(WIDTH//B_SIZE):
                    hp_weight = [60,20*1/(row+1),15*1/(row+1),5*1/(row+1)]
                    self.bricks.add(bricks((col*B_SIZE,row*B_SIZE), random.choices([1,2,3,4],weights=hp_weight,k=1)[0]))
            self.gen = False
        self.bricks.update()
        self.bricks.draw(self.screen)
        self.kill_brick()
        
    def kill_brick(self):
        for brick in self.bricks.sprites():
            if brick.hp <= 0:
                self.bricks.remove(brick)

    def __call__(self):

        # Objects
        bll = Ball((WIDTH//2,HEIGHT//2))
        player = plate()

        # Main loop
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if self.fullscreen == False:
                            self.screen = pygame.display.set_mode(SCREEN, pygame.FULLSCREEN | pygame.SCALED)
                            self.fullscreen = True
                        elif self.fullscreen:
                            self.screen = pygame.display.set_mode(SCREEN)
                            self.fullscreen = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.brickGen()
            bll.handler(self.screen, self.bricks.sprites(), player)
            player.handler(self.screen)

            pygame.display.update()

class Ball:
    def __init__(self, startpos:tuple) -> None:
        self.pos = vector(startpos)
        self.flat_vel = BALL_VEL
        self.vel = vector(0,-BALL_VEL)
        self.radius = 10
    
    def draw(self, screen):
        self.rect = pygame.draw.circle(screen,'white', self.pos, self.radius)
    
    def move(self):
        if self.pos.x <= self.radius or self.pos.x+self.radius >= WIDTH:
            self.vel.x *= -1
        if self.pos.y <= self.radius or self.pos.y+self.radius >= HEIGHT:
            self.vel.y *= -1
        self.vel = self.vel.normalize()*self.flat_vel
        self.pos += self.vel
    
    def collision(self, objs):
        for brick in objs:
            if self.rect.colliderect(brick):
                
                distances = {
                    'left':dist2(self.pos, brick.rect.midleft),
                    'right':dist2(self.pos, brick.rect.midright),
                    'top':dist2(self.pos,brick.rect.midtop),
                    'bottom':dist2(self.pos, brick.rect.midbottom)
                }

                keys = list(distances.keys())
                vals = list(distances.values())
                side = keys[vals.index(min(vals))]
                
                
                if side == 'bottom':
                    self.vel.y = abs(self.vel.y)
                if side == 'top':
                    self.vel.y = -abs(self.vel.y)
                if side == 'left':
                    self.vel.x = -abs(self.vel.x)
                if side == 'right':
                    self.vel.x = -abs(self.vel.x)

                print(side)
                
                brick.hp -= 1

                  
    def plate_coll(self, plate):
        if self.rect.colliderect(plate.rect):
            self.vel.x += (self.pos.x-plate.rect.centerx)//12
            self.vel.y *= -1

    def handler(self, screen, objs, plate):
        self.move()
        self.draw(screen)
        self.collision(objs)
        self.plate_coll(plate)

class bricks(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, hp:int):
        super().__init__()
        self.image = pygame.Surface((B_SIZE,B_SIZE))
        self.colorlist = ['white', 'yellow', 'orange', 'red'] 
        self.hp = hp
        self.image.fill(self.colorlist[self.hp-1])
        self.rect = self.image.get_rect(topleft=pos)
        self.color = self.colorlist[self.hp-1]
    
    def update(self):
        self.color = self.colorlist[self.hp-1]
        self.image.fill(self.color)
        return super().update()

class plate:
    def __init__(self):
        self.image = pygame.Surface((100, 10))
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT))
        self.image.fill('white')
        self.vel = vector()
        self.flat = PLAYER_VEL

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.vel = vector(-self.flat, 0)
        elif keys[pygame.K_d] and self.rect.right < WIDTH:
            self.vel = vector(self.flat, 0)
        else:
            self.vel = vector(0,0)
        self.rect.midbottom += self.vel
    
    def handler(self, screen):
        self.draw(screen)
        self.controls()

if __name__ == '__main__':
    main = game()
    main()