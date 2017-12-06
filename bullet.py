import pygame, math
from loader import load_image
class BulletDraw():
    def __init__(self,x,y):
        self.image = pygame.image.load("media/images/bullet.png")
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.image_orig = self.image

        self.x , self.y = x , y
    def draw(self,display,cam_x = None,cam_y = None):
        if cam_x == None and cam_y == None:
            display.blit(self.image,[self.x -self.image_w //2 ,self.y - self.image_h // 2])
        else:
            display.blit(self.image,[self.x -self.image_w //2 + cam_x ,self.y - self.image_h // 2 + cam_y])

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/images/bullet.png")
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.global_x = x
        self.global_y = y
        self.rect.topleft = self.global_x, self.global_y
        self.dir = direction
        self.speed = 17.0

        self.owner = owner

    def update_global(self):
        self.global_x = self.global_x + self.speed * math.cos(math.radians(270-self.dir))
        self.global_y = self.global_y + self.speed * math.sin(math.radians(270-self.dir))
    def update(self):
        self.rect.topleft = self.global_x - self.image_w // 2, self.global_y - self.image_h // 2
        self.mask = pygame.mask.from_surface(self.image)
    def check_wall_collide(self,spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False, pygame.sprite.collide_mask):
            return True
        else :
            return False
