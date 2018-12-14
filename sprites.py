
# i used some ideas from CodePylet https://www.youtube.com/watch?v=osDofIdja6s&t=1038s
# i also borrowed pretty much all of this from kids can code - thanks!
# on acceleration https://www.khanacademy.org/science/physics/one-dimensional-motion/kinematic-formulas/v/average-velocity-for-constant-acceleration 
# on vectors: https://www.youtube.com/watch?v=ml4NSzCQobk 
# I used a lot of different aspects of code from Mr. Cozort


import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint, randrange, choice
from settings import *

vec = pg.math.Vector2
class Spritesheet:
    # class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height, scalefactor):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // scalefactor, height // scalefactor))
        return image


class Player(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group - thanks pygame!
        self._layer = PLAYER_LAYER
        # add player to game groups when instantiated
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        print("adding vecs " + str(self.vel + self.acc))
    def load_images(self):
        if self.game.boughtpurple == False:
            self.standing_frames = [self.game.spritesheet.get_image(690, 406, 120, 201, 3),
                                    self.game.spritesheet.get_image(614, 1063, 120, 191, 3)
                                    ]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
            self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201, 3),
                                    self.game.spritesheet.get_image(692, 1458, 120, 207, 3)
                                    ]
            self.walk_frames_l = []
            for frame in self.walk_frames_r:
                frame.set_colorkey(BLACK)
                self.walk_frames_l.append(pg.transform.flip(frame, True, False))
            self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181, 3)
            self.jump_frame.set_colorkey(BLACK)
        if self.game.boughtpurple == True:
            self.standing_frames = [self.game.spritesheet.get_image(581, 1265, 121, 191, 3),
                                    self.game.spritesheet.get_image(584, 0, 121, 201, 3)
                                    ]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
            self.walk_frames_r = [self.game.spritesheet.get_image(584, 203, 121, 201, 3),
                                    self.game.spritesheet.get_image(678, 651, 121, 207, 3)
                                    ]
            self.walk_frames_l = []
            for frame in self.walk_frames_r:
                frame.set_colorkey(BLACK)
                self.walk_frames_l.append(pg.transform.flip(frame, True, False))
            self.jump_frame = self.game.spritesheet.get_image(416, 1660, 150, 181, 3)
            self.jump_frame.set_colorkey(BLACK)
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        # If b is pressed and you already bought bubble and it is not on cooldown: then it instantiates a bubble
        if keys[pg.K_b] and self.game.boughtbubble == True and self.game.bubblecooldown == 0:
            Bubble(self.game, self)
            self.game.bubblecooldown = 1000
        # The speed the player goes depends on which sprite the player has bought: The purple one being faster
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if self.game.boughtpurple == False:
                self.acc.x =  -PLAYER_ACC
            if self.game.boughtpurple == True:
                self.acc.x = -0.8
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if self.game.boughtpurple == False:
                self.acc.x =  PLAYER_ACC
            if self.game.boughtpurple == True:
                self.acc.x = 0.8
        # set player friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # jump to other side of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
    # cuts the jump short when the space bar is released
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def jump(self):
        print("jump is working")
        # check pixel below
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # adjust based on checked pixel
        self.rect.y -= 2
        # only allow jumping if player is on platform
        if hits and not self.jumping:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell the program that player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            print(self.acc.y)
    def animate(self):
        # gets time in miliseconds
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # checks state
        if not self.jumping and not self.walking:
            # gets current delta time and checks against 200 miliseconds
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                # reset bottom for each frame of animation
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Cloud(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = CLOUD_LAYER
        # add clouds to game groups when instantiated
        self.groups = game.all_sprites, game.clouds
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange (50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), 
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        self.speed = randrange(1,3)
    def update(self):
        if self.rect.top > HEIGHT * 2: 
            self.kill
            ''' mr cozort added animated clouds and made it so they 
            restart on the other side of the screen'''
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width

class Platform(Sprite):
    def __init__(self, game, x, y):
        # allows layering in LayeredUpdates sprite group
        self._layer = PLATFORM_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        if game.score < 500:
            images = [self.game.spritesheet.get_image(0, 288, 380, 94, 2), self.game.spritesheet.get_image(213, 1662, 201, 100, 2)]
        elif game.score < 1000:
            images = [self.game.spritesheet.get_image(0, 768, 380, 94, 2), self.game.spritesheet.get_image(213, 1764, 201, 100, 2)]
        elif game.score < 2000:
            images = [self.game.spritesheet.get_image(0, 576, 380, 94, 2), self.game.spritesheet.get_image(218, 1456, 201, 100, 2)]
        if game.score >= 2000:
            images = [self.game.spritesheet.get_image(0, 96, 380, 94, 2), self.game.spritesheet.get_image(382, 408, 200, 100, 2)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Spawns coins and enemies on platform
        if random.randrange(100) < COIN_SPAWN_PCT:
            Coin(self.game, self)
        elif random.randrange(100) < MOB2_SPAWN_PCT:
            Mob2(self.game, self)
            print("Mob2 is working")

# I made this
class Coin(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = COIN_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.load_frames()
        self.image = self.turning_frames[0]
        self.current_frame = 0
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
        self.last_update = 0
        self.descendanim = False
    def update(self):
        self.animate()
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()
    def load_frames(self):
        # loads animation frames
        self.turning_frames = [self.game.spritesheet.get_image(698, 1931, 84, 84, 2),
                                self.game.spritesheet.get_image(829, 0, 66, 84, 2),
                                self.game.spritesheet.get_image(897, 1574, 50, 84, 2),
                                self.game.spritesheet.get_image(645, 651, 15, 84, 2)]
        for frame in self.turning_frames:
            frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        # creates a back and forth type of animation that makes it look like its spinning
        if self.current_frame == 3:
            self.descendanim = True
        if self.current_frame == 0:
            self.descendanim = False
        if now - self.last_update > 150:
            self.last_update = now
            # added values for the rect.centerx accomodate for off center sprite formatting
            # elif format allows for a single if statement to pass at one time, which makes it display one frame at a time and animate correctly
            if self.current_frame == 0 and self.descendanim == False:
                self.current_frame = 1
                self.image = self.turning_frames[self.current_frame]
                self.rect.centerx = self.plat.rect.centerx + 4.5
            elif self.current_frame == 1  and self.descendanim == False:
                self.current_frame = 2
                self.image = self.turning_frames[self.current_frame]
                self.rect.centerx = self.plat.rect.centerx + 8.5
            elif self.current_frame == 2  and self.descendanim == False:
                self.current_frame = 3
                self.image = self.turning_frames[self.current_frame]
                self.rect.centerx = self.plat.rect.centerx + 17.25
            elif self.current_frame == 3  and self.descendanim == True:
                self.current_frame = 2
                self.image = pg.transform.flip(self.turning_frames[self.current_frame], True, False)
                self.rect.centerx = self.plat.rect.centerx + 8.5
            elif self.current_frame == 2  and self.descendanim == True:
                self.current_frame = 1
                self.image = pg.transform.flip(self.turning_frames[self.current_frame], True, False)
                self.rect.centerx = self.plat.rect.centerx + 4.5
            elif self.current_frame == 1  and self.descendanim == True:
                self.current_frame = 0
                self.image = pg.transform.flip(self.turning_frames[self.current_frame], True, False)
                self.rect.centerx = self.plat.rect.centerx
            
class Mob(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139, 3)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135, 3)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 3 or  self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

# I made this
class Mob2(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        # assigns it to a platform
        self.plat = plat 
        self.load_images()
        self.image = self.walkright[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top
        self.vx = 1
        self.currentframe = 1
        self.last_update = 0
    def update(self):
        # Keeps the Mob2 from going outside the boundaries of the platform
        if self.rect.right == self.plat.rect.right:
            self.vx = -1
        if self.rect.left == self.plat.rect.left:
            self.vx = 1
        self.animate()
        # makes the mob move left and right
        self.rect.x = self.rect.x + self.vx
        # moves the mob with the platform
        self.rect.bottom = self.plat.rect.top
        # kills the mob along with the platform
        if self.rect.bottom + 5 >= HEIGHT:
            self.kill()
    def animate(self):
        now = pg.time.get_ticks()
        # creates walking animation based on direction of walking
        if now - self.last_update > 150:
            self.last_update = now
            if self.vx == 1:
                if self.currentframe == 1:
                    self.currentframe = 0
                    self.image = self.walkright[self.currentframe]
                elif self.currentframe == 0:
                    self.currentframe = 1
                    self.image = self.walkright[self.currentframe]
            elif self.vx == -1:
                if self.currentframe == 1:
                    self.currentframe = 0
                    self.image = self.walkleft[self.currentframe]
                elif self.currentframe == 0:
                    self.currentframe = 1
                    self.image = self.walkleft[self.currentframe]
    def load_images(self):
        # loads animation frames
        self.walkright = [self.game.spritesheet.get_image(704, 1256, 120, 159, 3),
                                self.game.spritesheet.get_image(812, 296, 90, 155, 3)
                                ]
        for frame in self.walkright:
            frame.set_colorkey(BLACK)
        self.walkleft = [pg.transform.flip(self.walkright[0], True, False),
                                pg.transform.flip(self.walkright[1], True, False)
                                ]
        for frame in self.walkleft:
            frame.set_colorkey(BLACK)

# I made this
class Bubble(Sprite):
    def __init__(self, game, play1):
        # allows layering in LayeredUpdates sprite group
        self._layer = BUBBLE_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.game = game
        self.groups = game.all_sprites, game.bubbles
        Sprite.__init__(self, self.groups)
        self.player = play1
        self.image = self.game.spritesheet.get_image(0, 1662, 211, 215, 2).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.player.rect.center
        # adds transparency
        alpha = 70
        pixels = pg.PixelArray(self.image)
        pixels.replace((0, 0, 0, 255), (0, 0, 0, 0))
        self.image.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
    def update(self):
        # keeps the bubble centered on the player
        self.rect.center = self.player.rect.center

# I made this
class Coinmob(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.coinmobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(382, 510, 182, 123, 3)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(382, 635, 174, 126, 3)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 3 or  self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()