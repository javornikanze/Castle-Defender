import pygame
from asset_loader import *

class Castle:
    x = 0
    y = 0
    width = 512
    height = 312
    hp = 0

    surface = pygame.Surface((512, 512), pygame.SRCALPHA, 32)

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, stage):
        if stage == 0:
            self.img = castle_img
            self.hp = 800
            self.max_hp = 800
        elif stage == 1:
            self.img = castle_img
            self.hp = 600
            self.max_hp = 600
        elif stage == 2:
            self.img = castle_img_blue
            self.hp = 400
            self.max_hp = 400
        elif stage == 3:
            self.img = castle_img_red
            self.hp = 200
            self.max_hp = 200

        self.x = x
        self.y = y + 175

        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((512, 512), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

    def draw(self, screen, x_offset, y_offset, start):

        if start and self.hp < self.max_hp:
            self.hp += 0.01

        self.shadow_surface.fill((0, 0, 0, 0))
        self.shadow_surface.blit(self.shadow, (0, 0))

        screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                           (self.width, int(self.height * 0.9))), (self.x + x_offset, self.y + self.height + y_offset- 125))

        screen.blit(self.img, (self.x + x_offset, self.y + y_offset - 175))

        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(self.x + x_offset + 108 - 2, self.y + y_offset + 50 - 135 - 2, 300 + 4, 15 + 4))
        pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.x + x_offset + 108, self.y + y_offset + 50 - 135, 300, 15))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x + x_offset + 409 - ((self.max_hp - (self.hp)) / self.max_hp) * 300, self.y + y_offset + 50 - 135, ((self.max_hp - (self.hp)) / self.max_hp) * 300, 15))

        lines = int(self.max_hp / 12)

        for i in range(lines):
            pygame.draw.line(screen, (60, 60, 60), (self.x + x_offset + i * (300 / lines) + 108, self.y + 70 + y_offset - 20 - 135),
                             (self.x + x_offset + i * (300 / lines) + 108, self.y + 70 + y_offset - 15 - 135))

        for i in range(4):
            pygame.draw.line(screen, (60, 60, 60),
                             (self.x + x_offset + 108 + (int(lines * ((i + 1) / 4))) * (300 / lines) - 1,
                              self.y + y_offset - 20 + 70 - 135),
                             (self.x + x_offset + 108 + (int(lines * ((i + 1) / 4))) * (300 / lines) - 1,
                              self.y + y_offset - 14 + 70 - 135), 2)

