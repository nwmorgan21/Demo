import pygame as pg 
from pygame.sprite import Sprite
import random
from setting import *

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def update(self):
        self.acc = vec(0,player_grav)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc

        #Player Friction
        self.acc.x += self.vel.x * player_friction

        #Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -20



class Platform(Sprite):
    def __inti__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
   

#