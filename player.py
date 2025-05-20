import pygame as pg

gravity = 1

class Player(pg.sprite.Sprite):
    def __init__(self, sprite_path, start_pos, controls, speed=5, size=(48, 48)):
        super().__init__()
        self.controls = controls
        self.speed = speed
        self.y_vel = 0

        # 1) Carrega a imagem e força o tamanho
        raw = pg.image.load(sprite_path).convert_alpha()
        scaled = pg.transform.scale(raw, size)

        self.orig_image = scaled
        self.flip_image = pg.transform.flip(self.orig_image, True, False)

        # Começa usando a original
        self.image = self.orig_image
        self.rect  = self.image.get_rect(center=start_pos)

    def update(self, keys, screen_rect):

        # mover à esquerda
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
            self.image = self.orig_image
        # mover à direita
        if keys[self.controls['right']]:
            self.rect.x += self.speed
            self.image = self.flip_image

        

        if keys[self.controls['up']] and self.rect.bottom >= 500:
            self.y_vel = -12   # valor negativo faz subir

        self.y_vel += gravity
        self.rect.y += self.y_vel

        # mantém dentro da tela
        self.rect.clamp_ip(screen_rect)
