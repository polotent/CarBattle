import pygame
from loader import load_image

class Map(pygame.sprite.Sprite):
    def __init__(self, file_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(file_path,70,70)
        #self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.map_width  = self.image.get_width()
        self.map_height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect.topleft = x, y
    def update(self, x_change, y_change):
        self.rect.topleft = self.x - x_change, self.y - y_change
