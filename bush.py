import pygame
from asset_loader import *
from random import *

class Particle:
    def __init__(self, x, y):
        self.ttl = 200

        if randint(0, 2):
            self.color = (255, randint(0, 150), 0)
            self.size = randint(0, 5)
        else:
            rand = randint(20, 70)
            self.color = (rand, rand, rand)
            self.size = randint(0, 3)
        self.speed = (uniform(-0.1, 0.1), uniform(-0.01, -0.5))
        self.x = x
        self.y = y


class Bush:
    x = 0
    y = 0
    width = 64
    height = 64
    offset = 0

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, stage):
        if stage == 0:
            self.img = bush_img
        elif stage == 1:
            self.img = bush_img_yellow
        elif stage == 2:
            self.img = bush_img_blue
        elif stage == 3:
            self.img = bush_img_red
            self.offset = 20
        self.x = x
        self.y = y
        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)
        self.prev_time = pygame.time.get_ticks()
        self.particles = []

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def draw(self, screen, x_offset, y_offset, stage):
        if pygame.time.get_ticks() - self.prev_time > 150:
            self.prev_time = pygame.time.get_ticks()
            self.particles.append(Particle(randint(self.x, self.x + self.width), randint(self.y, self.y + self.height)))

        if stage != 3:
            self.shadow_surface.fill((0, 0, 0, 0))
            self.shadow_surface.blit(self.shadow, (0, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (int(self.width), int(self.height * 0.5))), (self.x + 5 + x_offset, self.y + self.height * 0.7 + y_offset))
        screen.blit(self.img, (self.x + x_offset, self.y + y_offset + self.offset))

        if stage == 3:
            for particle in self.particles:
                self.draw_rect_alpha(screen, (particle.color[0], particle.color[1], particle.color[2], 50),
                                 pygame.Rect(particle.x + x_offset - 2, particle.y + y_offset - 2, particle.size + 4,
                                             particle.size + 4))

                pygame.draw.rect(screen, particle.color,
                                 pygame.Rect(particle.x + x_offset, particle.y + y_offset, particle.size,
                                             particle.size))
                particle.x += particle.speed[0]
                particle.y += particle.speed[1]
                particle.ttl -= 1
                if particle.ttl < 0:
                    self.particles.remove(particle)



