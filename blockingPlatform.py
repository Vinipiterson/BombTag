import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_path, color=(90, 55, 25)):
        super().__init__()
    
        self.image = pg.image.load(sprite_path)
        self.rect = pg.Rect(x, y, self.image.get_width(), self.image.get_height())
        
class Floor(pg.sprite.Sprite):
    def __init__(self, x, y, size = (1920, 64)):
        super().__init__()
    
        self.image = pg.transform.scale(pg.image.load(r"sprites\floor.png").convert_alpha(), size)
        self.rect = pg.Rect(x, y, self.image.get_width(), self.image.get_height())