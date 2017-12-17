import pygame, math
from loader import load_image

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

class CarDraw():
    def __init__(self,car_type,name,health,x,y,direction,weapon_upgraded,bubbled,status):
        #self.image = load_image("media/images/" + car_type + ".png",1,1)
        self.image = pygame.image.load("media/images/" + car_type + ".png")
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.image_orig = self.image

        self.bubble_image = pygame.image.load("media/images/bubble.png")
        self.bubble_image_w = self.bubble_image.get_width()
        self.bubble_image_h = self.bubble_image.get_height()
        self.bubble_rect = self.bubble_image.get_rect()
        self.bubble_image_orig = self.bubble_image

        self.name = name
        self.health = health

        self.x , self.y = x , y
        self.dir = direction
        self.status = status

        self.weapon_upgraded = weapon_upgraded
        self.bubbled = bubbled

        self.font = pygame.font.Font('media/fonts/pixelfont.ttf',18)
        self.white_clr = (255,255,255)
        self.little_heart = pygame.image.load("media/images/little_heart.png")
    def update(self,health,x,y,direction,weapon_upgraded,bubbled,status):
        self.status = status
        self.health = health
        self.x , self.y = x , y
        self.dir = direction

        self.weapon_upgraded = weapon_upgraded
        self.bubbled = bubbled

        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()

        self.bubble_image, self.bubble_rect = rot_center(self.bubble_image_orig, self.bubble_rect, self.dir)
        self.bubble_image_w = self.bubble_image.get_width()
        self.bubble_image_h = self.bubble_image.get_height()

    def draw(self,display,bubble_bool,cam_x = None,cam_y = None):
        rendered_name = self.font.render(self.name,True,self.white_clr)
        if cam_x == None and cam_y == None:

            display.blit(self.image,[self.x - self.image_w // 2 ,self.y - self.image_h // 2])
            if bubble_bool == True:
                display.blit(self.bubble_image,[self.x - self.bubble_image_w // 2 ,self.y - self.bubble_image_h // 2])
            display.blit(rendered_name,[self.x - rendered_name.get_width() // 2 ,self.y - rendered_name.get_height() - 40])
            for hrt in range(self.health):
                display.blit(self.little_heart,[self.x - 40 + hrt * 18 , self.y - 40])
        else:

            display.blit(self.image,[self.x - self.image_w // 2 + cam_x ,self.y - self.image_h // 2 + cam_y])
            if bubble_bool:
                display.blit(self.bubble_image,[self.x - self.bubble_image_w // 2 + cam_x ,self.y - self.bubble_image_h // 2 + cam_y])
            display.blit(rendered_name,[self.x - rendered_name.get_width() // 2 + cam_x ,self.y - rendered_name.get_height() - 40 + cam_y])
            for hrt in range(self.health):
                display.blit(self.little_heart,[self.x - 40 + hrt * 18 + cam_x, self.y - 40 + cam_y])

class Car(pygame.sprite.Sprite):
    def __init__(self,car_type,health,x,y,direction,bullet_timeout):
        pygame.sprite.Sprite.__init__(self)
        #self.image = load_image("media/images/" + car_type + ".png",1,1)
        self.image = pygame.image.load("media/images/" + car_type + ".png")
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.mask = pygame.mask.from_surface(self.image)

        self.health = health
        self.maxhealth = self.health
        self.global_x = x
        self.global_y = y
        self.rect.topleft = self.global_x, self.global_y

        self.prev_global_x = self.global_x
        self.prev_global_y = self.global_y

        self.dir = direction
        self.prev_dir = direction

        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

        self.rotating = False
        self.speed = 0.0
        self.maxspeed = 8.5
        self.minspeed = -5.85
        self.acceleration = 0.3
        self.deacceleration = 0.4
        self.softening = 0.14
        self.steering = 7.60

        self.coll_go_forward = False
        self.coll_go_backward = False

        self.real_bullet_timeout = bullet_timeout
        self.bullet_timeout = bullet_timeout
        self.current_timeout = bullet_timeout

        self.weapon_timeout = 0
        self.weapon_upgraded = False

        self.bubble_timeout = 0
        self.bubbled = False

    def soften(self):
        if self.speed > 0:
            self.speed -= self.softening
            if abs(self.speed) < self.softening:
                self.speed = 0
        if self.speed < 0:
            self.speed += self.softening

#Accelerate the vehicle
    def accelerate(self):
        if self.speed < self.maxspeed:
            self.speed = self.speed + self.acceleration

#Deaccelerate.
    def deaccelerate(self):
        if self.speed > self.minspeed:
            self.speed = self.speed - self.deacceleration

#Steer.
    def steerleft(self):
        self.rotating = True
        self.dir = self.dir+self.steering
        if self.dir > 360:
            self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
#Steer.
    def steerright(self):
        self.rotating = True
        self.dir = self.dir-self.steering
        if self.dir < 0:
            self.dir = 360
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)

    def update_global(self):
        self.prev_dir = self.dir
        self.prev_global_x = self.global_x
        self.prev_global_y = self.global_y
        self.global_x = self.global_x + self.speed * math.cos(math.radians(270-self.dir))
        self.global_y = self.global_y + self.speed * math.sin(math.radians(270-self.dir))

    def update(self):
        if self.current_timeout == 0:
            self.current_timeout = self.bullet_timeout
        if self.current_timeout != self.bullet_timeout:
            self.current_timeout = self.current_timeout - 1
        if self.weapon_timeout != 0:
            self.weapon_timeout -= 1
        else:
            self.bullet_timeout = self.real_bullet_timeout
            self.weapon_upgraded = False
        if self.bubble_timeout != 0 :
            self.bubble_timeout -= 1
        else:
            self.bubbled = False
        self.prev_x, self.prev_y = self.rect.topleft
        self.rect.topleft = self.global_x - self.image_w // 2, self.global_y - self.image_h // 2
        self.mask = pygame.mask.from_surface(self.image)

    def backup_position(self):
        self.rotating = False
        self.dir = self.prev_dir
        self.prev_dir = self.dir
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.global_x = self.prev_global_x
        self.global_y = self.prev_global_y
        self.prev_global_x = self.global_x
        self.prev_global_y = self.global_y
        self.rect.topleft = self.prev_x, self.prev_y
        self.mask = pygame.mask.from_surface(self.image)
        if self.speed > 0 and (not self.coll_go_forward):
            self.speed = self.minspeed // 2
            self.coll_go_backward = True
        if self.speed < 0 and (not self.coll_go_backward):
            self.speed = -self.minspeed // 2
            self.coll_go_forward = True
    def check_wall_collide(self,spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False, pygame.sprite.collide_mask):
            self.backup_position()
            return(True)
        else :
            self.coll_go_forward = False
            self.coll_go_backward = False
    def check_bullet_collide(self,spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False, pygame.sprite.collide_mask):
            return True
        else :
            return False
    def check_bonus_collide(self,spriteGroup,bonus_type):
        if pygame.sprite.spritecollide(self, spriteGroup, False, pygame.sprite.collide_mask):
            return True
        else :
            return False
    def hit(self):
        if self.bubbled == False:
            if self.health == 0:
                self.health = 0
            else:
                self.health -= 1
    def heal(self):
        self.health += 1
    def weapon_upgrade(self):
        self.current_timeout = 5
        self.bullet_timeout = 5
        self.weapon_timeout = 350
        self.weapon_upgraded = True
    def defend(self):
        self.bubble_timeout = 350
        self.bubbled = True
