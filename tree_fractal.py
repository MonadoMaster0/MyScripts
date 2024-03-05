import numpy as np
import pylab as plt
from pygame.math import Vector2 as vector
import cv2, random

WIDTH, HEIGHT = SIZE = 4000, 3000
blank = np.ones((HEIGHT,WIDTH,3), np.uint8)
white = blank.copy()*255

def tup(self: vector):
    return (int(self.x),int(self.y))

start = vector(WIDTH//2,HEIGHT)
base = vector(0, 500)

cv2.line(blank, tup(start), tup(start-base), (255,255,255), 30)

def tree(start: vector, vec: vector, angle, z, level, randangle=True, direction=0):
    ss = vec.length()
    if level > 1:
        f = 1-(random.random()*random.random())**(1/2) if randangle==True else 1
        g = 1-(random.random()*random.random())**(1/2) if randangle==True else 1
        c = [random.random(),random.random()]
        c1, c2, c3 = c[0]**10, (c[1]+1)/level, (c[0]+1)/level*0.5
        x = random.randint(0,1) if direction==0 else 1
        rota = vec.rotate(angle*f)*z
        rotb = vec.rotate(-angle*g)*z
        cv2.line(blank, tup(start), tup(start-rota), (180,255-(255*c2*1.3),255-(255*c3)*0.8), level)
        cv2.line(blank, tup(start), tup(start-rotb), (180,255-(255*c2*1.3),255-(255*c3)*0.8), level)
        if x:
            tree(start-rota, rota, angle*level/(level-1), z, level-1, randangle)
            tree(start-rotb, rotb, angle*level/(level-1),  z, level-1, randangle)
        else:
            tree(start-rotb, rotb, angle*level/(level-1),  z, level-1, randangle)     
            tree(start-rota, rota, angle*level/(level-1), z, level-1, randangle)

tree(start-base, base/2.3, 15, 0.93, 20, randangle=True, direction=1)
# blank = cv2.GaussianBlur(blank, (21,21), 10)
trunk = cv2.subtract(white,blank)
trunk = cv2.GaussianBlur(trunk, (5,5), 10)

plt.imshow(trunk)
plt.show()