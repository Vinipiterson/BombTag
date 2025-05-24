import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, rect, color=(90, 55, 25)):
        super().__init__()
        self.image = pg.Surface((rect.width, rect.height))
        self.image.fill(color)
        self.rect  = rect