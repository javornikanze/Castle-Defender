import pygame
import math
from random import *
import player
import castle
from asset_loader import *

class Enemy:
    x = 0
    y = 0
    width = 64
    height = 128
    speed = 0
    hp = 0

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, width, height, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 1
        self.hp = hp
        self.max_hp = hp
        self.attack_range = 150

        self.movement = [0, 0, 0, 0]

        self.attack_img = attack_img
        self.surface_attack = pygame.Surface((32, 32), pygame.SRCALPHA, 32)

        self.img = enemy_img
        self.surface = pygame.Surface((32, 64), pygame.SRCALPHA, 32)

        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((32, 64), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        self.frame = 0

        self.attack = 0
        self.attack_frame = 10

        self.prev_frame = 0

        self.prev_pos = [0, 0]

        self.axis = True
        self.rand_offset = 50
        self.rand_dir = randint(0, 1)

        self.closest_target = 0
        self.distance_to_closest_target = 0

        self.target_x = 0
        self.target_y = 0

        self.x_kb = 0
        self.y_kb = 0

        self.x_placement = 500 #some middle ground values
        self.y_placement = 300
        self.draw_arrow = False
        self.freeze_shadow = False

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def move(self, target_lists, lists_of_obj, plyr, x_offset, y_offset, arrows, frame):
        tmp = target_lists[0][0]
        self.closest_target = tmp

        if frame > self.prev_frame:
            self.prev_frame = frame
            self.attack_frame += 0.8
        else:
            self.prev_frame = 0

        shortest_dist = self.distance(self.x + (self.width / 2), self.y + self.height / 2, tmp.x + tmp.width / 2, tmp.y + tmp.height / 2)
        self.distance_to_closest_target = shortest_dist

        self.target_x = tmp.x + tmp.width / 2 - self.width / 2
        self.target_y = tmp.y + tmp.height / 2 - self.height / 2
        for target_list in target_lists:
            for item in target_list:
                new_dist = self.distance(self.x + (self.width / 2), self.y + self.height / 2, item.x + item.width / 2, item.y + item.height / 2)
                if new_dist < shortest_dist:
                    shortest_dist = new_dist
                    self.target_x = item.x + item.width / 2 - self.width / 2
                    self.target_y = item.y + item.height / 2 - self.height / 2
                    self.closest_target = item
                    self.distance_to_closest_target = new_dist

        if self.distance_to_closest_target > 120:
            for target_list in target_lists:
                for item in target_list:
                    if isinstance(item, castle.Castle):
                        self.target_x = item.x + item.width / 2 - self.width / 2
                        self.target_y = item.y + item.height / 2 - self.height / 2

        for i in range(4):
            self.movement[i] = 0

        if randint(0, 50) == 50:
            self.axis = not self.axis

        if abs(self.target_y - self.y) < self.rand_offset:
            self.axis = False

        if abs(self.target_x - self.x) < self.rand_offset:
            self.axis = True

        if self.axis:
            if self.target_y < self.y:
                self.movement[0] = 1
            if self.target_y > self.y:
                self.movement[1] = 1
        else:
            if self.target_x < self.x:
                self.movement[2] = 1
            if self.target_x > self.x:
                self.movement[3] = 1

        if self.movement[0] == 1:
            self.y -= self.speed
            self.check_collision(0, lists_of_obj)
        if self.movement[1] == 1:
            self.y += self.speed
            self.check_collision(1, lists_of_obj)
        if self.movement[2] == 1:
            self.x -= self.speed
            self.check_collision(2, lists_of_obj)
        if self.movement[3] == 1:
            self.x += self.speed
            self.check_collision(3, lists_of_obj)

        if self.x_kb != 0:
            self.x += self.x_kb
            self.check_collision(5, lists_of_obj)

        if self.x_kb > 0:
            self.x_kb -= (1/(abs(self.x_kb) * 5))
        elif self.x_kb < 0:
            self.x_kb += (1/(abs(self.x_kb) * 5))

        if self.y_kb != 0:
            self.y += self.y_kb
            self.check_collision(6, lists_of_obj)

        if self.y_kb > 0:
            self.y_kb -= (1/(abs(self.x_kb) * 5))
        elif self.y_kb < 0:
            self.y_kb += (1/(abs(self.x_kb) * 5))

        if abs(self.x_kb) < 1:
            self.x_kb = 0

        if abs(self.y_kb) < 1:
            self.y_kb = 0

        if self.x == self.prev_pos[0] and self.y == self.prev_pos[1]:
            frame = 4
            self.freeze_shadow = True
            if self.attack_frame > 50:
                dist_to_player = math.sqrt(math.pow((plyr.x - x_offset) - self.x, 2) + math.pow((plyr.y - y_offset) - self.y, 2)) / 100
                #print(dist_to_player)
                #print(plyr.x - x_offset, self.x)
                if isinstance(self.closest_target, player.tmp_player) and self.distance_to_closest_target < 100:
                    self.attack_frame = 0
                    plyr.hp -= 5
                    if plyr.x - x_offset < self.x:
                        slash5r_sound.set_volume(1 / dist_to_player)
                        pygame.mixer.Sound.play(slash5r_sound)
                    else:
                        slash5l_sound.set_volume(1 / dist_to_player)
                        pygame.mixer.Sound.play(slash5l_sound)
                elif isinstance(self.closest_target, castle.Castle) and self.distance_to_closest_target < self.attack_range * 2.5:
                    self.attack_frame = 0
                    self.closest_target.hp -= 5
                    self.draw_arrow = True
                    if plyr.x - x_offset < self.x:
                        slash5r_sound.set_volume(1 / dist_to_player)
                        pygame.mixer.Sound.play(slash5r_sound)
                    else:
                        slash5l_sound.set_volume(1 / dist_to_player)
                        pygame.mixer.Sound.play(slash5l_sound)
                elif self.distance_to_closest_target < self.attack_range and not isinstance(self.closest_target, player.tmp_player):
                    self.attack_frame = 0
                    self.closest_target.hp -= 5
                    self.draw_arrow = True
                    if plyr.x - x_offset < self.x:
                        slash5r_sound.set_volume(1 / dist_to_player)
                        pygame.mixer.Sound.play(slash5r_sound)
                    else:
                        slash5l_sound.set_volume(1 / dist_to_player)
                        pygame.mixer.Sound.play(slash5l_sound)

            if isinstance(self.closest_target, castle.Castle) and self.distance_to_closest_target < self.attack_range * 2.5:
                self.x_placement = self.x + self.width / 2 + x_offset
                self.y_placement = self.y + self.height + y_offset
            elif self.distance_to_closest_target < self.attack_range:
                self.x_placement = self.x + self.width / 2 + x_offset
                self.y_placement = self.y + self.height + y_offset
        else:
            self.draw_arrow = False
            self.freeze_shadow = False

        #print(self.x_placement, self.y_placement)
        if self.draw_arrow:
            if self.x_placement < 0:
                y = (plyr.y + self.y_placement * 3) / 4
                if y > 820:
                    y = 820
                elif y < 50:
                    y = 50
                x = 50
            elif self.x_placement > 1600:
                y = (plyr.y + self.y_placement * 3) / 4
                if y > 820:
                    y = 820
                elif y < 50:
                    y = 50
                x = 1500
            if self.y_placement < 0:
                x = (plyr.x + self.x_placement * 3) / 4
                if x > 1500:
                    x = 1500
                elif x < 50:
                    x = 50
                y = 50
            elif self.y_placement > 1000:
                x = (plyr.x + self.x_placement * 3) / 4
                if x > 1500:
                    x = 1500
                elif x < 50:
                    x = 50
                y = 820
            if 'x' in locals() and 'y' in locals():
                arrows.append((x, y, math.atan2(plyr.y - self.y_placement, plyr.x - self.x_placement)))

        self.prev_pos[0] = self.x
        self.prev_pos[1] = self.y

        self.surface.fill((0, 0, 0, 0))
        self.shadow_surface.fill((0, 0, 0, 0))
        self.surface_attack.fill((0, 0, 0, 0))
        self.surface_attack.blit(self.attack_img, (int(self.attack_frame) * -32, 0))

    def check_collision(self, dir, lists_of_obj):
        for list in lists_of_obj:
            for item in list:
                if self.x == item.x and self.y == item.y:
                    continue

                if self.x + 10 < item.x + item.width and self.x + self.width - 10 > item.x:
                    if dir == 0 and item.y + item.height / 4 < self.y + self.height / 2 < item.y + item.height:
                        self.y += self.speed

                    if dir == 1 and item.y + item.height / 4 < self.y + self.height < item.y + item.height:
                        self.y -= self.speed

                    if dir == 5 and self.y_kb < 0 and item.y + item.height / 4 < self.y + self.height / 2 < item.y + item.height:
                        self.y -= self.y_kb

                    if dir == 5 and self.y_kb > 0 and item.y + item.height / 4 < self.y + self.height < item.y + item.height:
                        self.y -= self.y_kb

                if self.y + self.height / 2 < item.y + item.height and self.y + self.height > item.y + item.height / 4:
                    if dir == 2 and item.x < self.x + 10 < item.x + item.width:
                        self.x += self.speed

                    if dir == 3 and item.x < self.x + self.width - 10 < item.x + item.width:
                        self.x -= self.speed

                    if dir == 6 and self.x_kb < 0 and item.x < self.x + 10 < item.x + item.width:
                        self.x -= self.x_kb

                    if dir == 6 and self.x_kb > 0 and item.x < self.x + self.width - 10 < item.x + item.width:
                        self.x -= self.x_kb


    def draw(self, screen, frame, x_offset, y_offset):
        pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(self.x + x_offset - 2, self.y + y_offset - 20 - 1, 60 + 4, 10 + 2))
        pygame.draw.rect(screen, (185, 20, 255), pygame.Rect(self.x + x_offset, self.y + y_offset - 20, 60, 10))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x + x_offset + 60 - ((self.max_hp - (self.hp)) / self.max_hp) * 60, self.y + y_offset - 20, ((self.max_hp - (self.hp)) / self.max_hp) * 60, 10))

        lines = int(self.max_hp / 10)

        for i in range(lines):
            pygame.draw.line(screen, (60, 60, 60), (self.x + x_offset + i * (60 / lines), self.y + y_offset - 20), (self.x + x_offset + i * (60 / lines), self.y + y_offset - 15))

        for i in range(4):
            pygame.draw.line(screen, (60, 60, 60),
                         (self.x + x_offset + (int(lines * ((i + 1) / 4))) * (60 / lines) - 1,
                          self.y + y_offset - 20),
                         (self.x + x_offset + (int(lines * ((i + 1) / 4))) * (60 / lines) - 1,
                          self.y + y_offset - 14), 2)

        if self.freeze_shadow:
            frame = 4
        if self.movement[3] == 1 and self.movement[2] == 0:
            self.surface.blit(self.img, (frame * -32, 1 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))
            screen.blit(pygame.transform.scale(self.surface_attack, (64, 64)), (self.x + 50 + x_offset, self.y + 50 + y_offset))
        elif self.movement[2] == 1 and self.movement[3] == 0:
            self.surface.blit(self.img, (frame * -32, 2 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.surface_attack, True, False), (64, 64)), (self.x - 50 + x_offset, self.y + 50 + y_offset))
        elif self.movement[1] == 1 and self.movement[0] == 0:
            self.surface.blit(self.img, (frame * -32, 3 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))
            screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.surface_attack, True, False), 100), (196, 48)), (self.x - 60 + x_offset, self.y + 50 + y_offset))
        elif self.movement[0] == 1 and self.movement[1] == 0:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.surface_attack, False, True), 80), (196, 48)), (self.x - 70 + x_offset, self.y + 50 + y_offset))
            self.surface.blit(self.img, (frame * -32, 4 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))
        else:
            self.surface.blit(self.img, (frame * -32, 0 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x + x_offset, self.y + y_offset))
            screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.surface_attack, True, False), 100), (196, 48)), (self.x - 60 + x_offset, self.y + 50 + y_offset))



    def draw_shadow(self, screen, frame, x_offset, y_offset):
        if self.freeze_shadow:
            frame = 4

        if self.movement[3] == 1 and self.movement[2] == 0:
            self.shadow_surface.blit(self.shadow, (frame * -32, 1 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + self.height + y_offset))
        elif self.movement[2] == 1 and self.movement[3] == 0:
            self.shadow_surface.blit(self.shadow, (frame * -32, 2 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + self.height + y_offset))
        elif self.movement[1] == 1 and self.movement[0] == 0:
            self.shadow_surface.blit(self.shadow, (frame * -32, 3 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + self.height + y_offset))
        elif self.movement[0] == 1 and self.movement[1] == 0:
            self.shadow_surface.blit(self.shadow, (frame * -32, 4 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + self.height + y_offset))
        else:
            self.shadow_surface.blit(self.shadow, (frame * -32, 0 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x + x_offset, self.y + self.height + y_offset))
