import pygame as pg

class Bomb(pg.sprite.Sprite):
    def __init__(self, owner, explode, cooldown=0.4, explosion_time = 5, size=20):
        super().__init__()
        self.owner = owner
        self.expode = explode
        self.cooldown = cooldown
        self.explosion_time = explosion_time
        self.cooldown_timer = 0
        self.timer = 0
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(self.image, (230, 40, 40), (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=owner.rect.center)

    def update(self, players, delta_time):
        
        self.timer += delta_time
        self.cooldown_timer += delta_time
        self.rect.center = self.owner.rect.center
        
        if (self.timer >= self.explosion_time):
            self.expode(self.owner)
        
        if self.cooldown_timer < self.cooldown:
            return
        
        for player in players:
            if player is self.owner:
                continue
            
            if pg.sprite.collide_rect(self, player):
                self.owner = player
                self.cooldown_timer = 0
                #todo - Play sound
                break