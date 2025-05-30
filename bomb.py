import pygame as pg
from player import Player
import constants as const

pg.mixer.init()

slap = pg.mixer.Sound("sfx\slap.mp3")
slap.set_volume(0.2)

beep = pg.mixer.Sound(r"sfx\beep.ogg")
beep.set_volume(0.1)
charge = pg.mixer.Sound(r"sfx\bomb_charge.ogg")
charge.set_volume(0.15)
detonate = pg.mixer.Sound(r"sfx\bomb_detonate.ogg")
detonate.set_volume(.5)

BEEPEVENT = pg.USEREVENT + 1

class Bomb(pg.sprite.Sprite):
    def __init__(self, owner, explode_event, size=(46, 23)):
        super().__init__()
        self.owner = owner
        self.expode_event = explode_event
        self.cooldown = const.SWAP_COOLDOWN
        self.explosion_time = const.EXPLOSION_TIME
        self.cooldown_timer = 0
        self.timer = 0
        self.should_hide = True
        
        self.image = pg.transform.scale(pg.image.load("sprites/bomb_strap.png"), size)
        self.rect = self.image.get_rect(center=owner.rect.center)
        
        self.light = pg.image.load("sprites/bomb_light.png")
        self.light_rect = self.light.get_rect(center=owner.rect.center)
        
        self.owner.update_expression("mad")
        self.owner.speed = const.BOMB_SPEED
        
        pg.time.set_timer(BEEPEVENT, 1000, 1)

    def update(self, players, delta_time):        
        self.timer += delta_time
        self.cooldown_timer += delta_time
        self.rect.center = self.owner.rect.center
        self.rect.y += 20
        self.light_rect.center = self.rect.center
        self.light_rect.y += 5
        
        if (self.timer >= self.explosion_time):
            detonate.play()
            self.expode_event(self.owner)
        
        if self.cooldown_timer < self.cooldown:
            return
        
        for player in players:
            if player is self.owner:
                continue
            
            if pg.sprite.collide_rect(self.owner, player):
                self.owner.update_expression("happy")
                self.owner.speed = const.PLAYER_SPEED # Speed goes back to normal
                
                self.owner = player
                self.owner.update_expression("mad")
                self.owner.speed = const.BOMB_SPEED # Speed up
                        
                self.cooldown_timer = 0
                
                slap.play()
                break
    
    def beep(self):
        beep.play()
        
        time_remaining = self.explosion_time - self.timer
        
        if (time_remaining <= 1):
            charge.play()
        elif (time_remaining <= 3):
            pg.time.set_timer(BEEPEVENT, 75, 1)
        elif (time_remaining <= 5):
            pg.time.set_timer(BEEPEVENT, 125, 1)
        elif (time_remaining <= 7):
            pg.time.set_timer(BEEPEVENT, 250, 1)
        elif (time_remaining <= 10):
            pg.time.set_timer(BEEPEVENT, 500, 1)
        else:
            pg.time.set_timer(BEEPEVENT, 1000, 1)
            
        if (time_remaining < 20 and time_remaining > 1):
            self.should_hide = not self.should_hide
        else:
            self.should_hide = False
    
    # Used to render both bomb and light
    def render(self, display):
        display.blit(self.image, self.rect)
        if (not self.should_hide): display.blit(self.light, self.light_rect)
        
        
