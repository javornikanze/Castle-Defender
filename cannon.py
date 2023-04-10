import pygame
import math
import cannonball as c
from asset_loader import *
from random import *

class Cannon:
    x = 0
    y = 0
    width = 64
    height = 64
    rotation = 0
    ticks = 0
    ticks2 = 0
    cannonballs = []
    frame = 8
    hp = 0
    cost = 100
    img = cannon_img

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, ticks):
        self.x = x
        self.y = y
        self.ticks = ticks
        self.ticks2 = ticks
        self.cannonballs = []
        self.hp = 175
        self.max_hp = 175

        self.cannon_surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.cannonball = cannonball_img
        self.shot_img = shot_img
        self.shot_surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)

        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        self.shortest_dist = 0
        self.tx = 0
        self.ty = 0

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def draw(self, screen, x_offset, y_offset, start):
        if start and self.hp < self.max_hp:
            self.hp += 0.01

        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(self.x + x_offset - 2, self.y + y_offset - 20 - 1, 60 + 4, 10 + 2))
        pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.x + x_offset, self.y + y_offset - 20, 60, 10))
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(self.x + x_offset + 60.9 - ((self.max_hp - (self.hp)) / self.max_hp) * 60, self.y + y_offset - 20,
                                     ((self.max_hp - (self.hp)) / self.max_hp) * 60, 10))

        lines = int(self.max_hp / 12)

        for i in range(lines):
            pygame.draw.line(screen, (60, 60, 60), (self.x + x_offset + i * (60 / lines), self.y + y_offset - 20),
                             (self.x + x_offset + i * (60 / lines), self.y + y_offset - 15))

        for i in range(4):
            pygame.draw.line(screen, (60, 60, 60),
                             (self.x + x_offset + (int(lines * ((i + 1) / 4))) * (60 / lines) - 1,
                              self.y + y_offset - 20),
                             (self.x + x_offset + (int(lines * ((i + 1) / 4))) * (60 / lines) - 1,
                              self.y + y_offset - 14), 2)

        self.rotation = math.degrees(math.atan2(self.ty - self.y, self.tx - self.x)) + 180

        self.cannon_surface.fill((0, 0, 0, 0))
        self.shadow_surface.fill((0, 0, 0, 0))
        self.shot_surface.fill((0, 0, 0, 0))

        if 65 <= self.rotation < 110:
            self.shadow_surface.blit(self.shadow, (0 * -32, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, False),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.6))
            self.cannon_surface.blit(self.img, (0 * -32, 0))
#
            self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
            screen.blit(
                pygame.transform.rotate(pygame.transform.scale(self.shot_surface, (self.width, self.height)), 90),
                (self.x + x_offset, self.y + y_offset - self.height))
        elif 110 <= self.rotation < 155:
            self.shadow_surface.blit(self.shadow, (6 * -32, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, False),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.6))
            self.cannon_surface.blit(self.img, (6 * -32, 0))
#
            self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
            screen.blit(
                pygame.transform.rotate(pygame.transform.scale(self.shot_surface, (self.width, self.height)), 90),
                (self.x + x_offset, self.y + y_offset - self.height))
        elif 155 <= self.rotation <= 200:
            self.shadow_surface.blit(self.shadow, (3 * -32, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.8))
            self.cannon_surface.blit(self.img, (3 * -32, 0))
#
            self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
            screen.blit(pygame.transform.scale(self.shot_surface, (self.width, self.height)), (self.x + x_offset + self.width, self.y + y_offset - 8))
        elif 200 <= self.rotation <= 245:
           self.shadow_surface.blit(self.shadow, (4 * -32, 0))
           screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                              (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.8))
           self.cannon_surface.blit(self.img, (4 * -32, 0))
#
           self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
           screen.blit(pygame.transform.scale(self.shot_surface, (self.width, self.height)), (self.x + x_offset + self.width, self.y + y_offset - 8))
        elif 245 < self.rotation <= 290:
           self.shadow_surface.blit(self.shadow, (1 * -32, 0))
           screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, False),
                                              (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.5))
           self.cannon_surface.blit(self.img, (1 * -32, 0))

           self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
           screen.blit(
               pygame.transform.rotate(pygame.transform.scale(self.shot_surface, (self.width, self.height)), -90),
               (self.x + x_offset, self.y + y_offset + self.height - 5))
        elif 290 < self.rotation <= 335:
            self.shadow_surface.blit(self.shadow, (5 * -32, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, False),
                                               (self.width, int(self.height * 0.5))),
                        (self.x + x_offset, self.y + y_offset + self.height * 0.5))
            self.cannon_surface.blit(self.img, (5 * -32, 0))
#
            self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
            screen.blit(
                pygame.transform.rotate(pygame.transform.scale(self.shot_surface, (self.width, self.height)), -90),
                (self.x + x_offset, self.y + y_offset + self.height - 5))
        elif 335 <= self.rotation or self.rotation < 20:
            self.shadow_surface.blit(self.shadow, (2 * -32, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.8))
            self.cannon_surface.blit(self.img, (2 * -32, 0))
#
            self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
            screen.blit(pygame.transform.flip(pygame.transform.scale(self.shot_surface, (self.width, self.height)), True, False),
                        (self.x + x_offset - self.width, self.y + y_offset - 8))
        elif 20 <= self.rotation or self.rotation < 65:
            self.shadow_surface.blit(self.shadow, (7 * -32, 0))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + y_offset + self.height * 0.8))
            self.cannon_surface.blit(self.img, (7 * -32, 0))
#
            self.shot_surface.blit(self.shot_img, (self.frame * -32, 0))
            screen.blit(pygame.transform.flip(pygame.transform.scale(self.shot_surface, (self.width, self.height)), True, False),
                        (self.x + x_offset - self.width, self.y + y_offset - 8))

        screen.blit(pygame.transform.scale(self.cannon_surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))

    def shoot(self, enemies, ticks, player_with_offset):
        dist_to_player = math.sqrt(math.pow(player_with_offset.x - self.x, 2) + math.pow(player_with_offset.y - self.y, 2)) / 100

        if ticks - self.ticks > 2000:
            if len(enemies) > 0:
                tmp = enemies[0]
                self.shortest_dist = self.distance(self.x + (self.width / 2), self.y + self.height * 0.9, tmp.x + tmp.width / 2,
                                              tmp.y + tmp.height / 2)
                self.tx = tmp.x + tmp.width / 2 - self.width / 2
                self.ty = tmp.y + tmp.height / 2 - self.height / 2
                for enemy in enemies:
                    new_dist = self.distance(self.x + (self.width / 2), self.y + self.height * 0.9, enemy.x + enemy.width / 2,
                                             enemy.y + enemy.height / 2)
                    if new_dist < self.shortest_dist:
                        self.shortest_dist = new_dist
                        self.tx = enemy.x + enemy.width / 2 - self.width / 2
                        self.ty = enemy.y + enemy.height / 2 - self.height / 2

                if self.shortest_dist < 500:
                    self.cannonballs.append(c.Cannonball(self.x, self.y, self.tx, self.ty, self.cannonball))
                    if player_with_offset.x < self.x:
                        sound_l = 1 / dist_to_player
                        sound_r = sound_l * 0.25
                    else:
                        sound_r = 1 / dist_to_player
                        sound_l = sound_r * 0.25

                    cannon_sound_l.set_volume(sound_l)
                    cannon_sound_r.set_volume(sound_r)
                    print(sound_l, sound_r)
                    pygame.mixer.Sound.play(cannon_sound_l)
                    pygame.mixer.Sound.play(cannon_sound_r)

                    self.ticks = ticks
                    self.frame = 0

        if ticks - self.ticks2 > 80:
            self.frame += 1
            self.ticks2 = ticks

    def move_canonballs(self, screen, x_offset, y_offset, enemies):
        for ball in self.cannonballs:
            ball.move()
            ball.draw(screen, x_offset, y_offset)

            for enemy in enemies:
                if self.distance(ball.x + ball.width / 2, ball.y + ball.height / 2, enemy.x + enemy.width / 2, enemy.y + enemy.height / 2) < 50:
                    self.cannonballs.remove(ball)
                    enemy.hp -= 25
                    return

            if ball.x < -3000 or ball.x > 3000:
                self.cannonballs.remove(ball)
            elif ball.y < -3000 or ball.y > 3000:
                self.cannonballs.remove(ball)



