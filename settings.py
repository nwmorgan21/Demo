TITLE = "Rabbit Season"
# screen dims
WIDTH = 480
HEIGHT = 600
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
SKY_BLUE = (143, 185, 252)
LIGHT_PINK = (255,182,193)
DARK_GRAY = (169,169,169)
FONT_NAME = 'arial'
# Data Files
SPRITESHEET = "spritesheet_jumper.png"
HS_FILE = "highscore.txt"
COIN_FILE = "Coins.txt"
JUMP_BOOST_FILE = "Jump Boost.txt"
BUBBLE_FILE = "Bubble.txt"
PURPLE_FILE = "PurpleBunny.txt"
# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22.5
# game settings
BOOST_POWER = 60
COIN_SPAWN_PCT = 21
MOB2_SPAWN_PCT = 16
COINMOB_SPAWN_PCT = 0
MOB_FREQ = 5000
PLAYER_LAYER = 2
CLOUD_LAYER = 0
PLATFORM_LAYER = 1
POW_LAYER = 1
COIN_LAYER = 1
MOB_LAYER = 2
ICON_LAYER = 2
BUBBLE_LAYER = 2

# platform settings
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (65, HEIGHT - 300),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 150),
                 (200, HEIGHT - 450)]
