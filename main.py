import pygame as pg
from sys import exit
from player import Player

# --- Inicialização ---
pg.init()
pg.display.set_caption("Bomb Tag")
display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
clock = pg.time.Clock()

# --- Controles de cada jogador ---
controls_p1 = {'left': pg.K_a,    'right': pg.K_d,
               'up':   pg.K_w,    'down':  pg.K_s}
controls_p2 = {'left': pg.K_LEFT,'right': pg.K_RIGHT,
               'up':   pg.K_UP,   'down':  pg.K_DOWN,}

# --- Criação dos sprites ---
players = pg.sprite.Group(
    Player('sprites/green.png', (200, 200), controls_p1, speed=5, size=(48,48)),
    Player('sprites/blue.png',  (400, 200), controls_p2, speed=5, size=(48,48))
)

screen_id = 0

def game_screen():
    display.fill((128, 128, 128))
    players.update(pg.key.get_pressed(), display.get_rect())
    players.draw(display)

def end_screen():
    display.fill((0, 255, 0))

def check_quit():
    for e in pg.event.get():
        if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
            pg.quit()
            exit()

while True:
    check_quit()
    
    if screen_id == 0:
        game_screen()
    else:
        end_screen()
        
    pg.display.flip()
    clock.tick(60)
