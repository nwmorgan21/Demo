#this file was created by Nate Morgan
# Sources: goo.gl/2KMivS, Mr. Cozort, Kids Can Code    

'''
Curious, Creative, Tenacious(requires hopefulness)

Gameplay ideas:
- coin system that is saved using text file
- store system to purchase things, by using accumulated coins
- made a second mob type that stays on assigned platform
- platforms continually scroll downwards

Cosmetics:
- made power up icons show up on screen if they bought and off of cooldown while playing
- made coin icon to be displayed next to coin count to distinguish between coin count and score
- added coin sound
- Background changes color based on how high player score is
- Platforms change skin based on how high the player score is

Bugs:
- when you purchase something from the store and go back to the start screen it freezes and won't let you play
- the bubble cooldown system lets you stack multiple bubbles on top of each other

Gameplay Fixes:
- made player jump higher to keep the player from not being able to reach some platforms
- when jump boost is used the player is invincible to keep from killing the player immediately when they use jump boost

Features:
- you can purchase two power ups that can be used once you have bought them from the store:
    jump boost:
        shoots player up when space pressed, has cooldown of 1000
    bubble boost:
        protects player from  mobs for one hit, has cooldown of 1000
    *** Both of these are saved using text files 
- you can also buy a second player sprite that is faster and has a different skin
- winged coin mob that flies around screen and gives player 10 coins when hit
'''
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #init game window
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Rabbit Season")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

        # Assortment of variables used later on
        self.boostcooldown = 0
        self.bubblecooldown = 0
        self.playerinvincibility = False
        self.buyjumpboost = 0
        self.buybubble = 0
        self.buypurple = 0
        self.coinmob_timer = 0
        self.coincount = 0
        self.load_data()
        
    def load_data(self):
        print("load data is called...")
        # sets up directory name
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # opens file with write options
        ''' with is a contextual option that handles both opening and closing of files to avoid
        issues with forgetting to close
        '''

        # Opens highscore file to be able to save the highscore
        try:
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")

        # Opens the coin file to allow for coincount to be saved
        try:
            with open(path.join(self.dir, "Coins.txt"), 'r') as f:
                self.coincount = int(f.read())
                print(self.coincount)
        except:
            with open(path.join(self.dir, COIN_FILE), 'w') as f:
                self.cointcount = 0
                print("exception")

        # creates an in game variable for the amount coins the player has saved
        if self.coincount < 0:
            self.coincount = 0

        # Opens jump boost text file to be able to save things that were bought
        try:
            with open(path.join(self.dir, "Jump Boost.txt"), 'r') as f:
                self.buyjumpboost = int(f.read())
    
        except:
            with open(path.join(self.dir, JUMP_BOOST_FILE), 'w') as f:
                print("exception")
        
        # variable for whether or not the player has bought jump boost
        if self.buyjumpboost == 1:
            self.boughtjumpboost = True
        elif self.buyjumpboost == 0:
            self.boughtjumpboost = False

        # Opens bubble boost text file to be able to save things that were bought
        try:
            with open(path.join(self.dir, "Bubble.txt"), 'r') as f:
                self.buybubble = int(f.read())
                print(self.buybubble)
        except:
            with open(path.join(self.dir, BUBBLE_FILE), 'w') as f:
                print("exception")
        
        # variable for whether or not the player has bought bubble boost
        if self.buybubble == 1:
            self.boughtbubble = True
        elif self.buybubble == 0:
            self.boughtbubble = False

        # Opens Purple Bunny text to be able to save things that were bought from the store
        try:
            with open(path.join(self.dir, "PurpleBunny.txt"), 'r') as f:
                self.buypurple = int(f.read())
                print(self.buypurple)
        except:
            with open(path.join(self.dir, PURPLE_FILE), 'w') as f:
                print("exception")
        
        # variable for whether or not the player has bought the purple bunny
        if self.buypurple == 1:
            self.boughtpurple = True
        elif self.buypurple == 0:
            self.boughtpurple = False

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # load clouds
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())  

        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))
        self.coinsound = pg.mixer.Sound(path.join(self.snd_dir, 'coinhit.wav'))

        # Load Icons
        self.boostimg = self.spritesheet.get_image(820, 1805, 71, 70, 2)
        self.boostimg.set_colorkey(BLACK)
        self.coinicon = self.spritesheet.get_image(244, 1981, 61, 61, 3)
        self.coinicon.set_colorkey(BLACK)
        self.bubbleimg = self.spritesheet.get_image(826, 134, 71, 70, 2)
        self.bubbleimg.set_colorkey(BLACK)
     
    def new(self):
        # sets score
        self.score = 0
        # add all sprites to the pg group
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create platforms group
        self.platforms = pg.sprite.Group()
        # create cloud group
        self.clouds = pg.sprite.Group()
        # add powerups
        self.powerups = pg.sprite.Group()
        # create coin group
        self.coins = pg.sprite.Group()
        # create bubble group
        self.bubbles = pg.sprite.Group()
        # sets mob timer
        self.mob_timer = 0
        # add a player 1 to the group
        self.player = Player(self)
        # add mobs
        self.mobs = pg.sprite.Group()
        # add coinmobs
        self.coinmobs = pg.sprite.Group()

        # Instantiate Platform and clouds
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500

        # load music
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))

        # call the run method
        self.run()

    def run(self):
        # play music
        pg.mixer.music.play(loops=-1)
        # set boolean playing to true
        self.playing = True
        # Main game loop
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
    def update(self):
        # keeps every sprite updating through the game loop
        self.all_sprites.update()

        # Makes sure player doesn't stay invincible after jump boost
        if self.player.vel.y > 0:
            self.playerinvincibility = False      

        # Cooldown of boosts
        if self.boostcooldown > 0:
            self.boostcooldown -= 1
        if self.bubblecooldown > 0:
            self.bubblecooldown -= 1

        # Spawns a flying mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # Spawns coin mob
        now = pg.time.get_ticks()
        if now - self.coinmob_timer > 10000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.coinmob_timer = now
            Coinmob(self)

        # check for mob collisions
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        for m in mob_hits:
            if self.playerinvincibility == False:
                self.playing = False
            elif self.playerinvincibility == True:
                m.kill()

        # check for coinmob collisions
        coinmob_hits = pg.sprite.spritecollide(self.player, self.coinmobs, False)
        for m in coinmob_hits:
            if self.coincount < 989:
                self.coincount += 10
            self.coinsound.play()
            m.kill()

        # check for bubble and mob collisions by checking if sprites in two different groups collide
        pg.sprite.groupcollide(self.bubbles, self.mobs, True, True)
                       
        # check to see if player can jump - if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # set var to be current hit in list to find which to 'pop' to when two or more collide with player
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit
                # fall if center is off platform
                if self.player.pos.x < find_lowest.rect.right + 10 and self.player.pos.x > find_lowest.rect.left - 10:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                # scroll plats with player
        if self.player.rect.top <= HEIGHT / 4:
            if randrange(100) < 13:
                Cloud(self)
            # creates slight scroll at the top based on player y velocity
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.x / randrange(2,10)), 2)
            for mob in self.mobs:
                # creates slight scroll based on player y velocity
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for mob in self.coinmobs:
                # creates slight scroll based on player y velocity
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                # creates slight scroll based on player y velocity
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.centery - 20 >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Create continuous scroll
        for plat in self.platforms:
                plat.rect.y += 1
                if plat.rect.centery - 20 >= HEIGHT:
                    plat.kill()
                    self.score += 10
    
        # Kills player if they go beyond the screen limit
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False
        # generate new random platforms
        while len(self.platforms) < 10:
            width = random.randrange(50, 100)            
            Platform(self, random.randrange(0,WIDTH-width), 
                            random.randrange(-75, -30))

        # Detect if player hits a coin
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, False)
        for i in coin_hits:
            i.kill()
            self.coinsound.play()
            # limits amount of coins possible to 999 and adds 1 to coin count
            if self.coincount < 999:
                self.coincount = self.coincount + 1
        
        # resets cooldown once you die
        if self.playing == False:
            self.bubblecooldown = 0
            self.boostcooldown = 0

    def events(self):
        # detects if buttons are pressed in game
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w or event.key == pg.K_UP:
                        self.player.jump()
                    # Detects if jumpboost is available
                    if event.key == pg.K_SPACE and self.boughtjumpboost == True and self.boostcooldown == 0:
                        self.playerinvincibility = True
                        self.player.vel.y = -BOOST_POWER
                        self.boost_sound.play()
                        self.boostcooldown = 1000
                if event.type == pg.KEYUP:
                    if event.key == pg.K_w or event.key == pg.K_UP:
                        # cuts the jump short if the space bar is released
                        self.player.jump_cut()
    
    def draw(self):
        # Creates a background that changes based on the score of the player
        if self.score < 500:
            self.screen.fill(SKY_BLUE)
        elif self.score < 1000:
            self.screen.fill(DARK_GRAY)
        elif self.score < 2000:
            self.screen.fill(LIGHT_PINK)
        if self.score >= 2000:
            self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # Displays Boost once it is available to use
        if self.boostcooldown == 0 and self.boughtjumpboost == True:
            self.screen.blit(self.boostimg, (0, HEIGHT - 35 ))
        if self.bubblecooldown == 0 and self.boughtbubble == True:
            self.screen.blit(self.bubbleimg, (35, HEIGHT - 35 ))
        self.draw_text(str(self.score), 22, WHITE, 20, 10)
        self.draw_text(str(self.coincount), 22, WHITE, WIDTH - 20, 10)
        self.screen.blit(self.coinicon, (WIDTH - 60, 10 ))

        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()
    def wait_for_key(self): 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False
                    if event.key == pg.K_s:
                        self.store()

    # I made this
    def store(self):
        # Create store screen
        self.screen.fill(BLACK)
        self.draw_text("Store", 48, WHITE, WIDTH/2, 30)
        self.draw_text("Coins: " + str(self.coincount), 22, WHITE, WIDTH / 2, 100)
        self.draw_text("<-", 30, WHITE, 50, 50)
        self.draw_text("Esc", 30, WHITE, 50, 10)
        # Jump Boost display
        if self.boughtjumpboost == 0:
            self.draw_text("1: 200 coins", 22, WHITE, WIDTH/4, HEIGHT/2 + 20)
            self.screen.blit(self.boostimg, (WIDTH/4 - 35, HEIGHT/2 - 60))
        # Bubble boost display
        if self.boughtbubble == 0:
            self.draw_text("2: 100 coins", 22, WHITE, WIDTH * 3/4, HEIGHT/2 + 20)
            self.screen.blit(self.bubbleimg, (WIDTH * 3/4 - 35, HEIGHT/2 - 60))
        # Purple bunny display
        if self.boughtpurple == 0:
            self.draw_text("3: 300 coins", 22, WHITE, WIDTH/4, HEIGHT - 40)
            self.screen.blit(self.spritesheet.get_image(584, 0, 121, 201, 4), (WIDTH/4, HEIGHT - 100))
        

        pg.display.flip()
        self.store_wait()
    def store_wait(self):
        storewait = True
        # keeps waiting for button to be pushed while in store
        while storewait:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    storewait = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        storewait = False
                    # buying the jump boost and writing in the text files
                    if event.key == pg.K_1 and self.coincount >= 200:
                        if self.boughtjumpboost == False:
                            print("jump boost bought")
                            self.coincount -= 200
                            self.boughtjumpboost = True
                            try:
                                with open(path.join(self.dir, COIN_FILE), 'w') as C:
                                    C.write(str(self.coincount - 200))
                                with open(path.join(self.dir, JUMP_BOOST_FILE), 'w') as J:
                                    J.write(str(1))
                            except:
                                print("exception")
                            self.store()
                    # buying the bubble boost and writing in the text files
                    if event.key == pg.K_2 and self.coincount >= 100:
                        if self.boughtbubble == False:
                            print("bubble bought")
                            self.coincount -= 100
                            self.boughtbubble = True
                            with open(path.join(self.dir, COIN_FILE), 'w') as C:
                                C.write(str(self.coincount - 100))
                            with open(path.join(self.dir, BUBBLE_FILE), 'w') as B:
                                B.write(str(1))
                            self.store()
                    # buying the Purple bunny skin and writing in the text files
                    if event.key == pg.K_3 and self.coincount >= 300:
                        if self.boughtpurple == False:
                            print("purple bought")
                            self.coincount -= 300
                            self.boughtpurple = True
                            with open(path.join(self.dir, COIN_FILE), 'w') as C:
                                C.write(str(self.coincount - 300))
                            with open(path.join(self.dir, PURPLE_FILE), 'w') as P:
                                P.write(str(1))
                            self.store()
                            
        self.show_start_screen()

        
    def show_start_screen(self):
        # game splash screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press enter to play...", 22, WHITE, WIDTH / 2, HEIGHT/2 + 30)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        self.draw_text("Press S for the store", 22, WHITE, WIDTH / 2, 65)
        self.draw_text("Coins: " + str(self.coincount), 22, WHITE, WIDTH / 2, 40)
        # Displays the boosts that have been bought
        self.draw_text("Boosts: ", 22, WHITE, 35, HEIGHT * 3/4)
        if self.boughtjumpboost == True:
            self.screen.blit(self.spritesheet.get_image(820, 1805, 71, 70, 1), (10, HEIGHT - 115))
            self.draw_text("Spacebar", 22, WHITE, 45, HEIGHT-30)
        if self.boughtbubble == True:
            self.screen.blit(self.spritesheet.get_image(826, 134, 71, 70, 1), (91, HEIGHT - 115))
            self.draw_text("B button", 22, WHITE, 140, HEIGHT-30)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        # game splash screen
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press S for the store", 22, WHITE, WIDTH / 2, 65)
        self.draw_text("Press Enter to play...", 22, WHITE, WIDTH / 2, HEIGHT/2 + 90)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        self.draw_text("Coins: " + str(self.coincount), 22, WHITE, WIDTH / 2, HEIGHT/2 + 65)
        self.draw_text("Boosts: ", 22, WHITE, 35, HEIGHT * 3/4)
        # Displays the boosts if they were bought
        if self.boughtjumpboost == True:
            self.screen.blit(self.spritesheet.get_image(820, 1805, 71, 70, 1), (10, HEIGHT - 115))
            self.draw_text("Spacebar", 22, WHITE, 45, HEIGHT-30)
        if self.boughtbubble == True:
            self.screen.blit(self.spritesheet.get_image(826, 134, 71, 70, 1), (91, HEIGHT - 115))
            self.draw_text("B button", 22, WHITE, 140, HEIGHT-30)
        with open(path.join(self.dir, COIN_FILE), 'w') as f:
                f.write(str(self.coincount))
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 140)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)


        pg.display.flip()
        self.wait_for_key()
    # Method for drawing text
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()

g.show_start_screen()

while g.running:
    g.new()
    print("game loop is running...")
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")