import cv2
import numpy as np
from pylab import imshow, show, subplot, close

res = int(input("Enter resolution: "))

blank = np.ones((res,res), np.uint8)

def fractal(image: np.ndarray, order: int):
    
    # Initialized variables
    thirds = []
    fulls = []
    third = image.shape[0]
    fract = np.zeros(image.shape, np.uint8)
    
    # Make small boxes
    for _ in range(order):
        full = np.ones((third,third), np.uint8) # empty box
        third = third//3
        box = np.zeros((third,third), np.uint8) # box filler
        full[third:2*third, third:2*third] = box # full box
        thirds.append(full)
        
    # Making full size images from boxes
    try:
        for item in thirds:
            row = np.concatenate([item for _ in range(image.shape[0]//item.shape[0])], axis=1) # add images vertically
            im = np.concatenate([row for _ in range(image.shape[0]//item.shape[0])], axis=0) # add images horizontally
            fulls.append(im if im.shape == image.shape else cv2.resize(im, image.shape, interpolation=cv2.INTER_NEAREST))
    except ZeroDivisionError:
        print(f'Rendűségi hiba! A fraktál rendűsége nem lehet nagyobb, mint {np.log(image.shape[0])//np.log(3)} (képméret alapján)')
    
    # Merging images
    for img in fulls:
        fract = cv2.add(fract, img)
        # fract = cv2.cvtColor(fract, cv2.COLOR_BGR2GRAY)
        
    return cv2.threshold(fract, 1, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1], fulls
        

# fract = np.ones((1,1), np.uint8)
fract, fulls = fractal(blank, 10)
# fract = np.concatenate([fract, fract], axis=1)

imshow(fract, 'gray')
show()
