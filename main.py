import pygame as pg
from sys import exit
import random as rnd

# Custom modules
import player
from bomb import Bomb, BEEPEVENT
import levels
import constants as const

pg.init()
pg.mixer.init()
pg.display.set_caption("Bomb Tag – por Vinicius, Hugo e Felipe")

# screen
display = pg.display.set_mode((0, 0), pg.WINDOWMAXIMIZED)
screen_rect = display.get_rect()

# clock
clock = pg.time.Clock()

# fonts
headerfont = pg.font.Font("font/Super Squad.ttf", 40) #SysFont(None, 80)
font = pg.font.Font("font/Super Squad.ttf", 25)
subfont = pg.font.Font("font/Super Squad.ttf", 15)

# sfx
soundtrack = pg.mixer.music.load("sfx\soundtrack.mp3")
pg.mixer.music.set_volume(0.02)

# background
bg = pg.image.load("sprites/bg.png").convert()

# game state
screen_id = 0 # 0 - Game screen; 1 - round over screen; 3 - game over screen; 4 - main menu screen

# round
scores = [0, 0]
last_winner = -1

#~ Game
def game_screen(dt):
    display.blit(bg, (0, 0))
    players.update(pg.key.get_pressed(), platforms, screen_rect)
    bomb.update(players, dt)
    
    timer_surface = headerfont.render(f"{int(bomb.explosion_time - bomb.timer) + 1}", True, const.WHITE)
    timer_rect = timer_surface.get_rect(center = screen_rect.center)
    timer_rect.top = 20
    
    score_surface = font.render(f"{scores[0]} - {scores[1]}", True, const.WHITE)
    score_rect = score_surface.get_rect(center = screen_rect.center)
    score_rect.top = 80

    platforms.draw(display)
    players.draw(display)
    bomb.render(display)
    display.blit(timer_surface, timer_rect)
    display.blit(score_surface, score_rect)
    
def round_over_screen():
    w, h = screen_rect.size
    display.blit(bg, (0, 0))
    
    player_text = ("Green" if last_winner == 1 else "Yellow")
    winner_surface = font.render(f'{player_text} won the round!', True, const.WHITE)
    winner_rect = winner_surface.get_rect(center = screen_rect.center)
    
    restart_surface = subfont.render('Press "R" to proceed to next round or "N" to start from scratch', True, const.WHITE)
    restart_rect = restart_surface.get_rect(center = screen_rect.center)
    restart_rect.y += 50
    
    score_surface = font.render(f"{scores[0]} - {scores[1]}", True, const.WHITE)
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
        if (e.type == pg.KEYDOWN and e.key == pg.K_r):
            if (screen_id == 1):
                next_round()
        if (e.type == pg.KEYDOWN and e.key == pg.K_n):
            if (screen_id == 1):
                scores[0] = 0
                scores[1] = 0
                next_round()
        if (e.type == BEEPEVENT):
            bomb.beep()

def next_round():
    global platforms, players, bomb, screen_id, last_winner

    #~ regenerate level geometry
    platforms = levels.get_random_map(screen_rect)

    #~ respawn players
    players = player.spawn_players(screen_rect)

    #~ give bomb to the last winner
    bomb = Bomb(players.sprites()[last_winner-1], explode)

    last_winner = -1
    screen_id = 0
    
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
#~ Game

platforms = levels.get_random_map(screen_rect)
players = player.spawn_players(screen_rect)
bomb = Bomb(rnd.choice(players.sprites()), explode)

pg.mixer.music.play(-1)
while True:
    handle_events()
    delta_time = clock.tick(60) / 1000
    
    if (screen_id == 0):
        game_screen(delta_time)
    elif (screen_id == 1):
        round_over_screen()
    
    pg.display.flip()