import pygame
from time import sleep


screen_size = (500, 500)
background_color = (0, 255, 0)

def init_game_surface():
    pygame.init()

    display = pygame.display.set_mode(size=(500,500))

    screen = pygame.Rect(0, 0, *screen_size)

    pygame.draw.rect(display, background_color, screen)

    return display
