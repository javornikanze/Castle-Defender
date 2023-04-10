import pygame
from asset_loader import *

class Barrier:
    x = 0
    y = 0
    width = 100
    height = 64

    cost = 50

    img = barrier_img
    surface = pygame.Surface((64, 37), pygame.SRCALPHA, 32)

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, stage):
        self.x = x
        self.y = y

        print(stage)

        if stage == 0:
            self.hp = 300
            self.max_hp = 300
        elif stage == 1:
            self.hp = 255
            self.max_hp = 230
        elif stage == 2:
            self.hp = 200
            self.max_hp = 200
        elif stage == 3:
            self.hp = 180
            self.max_hp = 180

        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((64, 32), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

    def draw(self, screen, x_offset, y_offset, start):
        if start and self.hp < self.max_hp:
            self.hp += 0.01
        self.shadow_surface.fill((0, 0, 0, 0))
        self.shadow_surface.blit(self.shadow, (0, 0))
        screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                           (self.width, int(self.height * 0.5))), (self.x + 5 + x_offset, self.y + self.height * 0.7 + y_offset))
        screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))

        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(self.x + x_offset + 10 - 2, self.y + y_offset - 20 - 1, 80 + 4, 10 + 2))
        pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.x + x_offset + 10, self.y + y_offset - 20, 80, 10))
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(self.x + x_offset + 90.9 - ((self.max_hp - (self.hp)) / self.max_hp) * 80,
                                     self.y + y_offset - 20,
                                     ((self.max_hp - (self.hp)) / self.max_hp) * 80, 10))

        lines = int(self.max_hp / 12)

        for i in range(lines):
            pygame.draw.line(screen, (60, 60, 60), (self.x + x_offset + i * (80 / lines) + 10, self.y + y_offset - 20),
                             (self.x + x_offset + i * (80 / lines) + 10, self.y + y_offset - 15))

        for i in range(4):
            pygame.draw.line(screen, (60, 60, 60),
                             (self.x + x_offset + (int(lines * ((i + 1) / 4))) * (80 / lines) - 1,
                              self.y + y_offset - 20),
                             (self.x + x_offset + (int(lines * ((i + 1) / 4))) * (80 / lines) - 1,
                              self.y + y_offset - 14), 2)

