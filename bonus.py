import pygame, math
from loader import load_image

class BonusDraw():
    def __init__(self,bonus_type,x,y):
        self.image = pygame.image.load("media/images/" + bonus_type + ".png")
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.x , self.y = x , y

    def update(self,x,y):
        self.x , self.y = x , y
    def draw(self,display,cam_x = None, cam_y = None):
        if cam_x == None and cam_y == None:
            display.blit(self.image,[self.x - self.image_w // 2 ,self.y - self.image_h // 2])
        else:
            display.blit(self.image,[self.x - self.image_w // 2 + cam_x ,self.y - self.image_h // 2 + cam_y])

class Bonus(pygame.sprite.Sprite):
    def __init__(self,bonus_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/images/" + bonus_type + ".png")
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.bonus_type = bonus_type

        self.rect.topleft = x - self.image_w // 2, y - self.image_h // 2

        self.global_x = x
        self.global_y = y 
