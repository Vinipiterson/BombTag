import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#~ Bomb
EXPLOSION_TIME = 20
SWAP_COOLDOWN = 0.4 # seconds

#~ Player K de keyboard
CONTROLS_P1 = {'left': pg.K_a,    'right': pg.K_d,
               'up':   pg.K_w,    'down':  pg.K_s}
CONTROLS_P2 = {'left': pg.K_LEFT,'right': pg.K_RIGHT,
               'up':   pg.K_UP,   'down':  pg.K_DOWN}

PLAYER_SPEED = 10
BOMB_SPEED = 12
JUMP_STRENGHT = -27 # negative velocity makes the character go up
GRAVITY = 1.25