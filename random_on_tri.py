import pygame, sys, random
from pygame.math import Vector2 as vector
import math

WIDTH, HEIGHT = SCREEN_SIZE = 1280, 720
pygame.init()
pygame.font.init()
pygame.display.set_caption('Random point on triangle')
screen = pygame.display.set_mode(SCREEN_SIZE)

p1,p2,p3 = vector(100, HEIGHT//2), vector(1170, 80), vector(1100, HEIGHT-120)
text = pygame.font.SysFont('arial', 24, True)

def draw_triangle(p1,p2,p3, screen):
    pygame.draw.polygon(screen, 'black', [p1,p2,p3], 3)

def check_point_debug(a: vector,b: vector,c: vector, m):
    ab = b-a
    ac = c-a
    bc = c-b
    m = vector(m)
    am, bm, cm = m-a, m-b, m-c
    tri_area = -0.5*ab.length()*ac.length()*math.sin(math.radians(ac.angle_to(ab)))
    # Areas
    abm = -0.5*ab.length()*am.length()*math.sin(math.radians(am.angle_to(ab)))
    acm = -0.5*ac.length()*am.length()*math.sin(math.radians(ac.angle_to(am)))
    bcm = -0.5*bc.length()*bm.length()*math.sin(math.radians(bm.angle_to(bc)))
    return tri_area, abm, acm, bcm

def check_point(a: vector,b: vector,c: vector, m):
    ab = b-a
    ac = c-a
    bc = c-b
    m = vector(m)
    am, bm, cm = m-a, m-b, m-c
    tri_area = -0.5*ab.length()*ac.length()*math.sin(math.radians(ac.angle_to(ab)))
    # Areas
    abm = -0.5*ab.length()*am.length()*math.sin(math.radians(am.angle_to(ab)))
    acm = -0.5*ac.length()*am.length()*math.sin(math.radians(ac.angle_to(am)))
    bcm = -0.5*bc.length()*bm.length()*math.sin(math.radians(bm.angle_to(bc)))
    total = abs(abm)+abs(acm)+abs(bcm)
    on_triange = True if total == tri_area else False
    return on_triange

def vector_lines(a: vector, b: vector, c:vector, p: vector):
    ab = b-a
    ac = c-a
    w1 = (p.y*ac.x-a.y*ac.x-ac.y*p.x+ac.y*a.x)/(ab.y*ac.x-ac.y*ab.x)
    w2 = (p.x-a.x-ab.x*w1)/ac.x
    return w1, w2

def randompoints(a, b, c):
    ab = b-a
    ac = c-a
    points = []
    aa = 10
    for _ in range(3200):
        while aa >= 1:
            w11 = random.random()
            w22 = random.random()
            aa = w11+w22
        points.append(a+ab*w11+ac*w22)
    return points


# ab*w1 + ac*w2 = m
# area = check_coll(p1, p2, p3, (0,0))

def start():
    ab = p2-p1
    ac = p3-p1
    clock = pygame.time.Clock()
    points = []
    print(len(points))
    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill('white')
        draw_triangle(p1,p2,p3,screen)
        m_pos = pygame.mouse.get_pos()
        
        # generate random points
        if len(points) < 3200:
            a = 10
            while a >= 1:
                w11 = random.random()
                w22 = random.random()
                a = w11+w22
            points.append(p1+ab*w11+ac*w22)

        for point in points:
            pygame.draw.circle(screen, 'black', point, 2)

        w1, w2 = vector_lines(p1, p2, p3, vector(m_pos))
        if check_point(p1, p2, p3, m_pos):
            pygame.draw.line(screen, 'green', p1, m_pos, 1)
            pygame.draw.line(screen, 'blue', p1, p1+ab*w1, 3)
            pygame.draw.line(screen, 'red', p1+ab*w1, p1+ab*w1+ac*w2, 3)

        # Pointcheck params
        tri_area, abm, acm, bcm = check_point_debug(p1, p2, p3, m_pos)
        areas = text.render(f'Total Area:{tri_area:.2f} ABM: {abm:.2f}\n ACM: {acm:.2f}\n BCM: {bcm:.2f}\n TOTAL: {(abs(abm)+abs(acm)+abs(bcm)):.2f}', True, 'Black')
        areas_rect = areas.get_rect(topleft=(10,10))
        screen.blit(areas, areas_rect)
        # Scalars
        params = text.render(f'w1: {w1:.2f} w2: {w2:.2f}', True, 'black')
        params_rect = params.get_rect(topleft=areas_rect.bottomleft)
        screen.blit(params, params_rect)
        
        pygame.display.update()

start()