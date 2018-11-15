# this file was created by nate morgan
# thanks Chris Bradfield from Kids Can Code.
# I've not got this on github...

import pygame as pg
import random
from setting import *
from sprites import *

class Game:
    def __init__(self):
        # init game window, try:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
        # init pygame and create...
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()

        p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
        p2 = Platform(65, HEIGHT - 150, WIDTH - 300, 40)

        self.player1 = Player(self)
        #self.player2 = Player(WHITE)

        self.all_sprites.add(self.player1)
        #self.all_sprites.add(self.player2)

        self.all_sprites.add(p1)
        self.all_platforms.add(p1)
        self.all_sprites.add(p2)
        self.all_platforms.add(p2)

        self.run()
        # create new player object
    def run(self): 
        self.playing = True
        # game loop
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player1, self.all_platforms, False)
        print(hits)

        if hits:
            self.player1.pos.y = hits[0].rect.top + 1
            self.player1.vel.y = 0
        #self.player2.update(pg.K_a,pg.K_d,pg.K_w)
        # update things
    def events(self):
        
        # listening for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player1.jump()


    def draw(self):
        self.screen.fill(REDDISH)
        self.all_sprites.draw(self.screen)
        # double buffer
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
