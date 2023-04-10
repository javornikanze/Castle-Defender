import pygame
import math

class Cannonball:
    x = 0
    y = 0
    height = 0
    width = 0
    dir_x = 0
    dir_y = 0

    def __init__(self, x, y, tx, ty, cannonball):
        self.x = x + 16
        self.y = y + 16
        self.height = 16
        self.width = 16
        self.img = cannonball

        dx = abs(x - tx)
        dy = abs(y - ty)

        self.dir_x = dx / (dx + dy)
        self.dir_y = dy / (dx + dy)

        if tx < x:
            self.dir_x *= -1

        if ty < y:
            self.dir_y *= -1

        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def move(self):
        self.x += self.dir_x * 10
        self.y += self.dir_y * 10

    def draw(self, screen, x_offset, y_offset):
        self.shadow_surface.fill((0, 0, 0, 0))
        self.shadow_surface.blit(self.shadow, (0, 0))
        screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                           (self.width, int(self.height * 0.5))), (self.x + 5 + x_offset, self.y + 40 + y_offset))
        screen.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))
