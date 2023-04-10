import math

import pygame
from random import *


class Coin:
    x = 0
    y = 0
    width = 24
    height = 24
    surface = pygame.Surface((16, 16), pygame.SRCALPHA, 32)

    prev_frame = 0
    actual_frame = 0

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, coin):
        self.x = x
        self.y = y
        self.img = coin
        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

    def picked_up(self, px, py):
        distance = math.sqrt(math.pow((px + 16) - self.x, 2) + math.pow((py + 96) - self.y, 2))
        if distance < 300:
            radians = math.atan2(self.x - (px + 16), self.y - (py + 96))
            self.y -= math.cos(radians) / math.pow((distance / 200), 2)
            self.x -= math.sin(radians) / math.pow((distance / 200), 2)
            if distance < 50:
                return True
        return False

    def draw(self, screen, frame, x_offset, y_offset):

        self.actual_frame += 0.25
        if self.actual_frame > 8:
            self.actual_frame = 0

        self.shadow_surface.fill((0, 0, 0, 0))
        self.shadow_surface.blit(self.shadow, (int(self.actual_frame) * -16, 0))
        screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                           (self.width, int(self.height * 0.5))), (self.x + 2 + x_offset, self.y + self.height * 0.7 + y_offset))
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.img, (int(self.actual_frame) * -16, 0))
        screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))



