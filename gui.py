import pygame, math

class GameGUI():
    def __init__(self,display):
        self.heart_image = pygame.image.load("media/images/heart.png")
        self.weapon_image = pygame.image.load("media/images/weapon.png")
        self.shield_image = pygame.image.load("media/images/shield.png")
        self.width , self.height = display.get_width() , display.get_height()
        self.display = display
        self.font = pygame.font.Font('media/fonts/pixelfont.ttf',32)
    def draw(self,lifes,name,weaponed,bubbled,win = None):
        white   = (255,255,255)
        grey = (55, 58, 61)
        black   = (  0,  0,  0)
        green = (52, 212, 53)
        pygame.draw.rect(self.display, white, [0,0,207,87])
        pygame.draw.rect(self.display, grey, [0,0,200,80])
        rendered_text = self.font.render(name, True, white)
        self.display.blit(rendered_text, [5, 0])
        for h in range(lifes):
            self.display.blit(self.heart_image, [5 + (self.heart_image.get_width()+5) * h , 40])

        pygame.draw.rect(self.display, white, [0,self.height - 60,110,self.height])
        pygame.draw.rect(self.display, grey, [0,self.height - 52,102,self.height])


        if weaponed != 0:
            pygame.draw.arc(self.display, green, (1, self.height - 45, self.weapon_image.get_width()+8, self.weapon_image.get_height()+8), 1.57 - weaponed * (6.28 / 350), 1.57, 4)
            self.display.blit(self.weapon_image, [5,self.height - 42])
        if bubbled != 0:
            pygame.draw.arc(self.display, green, (51, self.height - 45, self.shield_image.get_width()+8, self.shield_image.get_height()+8), 1.57 - bubbled * (6.28 / 350), 1.57, 4)
            self.display.blit(self.shield_image, [55,self.height - 42])

        if lifes == 0:
            rendered_text = self.font.render("GAME OVER", True, white)
            pygame.draw.rect(self.display, white, [self.width // 2- rendered_text.get_width() // 2 - 34, self.height // 2 - rendered_text.get_height() // 2 - 150,240,73])
            pygame.draw.rect(self.display, grey, [self.width // 2- rendered_text.get_width() // 2 - 30, self.height // 2 - rendered_text.get_height() // 2 - 146,230,65])
            self.display.blit(rendered_text, [self.width // 2- rendered_text.get_width() // 2, self.height // 2 - 4 * rendered_text.get_height()])
            #погриаться с рамками для эксита

        if win != None:
            rendered_text = self.font.render("YOU WIN", True, white)
            pygame.draw.rect(self.display, white, [self.width // 2- rendered_text.get_width() // 2 - 34, self.height // 2 - rendered_text.get_height() // 2 - 150,210,73])
            pygame.draw.rect(self.display, grey, [self.width // 2- rendered_text.get_width() // 2 - 30, self.height // 2 - rendered_text.get_height() // 2 - 146,200,65])
            self.display.blit(rendered_text, [self.width // 2- rendered_text.get_width() // 2, self.height // 2 - 4 * rendered_text.get_height()])
