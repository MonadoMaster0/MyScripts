import sys
import random
import pygame
from pygame.math import Vector2

pygame.init()
pygame.font.init()
text = pygame.font.SysFont('courier', 16)


TILE_SIZE = 16
WIDTH,HEIGHT = 32, 32
FPS = 60

class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE))
        self.overlay = pygame.Surface((WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE)).convert_alpha()
        self.overlay.set_colorkey('green')
        self.overlay.fill('green')
        self.overlay.set_alpha(30)
        self.clock = pygame.time.Clock()
        self.alive = True
        self.score = 0

    def run(self):
        Snake = Snek()
        fruit = Fruit()
        global SCREEN_UPDATE
        SCREEN_UPDATE = pygame.USEREVENT
        global MOVE_SNAKE
        MOVE_SNAKE = pygame.USEREVENT
        pygame.time.set_timer(MOVE_SNAKE, 20)
        pygame.time.set_timer(SCREEN_UPDATE, 200)
        while True:
            if self.alive:
                self.clock.tick(FPS)
                global movings
                movings = False
                self.eventLoop(
                    Snake.startSnek
                )
                self.screen.fill('black')
                self.screen.blit(self.overlay,(0,0))
                self.grid()
                
                # Fruit handlers
                fruit.drawFruit(self.screen, Snake)
                if self.alive == False:
                    fruit.reset()

                # Snake handlers
                Snake.move(self.screen)
                Snake.controls()
                if movings and Snake.velvec != Vector2(0,0):
                    Snake.moveHandler()
                self.gameOver(Snake)

                # Score
                self.Score(self.score)
                self.score = Snake.fruitPickup(fruit)
                
            else:
                self.alive = False
                self.clock.tick(FPS)
                self.eventLoop(
                    Snake.startSnek
                )
                self.screen.fill('black')
                self.screen.blit(self.overlay,(0,0))
                Snake.move(self.screen)
                self.grid()
                self.gameOverActive(Snake)

            pygame.display.update()

    def Score(self, points):
        kurva = text.render(f'Score: {int(points)-3}', True, '#bbbb00')
        anyad = kurva.get_rect(topright=((WIDTH*TILE_SIZE-20),20))
        self.screen.blit(kurva, anyad)

    def gameOver(self, snek):
        if snek.body_pos[0].x > WIDTH*TILE_SIZE or snek.body_pos[0].x < 0 or snek.body_pos[0].y > HEIGHT*TILE_SIZE or snek.body_pos[0].y < 0:
            snek.gameOver = True 
            self.alive = False
        checkBite = [x for x in snek.body_pos if snek.body_pos.count(x) == 1]
        if len(snek.body_pos) != len(checkBite):
            self.alive = False
    
    def gameOverActive(self, snek):
        gameOverText = text.render('GAME OVER!', True, '#ffaa00')
        gameOverText_rect = gameOverText.get_rect(center=(WIDTH*TILE_SIZE//2,HEIGHT*TILE_SIZE//2))
        self.screen.blit(gameOverText, gameOverText_rect)
        finalScore = text.render(f'Your score is: {self.score-3}', True, '#ffaa00')
        finalRect = finalScore.get_rect(center=(WIDTH*TILE_SIZE//2,HEIGHT*TILE_SIZE//2+50))
        self.screen.blit(finalScore,finalRect)
        gameOverText = text.render('Press SPACE to play again...', True, '#ffaa00')
        gameOverText_rect = gameOverText.get_rect(center=(WIDTH*TILE_SIZE//2,HEIGHT*TILE_SIZE//2+100))
        self.screen.blit(gameOverText, gameOverText_rect)
        snek.Death()
        self.alive = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.alive = True
            snek.__init__()

    def grid(self):
        for col in range(WIDTH):
            pygame.draw.aaline(self.overlay, 'white', (col*TILE_SIZE, 0), (col*TILE_SIZE, HEIGHT*TILE_SIZE))
        for row in range(HEIGHT):
            pygame.draw.aaline(self.overlay, 'white', (0, row*TILE_SIZE), (WIDTH*TILE_SIZE, row*TILE_SIZE))

    def eventLoop(self, *funcs):
        for event in pygame.event.get():
            for func in funcs:
                func(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                global movings
                movings = True

class Snek:
    def __init__(self):
        self.pos = Vector2(16*16, 16*16)
        self.body_pos = [self.pos, self.pos.copy()-Vector2(1*TILE_SIZE, 0), self.pos.copy()-Vector2(2*TILE_SIZE, 0)]
        self.velvec = Vector2()
        self.vel = 16
        self.started = 0
        self.body = []
        self.moving = False
        self.rect = self.body[1] if len(self.body) else None

    def Death(self):
        self.vel = Vector2(0,0)

    def startSnek(self, event):
        if event.type == pygame.KEYDOWN and self.started != 1:
            self.started += 1
        if event.type == MOVE_SNAKE:
            self.moving = True
        else: self.moving = False

    def move(self, Screen):
        if self.started and self.velvec == Vector2(0,0):
            self.velvec= Vector2(self.vel, 0)
        for ind, block in enumerate(self.body_pos):
            if ind == 0:
                self.rect = (pygame.draw.rect(Screen, 'Blue', (block.x, block.y, 16, 16)))
                self.body.append(pygame.draw.rect(Screen, 'Blue', (block.x, block.y, 16, 16)))
            else:
                self.body.append(pygame.draw.rect(Screen, 'Blue', (block.x, block.y, 16, 16)))
    
    def controls(self):
        key = pygame.key.get_pressed()

        if self.started == 1:
            if key[pygame.K_d] and self.velvec != Vector2(-self.vel, 0):
                self.velvec = Vector2(self.vel, 0)
            elif key[pygame.K_a]and self.velvec != Vector2(self.vel, 0):
                self.velvec = Vector2(-self.vel, 0)
            elif key[pygame.K_s] and self.velvec != Vector2(0, -self.vel):
                self.velvec = Vector2(0, self.vel)
            elif key[pygame.K_w] and self.velvec != Vector2(0, self.vel):
                self.velvec = Vector2(0, -self.vel)


        
    def fruitPickup(self, fruit) -> int:
        if self.rect.colliderect(fruit.rect):
            fruit.reset()
            self.body_pos.append(self.body_pos[-1] + (self.body_pos[-1]-self.body_pos[-2]))
        return int(len(self.body_pos))

    def moveHandler(self):
        copy = self.body_pos[:-1]
        copy.insert(0, self.body_pos[0] + self.velvec)
        self.body_pos = copy[:]
        

class Fruit:
    def __init__(self):
        self.pos = Vector2(
            random.choice(range(0,WIDTH*TILE_SIZE,16))+8,
            random.choice(range(0,HEIGHT*TILE_SIZE,16))+8
        )
    
    def reset(self):
        self.__init__()

    def drawFruit(self, Screen, snake):
        self.rect = pygame.draw.circle(Screen, 'Red', self.pos, 8)
    
    def posRandomizer(self):

        self.pos = Vector2(
            random.choice(range(0,WIDTH,16))+8,
            random.choice(range(0,HEIGHT,16))+8
        )




if __name__ == '__main__':
    window = game()
    window.run()
