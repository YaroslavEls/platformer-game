import os

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'Platformer Game'

TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

SPRITE_SCALING_LASER = 0.8
SHOOT_SPEED = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 25

PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

PLAYER_START_X = 2
PLAYER_START_Y = 1

RIGHT_FACING = 0
LEFT_FACING = 1

CWD = os.getcwd()
ASSETS_PATH = os.path.join(CWD, 'assets')

LEVELS_COUNT = 3
MAP_NAME = lambda x: f'{ASSETS_PATH}/maps/level_{x}.json'

LAYER_NAME_BACKGROUND = 'Background'
LAYER_NAME_PLATFORMS = 'Platforms'
LAYER_NAME_LADDERS = 'Ladders'
LAYER_NAME_MOVING_PLATFORMS = 'Moving Platforms'
LAYER_NAME_FINISH = 'Finish'
LAYER_NAME_LOCKS = 'Locks'
LAYER_NAME_KEYS = 'Keys'
LAYER_NAME_COINS = 'Coins'
LAYER_NAME_ENEMIES = 'Enemies'
LAYER_NAME_DEATH = 'Death'
LAYER_NAME_PLAYER = 'Player'
LAYER_NAME_BULLETS = 'Bullets'

CHARACTER1_NAME = 'female_adventurer'
CHARACTER2_NAME = 'male_adventurer'

JUMP_SOUND_PATH = f'{ASSETS_PATH}/sounds/jump.wav'
COIN_SOUND_PATH = f'{ASSETS_PATH}/sounds/coin.wav'
KEY_SOUND_PATH = f'{ASSETS_PATH}/sounds/key.wav'
DEATH_SOUND_PATH = f'{ASSETS_PATH}/sounds/gameover.wav'
SHOOT_SOUND_PATH = f'{ASSETS_PATH}/sounds/hurt.wav'
HIT_SOUND_PATH = f'{ASSETS_PATH}/sounds/hit.wav'

LASER_IMAGE_PATH = f'{ASSETS_PATH}/images/effects/laser.png'
