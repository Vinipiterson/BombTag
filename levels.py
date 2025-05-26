import random
from blockingPlatform import Platform, Floor
import pygame as pg

s_size = 256
m_size = 384
l_size = 512

def map_1(screen_rect):
    w, h = screen_rect.size
    platforms = []
    
    # Floor
    platforms.append(Floor(0, h-64))
    
    # Small
    platforms.append(Platform(0, h-576, "sprites/platform_small.png"))
    platforms.append(Platform(w - s_size, h-576, "sprites/platform_small.png"))

    # Medium
    platforms.append(Platform(m_size * 0.75, h-320, "sprites/platform_medium.png"))
    platforms.append(Platform(w - (m_size * 1.75), h-320, "sprites/platform_medium.png"))
    platforms.append(Platform(m_size * 0.75, h-832, "sprites/platform_medium.png"))
    platforms.append(Platform(w - (m_size * 1.75), h-832, "sprites/platform_medium.png"))

    # Large
    platforms.append(Platform(w/2 - 256, h-576, "sprites/platform_large.png"))
    
    return pg.sprite.Group(platforms)


def map_2(screen_rect):
    w, h = screen_rect.size
    platforms = []
    
    # Floor
    platforms.append(Floor(0, h-64))

    # Small
    platforms.append(Platform(0, h-320, "sprites/platform_small.png"))
    platforms.append(Platform(w - s_size, h-320, "sprites/platform_small.png"))
    platforms.append(Platform(0, h-832, "sprites/platform_small.png"))
    platforms.append(Platform(w - s_size, h-832, "sprites/platform_small.png"))

    # Medium
    platforms.append(Platform(s_size + 32, h-576, "sprites/platform_medium.png"))
    platforms.append(Platform(w - (s_size * 2.5) - 32, h-576, "sprites/platform_medium.png"))

    # Large
    platforms.append(Platform(w/2 - l_size/2, h-320, "sprites/platform_large.png"))
    platforms.append(Platform(w/2 - l_size/2, h-832, "sprites/platform_large.png"))

    return pg.sprite.Group(platforms)

def map_3(screen_rect):
    w, h = screen_rect.size
    platforms = []

    # Floor
    platforms.append(Floor(0, h - 64))

    # Small (laterais mais baixas)
    platforms.append(Platform(0, h - 704, "sprites/platform_small.png"))
    platforms.append(Platform(w - s_size, h - 704, "sprites/platform_small.png"))

    # Large (meio alto e baixo) — agora mais próximos
    platforms.append(Platform(w/2 - l_size/2, h - 640, "sprites/platform_large.png"))
    platforms.append(Platform(w/2 - l_size/2, h - 320, "sprites/platform_large.png"))

    # Medium (lados médios) — posição ajustada para conectar com o centro
    platforms.append(Platform(s_size * 0.5, h - 480, "sprites/platform_medium.png"))
    platforms.append(Platform(w - s_size * 0.5 - m_size, h - 480, "sprites/platform_medium.png"))

    # Plataforma central extra (opcional)
    # platforms.append(Platform(w/2 - m_size/2, h - 832, "sprites/platform_medium.png"))

    return pg.sprite.Group(platforms)

def get_random_map(screen_rect):
    maps = [map_1, map_2, map_3]
    selected_map = random.choice(maps)
    return selected_map(screen_rect)