import pygame
from asset_loader import *

class Heal:
    width = 64
    cost = 50
    img = heal_img

class Zoom:
    width = 64
    cost = 50
    img = zoom_img
    surface = pygame.Surface((64, 37), pygame.SRCALPHA, 32)


