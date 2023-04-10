import pygame
from asset_loader import *

class MenuItem:
    x = 0
    y = 0
    width = 256
    height = 80
    item = ""

    img = quit_img

    def __init__(self, x, y, item):
        self.x = x
        self.y = y

        self.item = item

        if item == "quit":
            self.img = quit_img
        elif item == "resume":
            self.img = resume_img
        elif item == "settings":
            self.img = settings_img

    def draw(self, screen, size):
        screen.blit(pygame.transform.scale(self.img, (self.width - size, self.height - size)), (self.x + (size / 2), self.y + (size)))


