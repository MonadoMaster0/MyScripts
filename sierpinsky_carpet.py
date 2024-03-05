import sys, random, pygame
from pygame.math import Vector2 as vector

WIDTH, HEIGHT = WINSIZE = 1280, 720
FPS = 60
pygame.init()
SCREEN = pygame.display.set_mode(WINSIZE)

def draw_rect(screen: pygame.Surface, pos):
    surf = pygame.surface.Surface((800,800))
    surf.fill('white')
    rect = surf.get_rect(topleft=pos)
    screen.blit(surf, rect)
    return surf

def draw_rp(points: list, size):
    rm_x = random.random()
    rm_y = random.random()
    st_point = points[0]
    return (st_point[0]+size*rm_x, st_point[1]+size*rm_y)

def generate_sier(corners: list, size):
    rm_point = vector(draw_rp(corners, size))
    rm_corner = vector(random.choice(corners))
    points = []
    for _ in range(100000):
        p = rm_point+(rm_corner-rm_point)/2
        points.append(p)
        rm_point = p
        prev_corner = rm_corner
        while prev_corner == rm_corner:
            rm_corner = random.choice(corners)
    return points

def drawpoints(screen: pygame.surface,points: list):
    for point in points:
        pygame.draw.circle(screen, 'black', point, 1)


def main():
    rect_size = 800
    st_point = (240, 114)
    corners = [st_point, (st_point[0]+rect_size,st_point[1]), (st_point[0],st_point[1]+rect_size), (st_point[0]+rect_size,st_point[1]+rect_size)]
    sier_points = generate_sier(corners, rect_size)
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        SCREEN.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        rectangle = draw_rect(SCREEN, (240, 114))
        for point in sier_points:
            pygame.draw.circle(SCREEN, 'black', point, 1)
        



        pygame.display.update()

main()