import pygame as pg
from sys import exit
from player import Player
from bomb import Bomb
from blockingPlatform import Platform
import random as rnd

pg.init()
pg.display.set_caption("Bomb Tag – by Vinicius, Hugo e Felipe")

display     = pg.display.set_mode((0, 0), pg.FULLSCREEN)
screen_rect = display.get_rect()

clock       = pg.time.Clock()

headerfont = pg.font.SysFont(None, 80)
font = pg.font.SysFont(None, 56)
subfont = pg.font.SysFont(None, 30)

screen_id = 0 # 0 - Game screen; 1 - round over screen; 3 - game over screen; 4 - main menu screen

scores = [0, 0]
last_winner = -1

def make_platforms():
    w, h = screen_rect.size
    platforms = []

    #~ Floor
    platforms.append(Platform(pg.Rect(0, h - 40, w, 40)))
    #platforms.append(Platform(pg.Rect((w/2) - 5, (h/2) - 5, 10, h))) # - Middle marker

    rows = 3
    columns = 4
    
    row_distance = 220 #h/rows
    column_distance = w/(columns-1)

    for row in range(rows):
        row_factor = 1.0 - row * 0.1

        for column in range(columns):
            spawn_chance = 80 * row_factor
            
            if (rnd.randrange(1, 100) < spawn_chance): #
                height = 25
                width = rnd.randrange(350, 450)
                
                if (column == 0 or column == columns-1):
                    width = 500
                    
                width *= row_factor
                
                x = (column_distance * column) - (width/2)
                y = h - (row_distance * (row + 1))
                
                platforms.append(Platform(pg.Rect(x, y, width, height)))

    return pg.sprite.Group(platforms)

platforms = make_platforms()

#~ Players

def spawn_players():
    return pg.sprite.Group(
    Player('sprites/green.png', (350, screen_rect.height - 50), controls_p1),
    Player('sprites/blue.png',  (screen_rect.width - 350, screen_rect.height - 50), controls_p2)
)

def explode(player):
    global screen_id, last_winner
    
    if (player is players.sprites()[0]):
        last_winner = 2
        scores[1] += 1
    elif (player is players.sprites()[1]):
        last_winner = 1
        scores[0] += 1
    
    # Round over screen
    screen_id = 1

controls_p1 = {'left': pg.K_a,    'right': pg.K_d,
               'up':   pg.K_w,    'down':  pg.K_s}
controls_p2 = {'left': pg.K_LEFT,'right': pg.K_RIGHT,
               'up':   pg.K_UP,   'down':  pg.K_DOWN}

players = spawn_players()

bomb = Bomb(rnd.choice(players.sprites()), explode)

#~ -------- Main loop ---------------------------------------------------------
def game_screen(dt):
    display.fill((40, 40, 40))
    players.update(pg.key.get_pressed(), platforms, screen_rect)
    bomb.update(players, dt)
    
    timer_surface = headerfont.render(f"{int(bomb.explosion_time - bomb.timer) + 1}", False, (255, 255, 255))
    timer_rect = timer_surface.get_rect(center = screen_rect.center)
    timer_rect.top = 50
    
    score_surface = font.render(f"{scores[0]} - {scores[1]}", False, (255, 255, 255))
    score_rect = score_surface.get_rect(center = screen_rect.center)
    score_rect.top = 120

    platforms.draw(display)
    players.draw(display)
    display.blit(bomb.image, bomb.rect)
    display.blit(timer_surface, timer_rect)
    display.blit(score_surface, score_rect)
    
def round_over_screen():
    w, h = screen_rect.size
    display.fill((40, 40, 40))
    
    winner_surface = font.render(f'Player {last_winner} won the round!', True, (255, 255, 255))
    winner_rect = winner_surface.get_rect(center = screen_rect.center)
    
    restart_surface = subfont.render('Press R to proceed to next round', True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center = screen_rect.center)
    restart_rect.y += 50
    
    score_surface = font.render(f"{scores[0]} - {scores[1]}", False, (255, 255, 255))
    score_rect = score_surface.get_rect(center = screen_rect.center)
    score_rect.top = 120
    
    display.blit(winner_surface, winner_rect)
    display.blit(restart_surface, restart_rect)
    display.blit(score_surface, score_rect)
    
def handle_events():
    for e in pg.event.get():
        if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
            pg.quit()
            exit()
        if (e.type == pg.KEYDOWN and e.key == pg.K_r and screen_id):
            if (screen_id == 1):
                next_round()

def next_round():
    global platforms, players, bomb, screen_id, last_winner

    #~ regenerate level geometry
    platforms = make_platforms()

    #~ respawn players
    players = spawn_players()

    #~ give bomb to a random player
    bomb = Bomb(rnd.choice(players.sprites()), explode)

    last_winner = "none"
    screen_id = 0

while True:
    handle_events()
    delta_time = clock.tick(60) / 1000
    
    if (screen_id == 0):
        game_screen(delta_time)
    elif (screen_id == 1):
        round_over_screen()
    
    pg.display.flip()
