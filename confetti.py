import numpy as np
import pygame
import random

pygame.init()
pygame.font.init()

WIDHT, HEIGHT = 800, 600
FPS = 60
# Gravity 0.03
GRAV = 0.1
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Betha")
clock = pygame.time.Clock()
writer = pygame.font.SysFont('arial', 30)

def len_vector(vector):
    return (vector[0]**2+vector[-1]**2)**0.5

def norm(vector):
    return ((vector[0]/len_vector(vector),vector[1]/len_vector(vector)))

class ball:
    def __init__(self, x, y, radius, color, surf, theta, vel) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.surf = surf
        self.vel = vel
        self.vel_x = self.vel*np.cos(-(theta/180)*np.pi)
        self.vel_y = self.vel*np.sin(-(theta/180)*np.pi)

    def draw(self):
        self.rect = pygame.draw.circle(self.surf, self.color, (self.x, self.y), self.radius)
    
    def draw_vector(self):
        self.vector = pygame.draw.line(screen, '#ff0000', (self.x,self.y), (self.x+self.vel_x*10, self.y+self.vel_y*10), width=2)
    
    def collision(self, obj):
        # if abs(self.x-obj.x) < self.radius+obj.radius and abs(self.y-obj.y) < self.radius+obj.radius:
        if pygame.math.Vector2(abs(self.x-obj.x),abs(self.y-obj.y)).length() < self.radius+obj.radius:
            coll_vec =(self.x - obj.x, self.y - obj.y)
            vel_vec = (self.vel_x, self.vel_y)
            new_vec1 = (coll_vec[0]-vel_vec[0], coll_vec[-1]+vel_vec[-1])
            new_vec2 = (coll_vec[0]-vel_vec[0], coll_vec[-1]+vel_vec[-1])

            if len_vector(new_vec1) > len_vector(new_vec2):
                self.vel_x = norm(new_vec1)[0]*self.vel
                self.vel_y = norm(new_vec1)[-1]*self.vel
            else:
                self.vel_x = norm(new_vec2)[0]*self.vel
                self.vel_y = norm(new_vec2)[-1]*self.vel
            
    def movement(self):
        # Gravity
        if self.y < HEIGHT:
            self.vel_y += GRAV
        # Box
        if self.radius <= self.x <= WIDHT-self.radius and self.radius <= self.y <= HEIGHT-self.radius:
            pass
        elif self.rect.right >= WIDHT or self.rect.left <= 0:
            self.vel_x *= -1
        elif self.rect.bottom >= HEIGHT-self.radius or self.rect.top <= 0:
            self.vel_y *= -1
        elif self.rect.bottom > HEIGHT-self.radius or self.rect.top < 0:
            self.rect.bottom = HEIGHT
        
        self.x += self.vel_x
        self.y += self.vel_y
        
    def decay(self):
        if self.vel < 1:
            self.vel = 0
        elif random.randint(1,100*20) == 2:
            self.vel -= 1

    def attract(self):
        m_pos = pygame.mouse.get_pos()
        dist_vec = norm((m_pos[0]-self.x, m_pos[1]-self.y))
        distance = len_vector((m_pos[0]-self.x, m_pos[1]-self.y))
        mice = pygame.mouse.get_pressed()
        rad_vec = (dist_vec[0]*self.vel, dist_vec[1]*self.vel)
        inw = 2
        if distance < self.radius*8 and mice[0] and distance > self.radius+10:
            self.vel_x = (-rad_vec[1]*np.cos(-(inw/180)*np.pi) - rad_vec[0]*np.sin(-(inw/180)*np.pi))*0.5
            self.vel_y = (-rad_vec[1]*np.sin(-(inw/180)*np.pi) + rad_vec[0]*np.cos(-(inw/180)*np.pi))*0.5
        if mice[0]:
            cent = ball(m_pos[0], m_pos[1], 5, '#ff0000', screen, 0, 0)
            cent.draw()
    
    def getBackHere(self):
        tolarance = 100
        out = False
        if WIDHT+tolarance < self.x or self.x < -tolarance:
            self.vel_x = (WIDHT//2-self.x)/10
            out = True
        elif HEIGHT+tolarance < self.y or self.y < -tolarance:
            self.vel_y = (HEIGHT//2-self.y)/10
            out = True
        # if self.x + self.vel_x < -tolarance or self.x + self.vel_x > WIDHT+tolarance or self.y + self.vel_y < -tolarance or self.y + self.vel_y > HEIGHT+tolarance:
        #     self.vel_x *= 0.1
        #     self.vel_y *= 0.1
        return out
            
class Group:
    def __init__(self, objects) -> None:
        self.elements = objects

    def handle(self):
        for index, item in enumerate(self.elements):
            if item.getBackHere() == False:
                    item.draw()
                    item.movement()
                    # item.draw_vector()
                    item.attract()
                # item.decay()
                    for i, z in enumerate(self.elements):
                        if i != index:
                            item.collision(z)
                        else:
                            continue



def main():
    run = True
    blls = []*100
    for _ in range(20):
        blls.append(ball(WIDHT/2*random.uniform(0.5,1.5),HEIGHT/2*random.uniform(0.5,1.5), 10, '#ffffff', screen, random.randint(0,360), 3))        
    marked = ball(WIDHT//2, HEIGHT//2, 10, '#000000', screen, 90, 3)
    blls.append(marked)
    group = Group(blls)
    count = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill('#9FFF93')
        count += 1
        group.handle()

        mouse_pos = writer.render(f"{pygame.mouse.get_pos()}",True, '#000000')
        screen.blit(mouse_pos, (10,10))
        gravity = writer.render(f"Gravity: {GRAV}", True, '#df00ad')
        grav = gravity.get_rect(topright = (WIDHT, 10))
        screen.blit(gravity, grav)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()