import pygame
from asset_loader import *
from random import *
from bush import *

class Player:
    x = 0
    y = 0
    width = 64
    height = 128
    x_offset = 0
    y_offset = 0
    speed = 0
    hp = 150
    max_hp = 150
    gold = 0

    def __lt__(self, other):
        return self.y - self.y_offset < other.y

    def __init__(self, x, y, width, height, stage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.hp = 150
        self.max_hp = 150
        if stage == 0:
            self.gold = 1200
        elif stage == 1:
            self.gold = 1000
        elif stage == 2:
            self.gold = 800
        elif stage == 3:
            self.gold = 600

        self.score = 0

        self.movement = [0, 0, 0, 0]

        self.attack_img = slash_img
        self.surface_attack = pygame.Surface((32, 32), pygame.SRCALPHA, 32)

        self.img = player_img
        self.surface = pygame.Surface((32, 64), pygame.SRCALPHA, 32)

        self.shadow = self.img.copy()
        self.shadow_surface = pygame.Surface((32, 64), pygame.SRCALPHA, 32)
        alpha = 96
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        self.frame = 0
        self.prev_frame = 0
        self.attack = 0
        self.attack_frame = 10

        self.draw_dir = [False, False, False, False]
        self.prev_time = 0
        self.animate = True
        self.idle = True

    def attack_enemy(self, enemies):
        for enemy in enemies:
            if abs(enemy.x - (self.x - self.x_offset)) < 150 and abs((enemy.y - enemy.height / 3) - (self.y - self.y_offset)) < 150:
                enemy.hp -= 20
                if enemy.x > (self.x - self.x_offset):
                    enemy.x_kb = 3
                else:
                    enemy.x_kb = -3

                if enemy.y > (self.y - self.y_offset):
                    enemy.y_kb = 3
                else:
                    enemy.y_kb = -3

    def check_keys(self, event, enemies):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.movement[0] = 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.movement[1] = 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.movement[2] = 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.movement[3] = 1
            if event.key == pygame.K_SPACE:
                if self.attack_frame > 12:
                    rand = randint(0, 3)
                    if rand == 0:
                        pygame.mixer.Sound.play(slash1_sound)
                    elif rand == 1:
                        pygame.mixer.Sound.play(slash2_sound)
                    elif rand == 2:
                        pygame.mixer.Sound.play(slash3_sound)
                    elif rand == 3:
                        pygame.mixer.Sound.play(slash4_sound)

                    self.attack_enemy(enemies)
                    self.attack_frame = 0
                    self.prev_time = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.movement[0] = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.movement[1] = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.movement[2] = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.movement[3] = 0

        for key in self.movement:
            if key:
                return True

        return False


    def move(self, lists_of_obj):
        if self.movement[0] == 1:
            self.y_offset += self.speed
            self.check_collision(0, lists_of_obj)
        if self.movement[1] == 1:
            self.y_offset -= self.speed
            self.check_collision(1, lists_of_obj)
        if self.movement[2] == 1:
            self.x_offset += self.speed
            self.check_collision(2, lists_of_obj)
        if self.movement[3] == 1:
            self.x_offset -= self.speed
            self.check_collision(3, lists_of_obj)

        self.check_collision(4, lists_of_obj)




    def check_collision(self, dir, lists_of_obj):
        for list in lists_of_obj:
            for item in list:
                if self.x + 10 - self.x_offset < item.x + item.width and self.x + self.width - self.x_offset - 10 > item.x:
                    if dir == 0 and item.y + item.height / 4 < self.y + self.height * 0.75 - self.y_offset < item.y + item.height:
                        if isinstance(item, Bush) and item.offset == 20:
                            self.hp -= 1
                        else:
                            self.y_offset -= self.speed
                    if dir == 1 and item.y + item.height / 4 < self.y + self.height - self.y_offset < item.y + item.height:
                        if isinstance(item, Bush) and item.offset == 20:
                            self.hp -= 1
                        else:
                            self.y_offset += self.speed
                    if dir == 4 and isinstance(item, Bush) and item.offset == 20 and item.y + item.height / 4 < self.y + self.height - self.y_offset < item.y + item.height:
                        self.hp -= 1

                if self.y + self.height * 0.75 - self.y_offset < item.y + item.height and self.y + self.height - self.y_offset > item.y + item.height / 4:
                    if dir == 2 and item.x < self.x + 10 - self.x_offset < item.x + item.width:
                        if isinstance(item, Bush) and item.offset == 20:
                            self.hp -= 1
                        else:
                            self.x_offset -= self.speed
                    if dir == 3 and item.x < self.x + self.width - 10 - self.x_offset < item.x + item.width:
                        if isinstance(item, Bush) and item.offset == 20:
                            self.hp -= 1
                        else:
                            self.x_offset += self.speed
                    if dir == 4 and isinstance(item, Bush) and item.offset == 20 and item.x < self.x + self.width - 10 - self.x_offset < item.x + item.width:
                        self.hp -= 1




    def draw(self, screen, frame, start):

        if start and self.hp < self.max_hp:
            self.hp += 0.01

        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(self.x - 2, self.y - 20, 60 + 4, 12))
        pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(self.x, self.y - 19, 60, 10))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x + 61 - ((self.max_hp - (self.hp)) / self.max_hp) * 60, self.y - 19, ((self.max_hp - (self.hp)) / self.max_hp) * 60, 10))

        lines = int(self.max_hp / 10)

        for i in range(lines):
            pygame.draw.line(screen, (60, 60, 60), (self.x + i * (60 / lines), self.y - 20),
                             (self.x + i * (60 / lines), self.y - 15))

        for i in range(4):
            pygame.draw.line(screen, (60, 60, 60),
                             (self.x + (int(lines * ((i + 1) / 4))) * (60 / lines) - 1,
                              self.y - 20),
                             (self.x + (int(lines * ((i + 1) / 4))) * (60 / lines) - 1,
                              self.y - 14), 2)

        if frame > self.prev_frame:
            self.prev_frame = frame
            self.attack_frame += 0.8
        else:
            self.prev_frame = 0

        self.surface.fill((0, 0, 0, 0))
        self.shadow_surface.fill((0, 0, 0, 0))
        self.surface_attack.fill((0, 0, 0, 0))
        self.surface_attack.blit(self.attack_img, (int(self.attack_frame) * -32, 0))

        if self.movement[3] == 1 and self.movement[2] == 0:
            self.draw_dir[0] = True
            self.draw_dir[1] = False
            self.draw_dir[2] = False
            self.draw_dir[3] = False
            self.idle = False
            self.prev_time = pygame.time.get_ticks()
        elif self.movement[2] == 1 and self.movement[3] == 0:
            self.draw_dir[1] = True
            self.draw_dir[0] = False
            self.draw_dir[2] = False
            self.draw_dir[3] = False
            self.idle = False
            self.prev_time = pygame.time.get_ticks()
        elif self.movement[1] == 1 and self.movement[0] == 0:
            self.draw_dir[2] = True
            self.draw_dir[1] = False
            self.draw_dir[0] = False
            self.draw_dir[3] = False
            self.idle = False
            self.prev_time = pygame.time.get_ticks()
        elif self.movement[0] == 1 and self.movement[1] == 0:
            self.draw_dir[3] = True
            self.draw_dir[1] = False
            self.draw_dir[2] = False
            self.draw_dir[0] = False
            self.idle = False
            self.prev_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.prev_time > 1000:
            for i in range(4):
                self.draw_dir[i] = False
            self.idle = True

        self.animate = False
        for i in range(4):
            if self.movement[i] == 1:
                self.animate = True
        if self.idle:
            self.animate = True

        if not self.animate:
            frame = 4

        if self.draw_dir[0]:
            self.surface.blit(self.img, (frame * -32, 1 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x, self.y))
            screen.blit(pygame.transform.scale(self.surface_attack, (64, 64)), (self.x + 50, self.y + 50))
        elif self.draw_dir[1]:
            self.surface.blit(self.img, (frame * -32, 2 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x, self.y))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.surface_attack, True, False), (64, 64)), (self.x - 50, self.y + 50))
        elif self.draw_dir[2]:
            self.surface.blit(self.img, (frame * -32, 3 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x, self.y))
            screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.surface_attack, True, False), 100), (196, 48)), (self.x - 60, self.y + 50))
        elif self.draw_dir[3]:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.surface_attack, False, True), 80), (196, 48)), (self.x - 70, self.y + 50))
            self.surface.blit(self.img, (frame * -32, 4 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x, self.y))
        else:
            self.surface.blit(self.img, (frame * -32, 0 * -64))
            screen.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (self.x, self.y))
            screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.surface_attack, True, False), 100), (196, 48)), (self.x - 60, self.y + 50))



    def draw_shadow(self, screen, frame):
        if not self.animate:
            frame = 4
        if self.draw_dir[0]:
            self.shadow_surface.blit(self.shadow, (frame * -32, 1 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x, self.y + self.height))
        elif self.draw_dir[1]:
            self.shadow_surface.blit(self.shadow, (frame * -32, 2 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x, self.y + self.height))
        elif self.draw_dir[2]:
            self.shadow_surface.blit(self.shadow, (frame * -32, 3 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x, self.y + self.height))
        elif self.draw_dir[3]:
            self.shadow_surface.blit(self.shadow, (frame * -32, 4 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x, self.y + self.height))
        else:
            self.shadow_surface.blit(self.shadow, (frame * -32, 0 * -64))
            screen.blit(pygame.transform.scale(pygame.transform.flip(self.shadow_surface, False, True),
                                               (self.width, int(self.height * 0.5))), (self.x, self.y + self.height))

class tmp_player:
    x = 0
    y = 0
    width = 0
    height = 0

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height