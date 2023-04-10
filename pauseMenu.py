import pygame
import menuItem as m
from asset_loader import *

class PauseMenu:
    width = 256
    height = 128
    x = 0
    y = 0

    menu = pause_menu_img

    def __init__(self, screen):
        width, height = screen.get_size()
        self.width = int((width / 4.25))
        self.height = int((height / 2))
        self.x = (width / 2) - (self.width / 2)
        self.y = (height / 3) - (self.height / 2)

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.menu, (self.width, self.height)), (self.x, self.y))
