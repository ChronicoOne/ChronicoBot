import pygame

def colorFromGrayscale(grayscale, color):
    newColor = pygame.Color(color)
    lightness = (grayscale.hsla[2] * 0.5) + (newColor.hsla[2] * 0.5)
    newColor.hsla = (color.hsla[0], color.hsla[1], lightness, grayscale.hsla[3])
    return newColor

def colorSurface(surface, color):
    for j in range(surface.get_width()):
            for k in range(surface.get_height()):
                surface.set_at((j,k), colorFromGrayscale(surface.get_at((j,k)), color))

def stringToColor(string):
    red, green, blue = string.split(",")
    return pygame.Color(int(red), int(green), int(blue))
