import random
import pygame
from pygame.math import Vector2 as vector
import sys

pygame.init()
pygame.font.init

WINSIZE = WIDTH, HEIGHT = 800, 800

def point_on_triangle(pt1, pt2, pt3):
    """
    Random point on the triangle with vertices pt1, pt2 and pt3.
    (Barycentric coordinates)
    """
    x, y = sorted([random.random(), random.random()])
    s, t, u = x, y - x, 1 - y
    return (s * pt1[0] + t * pt2[0] + u * pt3[0],
            s * pt1[1] + t * pt2[1] + u * pt3[1])

class Triangle:
    def __init__(self) -> None:
        self.edgeLen = 600
        self.startpoint = vector(WIDTH//2, 100)
        self.tor = vector(0,self.edgeLen)
        self.leftpoint = self.startpoint+self.tor.rotate(-30)
        self.rightpoint = self.startpoint+self.tor.rotate(30)
        self.list = [self.startpoint, self.leftpoint, self.rightpoint]
        self.halfPoints = []
        self.curr = vector(point_on_triangle(self.list[0], self.list[1], self.list[2]))
    
    def drawBody(self, screen):
        self.rect = pygame.draw.polygon(screen, (255,255,255), [self.startpoint, self.leftpoint, self.rightpoint])

    def drawPoints(self, screen):
        rand = random.choice(self.list)
        vec = rand + self.curr
        self.curr = vec.normalize()*(vec.length()//2)
        if self.curr not in self.halfPoints:
            pygame.draw.circle(screen, '#777777', self.curr, 5)
            self.halfPoints.append(self.curr)
            for pos in self.halfPoints:
                pygame.draw.circle(screen, 'black', pos, 1)

def main():
    text = pygame.font.SysFont('cooper', 32, True)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Triangle')
    # icon = pygame.image.load('sierpinsky.png').convert()
    # pygame.display.set_icon(icon)
    tri = Triangle()
    while True:
        clock.tick(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        tri.drawBody(screen)
        tri.drawPoints(screen)
        particles = text.render(f'Particle Number: {len(tri.halfPoints)}', True, 'white')
        screen.blit(particles, (10,10))

        pygame.display.update()


# print(np.tan(30))
if __name__ == '__main__':
    main()