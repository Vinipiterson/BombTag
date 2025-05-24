import pygame as pg
GRAVITY = 1

class Player(pg.sprite.Sprite):
    def __init__(self, sprite_path, start_pos, controls, speed=10, jump_strenght=-25, size=(40, 48)):
        super().__init__()
        self.controls = controls
        self.speed = speed
        self.jump_strenght = jump_strenght
        self.y_vel = 0
        self.x_vel = 0
        self.grounded = False

        img = pg.transform.scale(pg.image.load(sprite_path).convert_alpha(), size)
        self.img_left  = img
        self.img_right = pg.transform.flip(img, True, False)

        self.image = self.img_right
        self.rect  = self.image.get_rect(center=start_pos)

    def update(self, keys, platforms, screen_rect):
        # Calculate X velocity based on input
        x_vel = 0
        if keys[self.controls['left']]:
            x_vel = -self.speed
            self.image = self.img_left
        elif keys[self.controls['right']]:
            x_vel =  self.speed
            self.image = self.img_right

        # Move x axis based on velocity, then apply collision
        self.rect.x += x_vel
        if x_vel != 0:
            hits = pg.sprite.spritecollide(self, platforms, False)
            for p in hits:
                if x_vel > 0:        #~ moving right
                    self.rect.right = p.rect.left
                else:                #~ moving left
                    self.rect.left  = p.rect.right

        #~ jump only if on ground
        if keys[self.controls['up']] and self.grounded:
            self.y_vel = self.jump_strenght

        #~ apply gravity and move on Y
        self.y_vel += GRAVITY
        self.rect.y += self.y_vel

        #~ vertical collisions
        self.grounded = False
        hits = pg.sprite.spritecollide(self, platforms, False)
        for p in hits:
            if self.y_vel > 0:       #~ falling
                self.rect.bottom = p.rect.top
                self.grounded = True
            elif self.y_vel < 0:     #~ rising
                self.rect.top = p.rect.bottom
            self.y_vel = 0

        #~ keep player inside the screen
        self.rect.clamp_ip(screen_rect)