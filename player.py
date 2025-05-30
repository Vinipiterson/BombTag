import pygame as pg
import constants as const

def spawn_players(screen_rect):
    return pg.sprite.Group(
    Player("green", (350, screen_rect.height - 50), const.controls_p1),
    Player('yellow',  (screen_rect.width - 350, screen_rect.height - 50), const.controls_p2)
)

class Player(pg.sprite.Sprite):
    def __init__(self, color, start_pos, controls, size=(64, 64)):
        super().__init__()
        self.controls = controls
        self.speed = const.PLAYER_SPEED
        self.jump_strenght = const.JUMP_STRENGHT
        self.y_vel = 0
        self.x_vel = 0
        self.grounded = False
        self.color = color
        self.expression = "happy"
        self.direction = "right"
        self.happy = pg.transform.scale(pg.image.load(f"sprites/{self.color}/Happy.png").convert_alpha(), size)
        self.mad = pg.transform.scale(pg.image.load(f"sprites/{self.color}/Mad.png").convert_alpha(), size)

        self.image = self.happy
        self.rect  = self.image.get_rect(center=start_pos)

    def update_expression(self, expression):
        self.expression = expression
        
        img = self.happy if self.expression == "happy" else self.mad
        if (self.direction == "left"):
            img = pg.transform.flip(img, True, False)
            
        self.image = img
        
    def update_direction(self, direction):
        self.direction = direction
        
        img = self.happy if self.expression == "happy" else self.mad
        if (self.direction == "left"):
            img = pg.transform.flip(img, True, False)
            
        self.image = img

    def update(self, keys, platforms, screen_rect):
        # Calculate X velocity based on input
        x_vel = 0
        if keys[self.controls['left']]:
            x_vel = -self.speed
            self.update_direction("left")
        elif keys[self.controls['right']]:
            x_vel =  self.speed
            self.update_direction("right")
            
        if keys[self.controls['down']]:
            if (self.y_vel < 0): # is going upwards
                self.y_vel = const.GRAVITY * 10

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
        self.y_vel += const.GRAVITY
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