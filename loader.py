import os, sys, pygame
from pygame.locals import *

#Load an image. :)
def load_image(file,x_trans,y_trans,transparent = True):
    fullname = os.path.join('', file)
    image = pygame.image.load(fullname)
    if transparent == True:
        image = image.convert()
        colorkey = image.get_at((x_trans,y_trans))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image
