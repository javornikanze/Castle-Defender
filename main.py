import math
import time
import sys
from random import *

import numpy as np

import player as p
import cannon as c
import bush as b
import tree as t
import enemy as e
import castle as cst
import coin as co
import barrier as ba
import shopItem as s
import pauseMenu as pa
import menuItem as m
import settingsMenu as se
from asset_loader import *
import heal as h
import pygame
import pygame_gui
from PIL import Image, ImageFilter

shop_coords = [screen_width - 50]


running = True
pause = False
settings = False


cannons = []
bushes = []
enemies = []
coins = []
#for i in range(20):
#    coins.append(co.Coin(i * 16, 500 * uniform(0.8, 1.2), coin_img))
barriers = []
arrows = []

selected_item = 0
zoom_level = 0

mouse_x = 0
mouse_y = 0

volume = 50
music = 10
mute = False
tutorial = True

file = open("config/config.txt", "r")
if file:
    for line in file:
        line = line.strip().split(":")
        if line[0] == "volume":
            volume = int(line[1])
        if line[0] == "music":
            music = int(line[1])
        if line[0] == "mute_all":
            mute = (line[1] == "True")
        if line[0] == "tutorial":
            tutorial = (line[1] == "True")

    pygame.mixer.music.set_volume(music / 1000)
    cannon_sound_l.set_volume(volume / 100)
    cannon_sound_r.set_volume(volume / 100)
    coin_sound.set_volume(volume / 100)
    walking_sound.set_volume(volume / 100)
    place_down.set_volume(volume / 100)
    slash1_sound.set_volume(volume / 100)
    slash2_sound.set_volume(volume / 100)
    slash3_sound.set_volume(volume / 100)
    slash4_sound.set_volume(volume / 100)
    slash5l_sound.set_volume(volume / 100)
    slash5r_sound.set_volume(volume / 100)

    if mute:
        pygame.mixer.music.set_volume(0)
        cannon_sound_l.set_volume(0)
        cannon_sound_r.set_volume(0)
        coin_sound.set_volume(0)
        walking_sound.set_volume(0)
        place_down.set_volume(0)
        slash1_sound.set_volume(0)
        slash2_sound.set_volume(0)
        slash3_sound.set_volume(0)
        slash4_sound.set_volume(0)
        slash5r_sound.set_volume(0)
        slash5l_sound.set_volume(0)
volume_down = False
volume_up = False
music_down = False
music_up = False
mouse_down = False

start = False
tutorial_state = 0

#font = pygame.font.SysFont("javanesetext", 20)
font2 = pygame.font.SysFont("javanesetext", 40)
waves = open("waves.txt", "r")
last_spawn = pygame.time.get_ticks()


def show_user_name(user_name):
    pygame.mixer.music.play(-1)
    n = 245
    while n > 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((200, 150, 100))
        s = pygame.Surface((screen_width, screen_height))
        s.set_alpha(n)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))
        n -= 0.675

        new_text = font2.render(f"Welcome to Castle defender", False, (255-n, 255-n, 255-n))
        new_text_rect = new_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(new_text, new_text_rect)

        new_text = font2.render(user_name, False, (255 - n, 255 - n, 255 - n))
        new_text_rect = new_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        screen.blit(new_text, new_text_rect)
        actual_screen.blit(pygame.transform.scale(screen, (actual_screen.get_width(), actual_screen.get_height())),
                           (0, 0))
        clock.tick(60)
        pygame.display.update()

pygame.mouse.set_visible(False)
def get_user_name():
    #pygame.mouse.set_visible(False)
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(500, 300)))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(500, 300)))
    b = False
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                pygame.mouse.set_pos([screen_width / 2, screen_height / 2])
                #pygame.mouse.set_visible(True)
                show_user_name(event.text)
                b = True

            manager.process_events(event)
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

        manager.update(UI_REFRESH_RATE)
        if b:
            pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            return
        screen.fill((200, 150, 100))
        new_text = font2.render(f"Enter your nickname", False, (255, 255, 255))
        new_text_rect = new_text.get_rect(center=(screen_width / 2, screen_height / 4 + 20))
        screen.blit(new_text, new_text_rect)
        manager.draw_ui(screen)
        actual_screen.blit(pygame.transform.scale(screen, (actual_screen.get_width(), actual_screen.get_height())),
                           (0, 0))
        pygame.display.update()

get_user_name()
tmp_bg_img = 0
arrow_offset = 0
arrow_scale = 0
arrow_scale_dir = True

stage_select = True

while stage_select:
    mb = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stage_select = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mb = True

    x_scaling = actual_screen.get_width() / screen_width
    y_scaling = actual_screen.get_height() / screen_height
    screen.fill((200, 150, 100))
    ui.fill((0, 0, 0, 0))
    mx, my = pygame.mouse.get_pos()
    mx /= x_scaling
    my /= y_scaling

    if 150 < mx < 790 and 50 < my < 410:
        screen.blit(pygame.transform.scale(s1, (654, 370)), (142, 45))
        if mb:
            stage = 0
            stage_select = False
    else:
        screen.blit(s1, (150, 50))

    if 850 < mx < 1490 and 50 < my < 410:
        screen.blit(pygame.transform.scale(s2, (654, 370)), (840, 45))
        if mb:
            stage = 1
            stage_select = False
    else:
        screen.blit(s2, (850, 50))

    if 150 < mx < 790 and 450 < my < 810:
        screen.blit(pygame.transform.scale(s3, (654, 370)), (140, 440))
        if mb:
            stage = 2
            stage_select = False
    else:
        screen.blit(s3, (150, 450))

    if 850 < mx < 1490 and 450 < my < 810:
        screen.blit(pygame.transform.scale(s4, (654, 370)), (840, 440))
        if mb:
            stage = 3
            stage_select = False
    else:
        screen.blit(s4, (850, 450))


    cursor_img_rect.center = (pygame.mouse.get_pos()[0] / actual_screen.get_width() * 1600,
                              pygame.mouse.get_pos()[1] / actual_screen.get_height() * 900)
    ui.blit(pygame.transform.scale(cursor_img, (int(30 * x_scaling), int(36 * y_scaling))),
            cursor_img_rect)

    actual_screen.blit(pygame.transform.scale(screen, (actual_screen.get_width(), actual_screen.get_height())), (0, 0))
    actual_screen.blit(pygame.transform.scale(ui, (actual_screen.get_width(), actual_screen.get_height())), (0, 0))
    pygame.display.flip()


    clock.tick(60)


player = p.Player(actual_screen.get_width() / 2 - 64, actual_screen.get_height() / 2 - 128, 64, 128, stage)
player.x_offset = 470
player.y_offset = -75
castle = cst.Castle(50, 0, stage)
player_with_offset = p.tmp_player(player.x - player.x_offset, player.y - player.y_offset, 64, 128)

shop_items = [s.ShopItem(screen_width, 40, ba.Barrier(0, 0, stage)), s.ShopItem(screen_width, 170, c.Cannon(0, 0, 0)), s.ShopItem(screen_width, 300, h.Heal()), s.ShopItem(screen_width, 430, h.Zoom())]
menu_items = [m.MenuItem(screen_width / 2 - 130, screen_height / 2 - 250, "resume"), m.MenuItem(screen_width / 2 - 130, screen_height / 2 - 150, "settings"), m.MenuItem(screen_width / 2 - 130, screen_height / 2 - 50, "quit")]
pause_menu = pa.PauseMenu(screen)
settings_menu = se.SettingsMenu(screen)

def draw_ui():
    global start
    global tutorial_state
    global arrow_offset
    global arrow_scale
    global arrow_scale_dir
    mx, my = pygame.mouse.get_pos()
    x_scaling = actual_screen.get_width() / screen_width
    y_scaling = actual_screen.get_height() / screen_height
    curr_screen_width = actual_screen.get_width()
    curr_screen_height = actual_screen.get_height()

    if arrow_scale_dir:
        arrow_scale += 0.1
    else:
        arrow_scale -= 0.1

    if round(arrow_scale) == 10:
        arrow_scale_dir = False
    elif round(arrow_scale) == 0:
        arrow_scale_dir = True

    if tutorial:
        if tutorial_state == 0:
            ui.blit(pygame.transform.scale(pygame.transform.rotate(arrow_img, -90), (40 + int(arrow_scale), 40 + int(arrow_scale))), (1500 + arrow_offset, 90 - int(arrow_scale / 2)))
            ui.blit(t1_img, (1050 + arrow_offset, 80))
        elif tutorial_state == 1:
            ui.blit(pygame.transform.scale(pygame.transform.rotate(arrow_img, -90), (40 + int(arrow_scale), 40 + int(arrow_scale))), (1500 + arrow_offset, 210 - int(arrow_scale / 2)))
            ui.blit(t2_img, (1050 + arrow_offset, 200))
        elif tutorial_state == 2:
            ui.blit(pygame.transform.scale(pygame.transform.rotate(arrow_img, -90), (40 + int(arrow_scale), 40 + int(arrow_scale))), (1170, 780 - int(arrow_scale / 2)))
            ui.blit(t3_img, (740, 640))
        elif tutorial_state == 3:
            ui.blit(t4_img, (30, 140))
        elif tutorial_state == 4:
            ui.blit(t5_img, (30, 140))


    if mx > 1400 * x_scaling:
        for shop_item in shop_items:
            if shop_item.x > screen_width - 160:
                shop_item.x -= 10
        if shop_coords[0] > screen_width - 200:
            shop_coords[0] -= 10
            arrow_offset -= 10
    else:
        for shop_item in shop_items:
            if shop_item.x < screen_width:
                shop_item.x += 10
        if shop_coords[0] < screen_width - 45:
            shop_coords[0] += 10
            arrow_offset += 10

    ui.blit(pygame.transform.scale(ui_img, (320, 100)), (10, 10))
    ui.blit(pygame.transform.scale(shop_img, (190, 600)), (shop_coords[0], 10))

    if not tutorial or (tutorial and tutorial_state == 2):
        if not start and len(enemies) == 0 and screen_width * x_scaling - 350 * x_scaling < mx < screen_width * x_scaling - 50 * x_scaling and screen_height * y_scaling - 150 * y_scaling < my < screen_height * y_scaling - 50 * y_scaling:
            ui.blit(pygame.transform.scale(start_img, (294, 94)), (screen_width - 347, screen_height - 147))
            if pygame.mouse.get_pressed()[0]:
                if (tutorial and tutorial_state == 2):
                    tutorial_state += 1
                else:
                    start = True
                    player.score += 1
        elif not start and len(enemies) == 0:
            ui.blit(pygame.transform.scale(start_img, (300, 100)), (screen_width - 350, screen_height - 150))


    fps_text = font.render(str(int(clock.get_fps())), False, pygame.Color("black"))
    ui.blit(fps_text, (0, -10))

    if player.gold >= 999999:
        gld = "999999..."
    else:
        gld = player.gold

    gold_text = font.render("Gold: " + str(gld), False, (60, 60, 60))
    ui.blit(pygame.transform.scale(gold_text, (int(gold_text.get_width() * 2), int(gold_text.get_height() * 1.5))),
                (33, 18))

    gold_text = font.render("Gold: " + str(gld), False, (252, 198, 3))
    ui.blit(pygame.transform.scale(gold_text, (int(gold_text.get_width() * 2), int(gold_text.get_height() * 1.5))),
                (30, 15))

    if player.score == 0:
        scr = ""
    else:
        scr = player.score

    score_text = font.render("Wave: " + str(scr), False, (60, 60, 60))
    ui.blit(pygame.transform.scale(score_text, (int(score_text.get_width() * 2), int(score_text.get_height() * 1.5))),
                (32, 47))

    score_text = font.render("Wave: " + str(scr), False, (252, 160, 3))
    ui.blit(pygame.transform.scale(score_text, (int(score_text.get_width() * 2), int(score_text.get_height() * 1.5))),
                (30, 45))

    if selected_item != 0:
        selected_item.draw_on_mouse(ui, (mx / actual_screen.get_width()) * 1600 - 32 * (actual_screen.get_width() / screen.get_width()) / x_scaling, (my / actual_screen.get_height()) * 900 - 32 * (actual_screen.get_height() / screen.get_height()) / y_scaling, x_scaling, y_scaling, screen_width_z, screen_height_z)

    for shop_item in shop_items:
        if shop_item.x * x_scaling < mx < shop_item.x * x_scaling + shop_item.width * x_scaling and shop_item.y * y_scaling < my < shop_item.y * y_scaling + shop_item.height * y_scaling:
            shop_item.draw(ui, 8, zoom_level, player.gold)
        else:
            shop_item.draw(ui, 0, zoom_level, player.gold)

    for arrow in arrows:
        ui.blit(pygame.transform.scale(pygame.transform.rotate(arrow_img, math.degrees(-arrow[2]) + 90), (40, 40)), (arrow[0], arrow[1]))
    arrows.clear()

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

trees = []

if stage == 0:
    for i in range(4):
        bushes.append(b.Bush(i * 60 - 180, -120, stage))
        bushes.append(b.Bush(i * 60 - 180, -120, stage))
        bushes.append(b.Bush((i + 11) * 60 - 180, -120, stage))

        bushes.append(b.Bush(i * 60 - 180, 780, stage))
        bushes.append(b.Bush((i + 11) * 60 - 180, 780, stage))

    for i in range(5):
        bushes.append(b.Bush(-240, i * 60 - 120, stage))
        bushes.append(b.Bush(-240, (i + 11) * 60 - 120, stage))

        bushes.append(b.Bush(720, i * 60 - 120, stage))
        bushes.append(b.Bush(720, (i + 11) * 60 - 120, stage))

elif stage == 1:
    bushes.append(b.Bush(560, -130, stage))
    bushes.append(b.Bush(500, -130, stage))
    bushes.append(b.Bush(530, -80, stage))

    bushes.append(b.Bush(-100, -40, stage))
    bushes.append(b.Bush(30, -80, stage))

    bushes.append(b.Bush(-20, 500, stage))
    bushes.append(b.Bush(-10, 560, stage))
    bushes.append(b.Bush(-80, 630, stage))
    bushes.append(b.Bush(-20, 620, stage))

    bushes.append(b.Bush(40, 480, stage))
    bushes.append(b.Bush(40, 530, stage))

    bushes.append(b.Bush(800, 460, stage))
    bushes.append(b.Bush(740, 480, stage))
    bushes.append(b.Bush(750, 530, stage))

    bushes.append(b.Bush(-350, 400, stage))
    bushes.append(b.Bush(-320, 450, stage))
    bushes.append(b.Bush(-386, 450, stage))

elif stage == 2:
    bushes.append(b.Bush(60, -130, stage))
    bushes.append(b.Bush(0, -130, stage))
    bushes.append(b.Bush(30, -80, stage))
    bushes.append(b.Bush(-100, -40, stage))
    bushes.append(b.Bush(530, -80, stage))
    bushes.append(b.Bush(500, 500, stage))
    bushes.append(b.Bush(520, 560, stage))
    bushes.append(b.Bush(584, 560, stage))
    bushes.append(b.Bush(540, 620, stage))

    bushes.append(b.Bush(50, 480, stage))
    bushes.append(b.Bush(10, 600, stage))
    bushes.append(b.Bush(-30, 650, stage))
    bushes.append(b.Bush(36, 650, stage))

elif stage == 3:
    bushes.append(b.Bush(60, -130, stage))
    bushes.append(b.Bush(-280, -460, stage))
    bushes.append(b.Bush(-280, 460, stage))
    bushes.append(b.Bush(-240, 660, stage))
    bushes.append(b.Bush(-80, 860, stage))
    bushes.append(b.Bush(-80, -60, stage))
    bushes.append(b.Bush(530, -70, stage))
    bushes.append(b.Bush(520, 470, stage))
    bushes.append(b.Bush(530, 520, stage))
    bushes.append(b.Bush(590, 520, stage))
    bushes.append(b.Bush(570, 570, stage))
    bushes.append(b.Bush(740, 670, stage))
    bushes.append(b.Bush(580, 860, stage))

trees.append(t.Tree(-130, -20, True, stage))
trees.append(t.Tree(-130, 650, True, stage))

trees.append(t.Tree(600, -20, False, stage))
trees.append(t.Tree(600, 650, False, stage))

trees.append(t.Tree(650, -350, True, stage))
trees.append(t.Tree(-500, 800, False, stage))
trees.append(t.Tree(-300, 1000, False, stage))
trees.append(t.Tree(-350, -220, False, stage))
trees.append(t.Tree(-150, -320, True, stage))
trees.append(t.Tree(900, -120, False, stage))
trees.append(t.Tree(700, 950, False, stage))
trees.append(t.Tree(950, 750, True, stage))

frame = 0
ticks = 0
tutorial_spawn = True

while running:
    if tutorial:
        if tutorial_state == 0:
            if len(barriers) == 4:
                tutorial_state += 1
        elif tutorial_state == 1:
            if len(cannons) == 4:
                tutorial_state += 1
        elif tutorial_state == 3:
            if tutorial_spawn:
                enemies.append(e.Enemy(1500, 160, 64, 128, 40))
                enemies.append(e.Enemy(1500, 270, 64, 128, 40))
                enemies.append(e.Enemy(-800, 160, 64, 128, 40))
                enemies.append(e.Enemy(-800, 270, 64, 128, 40))
                enemies.append(e.Enemy(230, -500, 64, 128, 40))
                enemies.append(e.Enemy(310, -500, 64, 128, 40))
                enemies.append(e.Enemy(230, 1000, 64, 128, 40))
                enemies.append(e.Enemy(310, 1000, 64, 128, 40))
                tutorial_spawn = False
            if len(enemies) == 0:
                tutorial_state += 1
        elif tutorial_state == 4:
            if len(coins) == 0:
                #COMPLETE TUTORIAL MESSAGE
                #SET DEFAULT VALUES (gold, castle and player hp bar, all lists to [])
                screen_width_z = 1600
                screen_height_z = 900
                screen = pygame.transform.scale(screen, (int(screen_width_z), int(screen_height_z)))
                player.x = (screen.get_width() / 2 - 64)
                player.y = (screen.get_height() / 2 - 128)
                zoom_level = 0

                if stage == 0:
                    player.gold = 1200
                elif stage == 1:
                    player.gold = 1000
                elif stage == 2:
                    player.gold = 800
                elif stage == 3:
                    player.gold = 600

                player.hp = player.max_hp
                player.score = 0
                castle.hp = castle.max_hp
                cannons = []
                barriers = []
                enemies = []
                player.x_offset = 470
                player.y_offset = -75
                player.movement = [0, 0, 0, 0]
                tutorial_state += 1



                tutorial = False

    x_scaling = actual_screen.get_width() / screen_width
    y_scaling = actual_screen.get_height() / screen_height
    sc = False
    while pause:
        x_scaling = actual_screen.get_width() / screen_width
        y_scaling = actual_screen.get_height() / screen_height
        if not sc:
            screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
            image = Image.fromarray(np.uint8(screenshot))
            blurred = image.filter(ImageFilter.GaussianBlur(5))
            blurred_arr = np.array(blurred, dtype=np.uint8)
            tmp_bg_img = pygame.surfarray.make_surface(blurred_arr)
            sc = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pause = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx = pygame.mouse.get_pos()[0]
                    my = pygame.mouse.get_pos()[1]
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False


        while settings:
            x_scaling = actual_screen.get_width() / screen_width
            y_scaling = actual_screen.get_height() / screen_height
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    settings = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        settings = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx = pygame.mouse.get_pos()[0]
                        my = pygame.mouse.get_pos()[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx = pygame.mouse.get_pos()[0]
                        my = pygame.mouse.get_pos()[1]

                        if 985 * x_scaling < mx < 1008 * x_scaling and 255 * y_scaling < my < 280 * y_scaling:
                            volume_down = True
                        elif 1012 * x_scaling < mx < 1035 * x_scaling and 255 * y_scaling < my < 280 * y_scaling:
                            volume_up = True
                        elif 985 * x_scaling < mx < 1008 * x_scaling and 300 * y_scaling < my < 325 * y_scaling:
                            music_down = True
                        elif 1012 * x_scaling < mx < 1035 * x_scaling and 300 * y_scaling < my < 325 * y_scaling:
                            music_up = True
                        elif 730 * x_scaling < mx < 750 * x_scaling and 350 * y_scaling < my < 375 * y_scaling:
                            mute = not mute
                        elif 840 * x_scaling < mx < 1060 * x_scaling and 375 * y_scaling < my < 430 * y_scaling:
                            settings = False

                        mouse_down = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        volume_down = False
                        volume_up = False
                        music_down = False
                        music_up = False
                        mouse_down = False

            if mouse_down:
                mx = pygame.mouse.get_pos()[0]
                my = pygame.mouse.get_pos()[1]
                if 730 * x_scaling < mx < 975 * x_scaling and 255 * y_scaling < my < 275 * y_scaling:
                    volume = (mx - 730 * x_scaling) / (975 * x_scaling - 730 * x_scaling) * 100
                elif 730 * x_scaling < mx < 975 * x_scaling and 300 * y_scaling < my < 325 * y_scaling:
                    music = (mx - 730 * x_scaling) / (975 * x_scaling - 730 * x_scaling) * 100

            if volume_down and volume > 0:
                volume -= 1
            elif volume_up and volume < 100:
                volume += 1
            if music_down and music > 0:
                music -= 1
            elif music_up and music < 100:
                music += 1

            ui.blit(pygame.transform.scale(tmp_bg_img, (1600, 900)), (0, 0))

            mx, my = pygame.mouse.get_pos()
            if 840 * x_scaling < mx < 1060 * x_scaling and 375 * y_scaling < my < 430 * y_scaling:
                settings_menu.draw(ui, volume, music, mute, 0)
            else:
                settings_menu.draw(ui, volume, music, mute, 4)


            cursor_img_rect.center = (pygame.mouse.get_pos()[0] / actual_screen.get_width() * 1600,
                                      pygame.mouse.get_pos()[1] / actual_screen.get_height() * 900)
            ui.blit(pygame.transform.scale(cursor_img, (int(30 * x_scaling), int(36 * y_scaling))),
                        cursor_img_rect)
            actual_screen.blit(pygame.transform.scale(ui, (actual_screen.get_width(), actual_screen.get_height())),
                               (0, 0))
            pygame.display.flip()
            clock.tick(60)

            coin_sound.set_volume(volume / 100)
            cannon_sound_l.set_volume(volume / 100)
            cannon_sound_r.set_volume(volume / 100)
            walking_sound.set_volume(volume / 100)
            place_down.set_volume(volume / 100)
            slash1_sound.set_volume(volume / 100)
            slash2_sound.set_volume(volume / 100)
            slash3_sound.set_volume(volume / 100)
            slash4_sound.set_volume(volume / 100)
            slash5r_sound.set_volume(volume / 100)
            slash5l_sound.set_volume(volume / 100)
            pygame.mixer.music.set_volume(music / 1000)
            if mute:
                coin_sound.set_volume(0)
                cannon_sound_l.set_volume(0)
                cannon_sound_r.set_volume(0)
                walking_sound.set_volume(0)
                place_down.set_volume(0)
                pygame.mixer.music.set_volume(0)
                slash1_sound.set_volume(0)
                slash2_sound.set_volume(0)
                slash3_sound.set_volume(0)
                slash4_sound.set_volume(0)
                slash5r_sound.set_volume(0)
                slash5l_sound.set_volume(0)
        ui.blit(pygame.transform.scale(tmp_bg_img, (1600, 900)), (0, 0))
        pause_menu.draw(ui)
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]


        for menu_item in menu_items:
            if menu_item.x * x_scaling < mx < menu_item.x * x_scaling + menu_item.width * x_scaling and menu_item.y * y_scaling < my < menu_item.y * y_scaling + menu_item.height * y_scaling:
                menu_item.draw(ui, 2)
            else:
                menu_item.draw(ui, 0)
        if not mouse_down:
            for menu_item in menu_items:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx = pygame.mouse.get_pos()[0]
                        my = pygame.mouse.get_pos()[1]
                        if menu_item.x * x_scaling < mx < menu_item.x * x_scaling + menu_item.width * x_scaling and menu_item.y * y_scaling < my < menu_item.y * y_scaling + menu_item.height * y_scaling:
                            if menu_item.item == "settings":
                                settings = True
                            elif menu_item.item == "quit":
                                pause = False
                                running = False
                            elif menu_item.item == "resume":
                                pause = False
        cursor_img_rect.center = (pygame.mouse.get_pos()[0] / actual_screen.get_width() * 1600,
                                  pygame.mouse.get_pos()[1] / actual_screen.get_height() * 900)
        ui.blit(pygame.transform.scale(cursor_img, (int(30 * x_scaling), int(36 * y_scaling))),
                    cursor_img_rect)
        actual_screen.blit(pygame.transform.scale(ui, (actual_screen.get_width(), actual_screen.get_height())), (0, 0))
        pygame.display.flip()
        clock.tick(60)

    if start and pygame.time.get_ticks() > last_spawn:
        enemy_spawn = waves.readline().strip().split(",")
        if len(enemy_spawn) == 3:
            enemies.append(e.Enemy(int(enemy_spawn[0]), int(enemy_spawn[1]), 64, 128, int(enemy_spawn[2])))
        if len(enemy_spawn) > 0:
            if enemy_spawn[0] == '':
                last_spawn = pygame.time.get_ticks() + 5000
                print("pause")
            elif enemy_spawn[0] == 'w':
                print("waiting for user to start new wave")
                start = False

    if pygame.time.get_ticks() - ticks > 100:
        ticks = pygame.time.get_ticks()
        frame += 1
        if frame == 8:
            frame = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_pos(int(actual_screen.get_width() / 2), int(actual_screen.get_height() / 2))
                pause = True
            if event.key == pygame.K_z:
                screen_width_z += (screen_width_z / screen_height_z) * 90
                screen_height_z += (screen_height_z / screen_width_z) * 160
                screen = pygame.transform.scale(screen, (int(screen_width_z), int(screen_height_z)))
                player.x = (screen.get_width() / 2 - 64)
                player.y = (screen.get_height() / 2 - 128)
                player.x_offset += (screen_width_z / screen_height_z) * 90/2
                player.y_offset += (screen_height_z / screen_width_z) * 160/2
            if event.key == pygame.K_u:
                screen_width_z -= (screen_width_z / screen_height_z) * 9
                screen_height_z -= (screen_height_z / screen_width_z) * 16
                screen = pygame.transform.scale(screen, (int(screen_width_z), int(screen_height_z)))
                player.x = (screen.get_width() / 2 - 64)
                player.y = (screen.get_height() / 2 - 128)
                player.x_offset -= (screen_width_z / screen_height_z) * 9 / 2
                player.y_offset -= (screen_height_z / screen_width_z) * 16 / 2
            if event.key == pygame.K_g:
                player.gold += 50
            if event.key == pygame.K_h:
                tutorial_state += 1
            if event.key == pygame.K_j:
                player.hp = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                selected_item = 0

            if event.button == 1:
                mx = pygame.mouse.get_pos()[0]
                my = pygame.mouse.get_pos()[1]

                spawn = True
                paint_red = False
                for shop_item in shop_items:
                    if shop_item.x * x_scaling < mx < shop_item.x * x_scaling + shop_item.width * x_scaling and shop_item.y * y_scaling < my < shop_item.y * y_scaling + shop_item.height * y_scaling:
                        cost = shop_item.item.cost
                        if isinstance(shop_item.item, h.Zoom):
                            cost = shop_item.item.cost * (zoom_level + 1)
                        if tutorial:
                            cost = 0
                        if player.gold >= cost:
                            if isinstance(shop_item.item, h.Heal):
                                player.hp += 25
                                player.gold -= cost
                                if player.hp > player.max_hp:
                                    player.hp = player.max_hp
                            elif isinstance(shop_item.item, h.Zoom):
                                if zoom_level < 5:
                                    player.gold -= cost
                                    screen_width_z += ((screen_width_z / screen_height_z) * 9) * 10
                                    screen_height_z += ((screen_height_z / screen_width_z) * 16) * 10
                                    screen = pygame.transform.scale(screen, (int(screen_width_z), int(screen_height_z)))
                                    player.x = (screen.get_width() / 2 - 64)
                                    player.y = (screen.get_height() / 2 - 128)
                                    player.x_offset += ((screen_width_z / screen_height_z) * 9 / 2) * 10
                                    player.y_offset += ((screen_height_z / screen_width_z) * 16 / 2) * 10
                                    zoom_level += 1
                            else:
                                selected_item = shop_item
                                spawn = False

                mx = (mx / actual_screen.get_width()) * 1600
                my = (my / actual_screen.get_height()) * 900
                x_mul = screen_width_z / 1600
                y_mul = screen_height_z / 900

                trees_and_bushes = bushes + trees
                #print(screen.get_width(), actual_screen.get_width(), screen_width_z)
                for bush in trees_and_bushes:
                    if selected_item != 0:
                        if isinstance(selected_item.item, c.Cannon) and abs((mx * x_mul - player.x_offset - 32) - bush.x) < 50 and abs((my * y_mul - player.y_offset - 32) - bush.y) < 50:
                            spawn = False
                            paint_red = True
                        if isinstance(selected_item.item, ba.Barrier) and abs((mx * x_mul - player.x_offset - 16) - bush.x) < 75 and abs((my * y_mul - player.y_offset - 32) - bush.y) < 50:
                            spawn = False
                            paint_red = True
                if selected_item != 0:
                    if isinstance(selected_item.item, c.Cannon) and abs((mx * x_mul - player.x_offset - 32) - (castle.x + 225)) < 275 and abs((my * y_mul - player.y_offset - 32) - castle.y - 100) < 200:
                        spawn = False
                        paint_red = True
                    if isinstance(selected_item.item, ba.Barrier) and abs((mx * x_mul - player.x_offset - 16) - (castle.x + 225)) < 300 and abs((my * y_mul - player.y_offset - 32) - castle.y - 100) < 200:
                        spawn = False
                        paint_red = True

                if selected_item != 0 and isinstance(selected_item.item, c.Cannon):
                    if abs(mx * x_mul - (screen_width / 2 - 32)) < 50 and abs((my * y_mul - (screen_height / 2 - 32))) < 50:
                        spawn = False
                        paint_red = True
                else:
                    if abs(mx * x_mul - (screen_width / 2 - 48)) < 75 and abs((my * y_mul - (screen_height / 2 - 32))) < 50:
                        spawn = False
                        paint_red = True

                if spawn and selected_item != 0:
                    spawn2 = True
                    if isinstance(selected_item.item, c.Cannon):
                        if len(cannons) == 0:
                            if len(barriers) == 0:
                                cannons.append(c.Cannon((mx / 1600) * screen_width_z - player.x_offset - 32, (my / 900) * screen_height_z - player.y_offset - 32, pygame.time.get_ticks()))
                                if not tutorial:
                                    player.gold -= selected_item.item.cost
                                selected_item.alpha = 0
                                selected_item = 0
                            else:
                                for barrier in barriers:
                                    if abs((mx * x_mul - player.x_offset - 32) - (barrier.x + 16)) < 75 and abs((my * y_mul - player.y_offset - 32) - barrier.y) < 50:
                                        spawn2 = False
                                if spawn2:
                                    cannons.append(c.Cannon((mx / 1600) * screen_width_z - player.x_offset - 32, (my / 900) * screen_height_z - player.y_offset - 32, pygame.time.get_ticks()))
                                    if not tutorial:
                                        player.gold -= selected_item.item.cost
                                    selected_item.alpha = 0
                                    selected_item = 0
                        else:
                            for cannon in cannons:
                                if distance(mx * x_mul - player.x_offset - 32, my * y_mul - player.y_offset - 32, cannon.x, cannon.y) < 50:
                                    spawn2 = False
                            for barrier in barriers:
                                if abs((mx * x_mul - player.x_offset - 32) - (barrier.x + 16)) < 75 and abs((my * y_mul - player.y_offset - 32) - barrier.y) < 50:
                                    spawn2 = False
                            if spawn2:
                                cannons.append(c.Cannon((mx / 1600) * screen_width_z - player.x_offset - 32, (my / 900) * screen_height_z - player.y_offset - 32, pygame.time.get_ticks()))
                                if not tutorial:
                                    player.gold -= selected_item.item.cost
                                selected_item.alpha = 0
                                selected_item = 0
                        if not spawn2:
                            paint_red = True

                    elif isinstance(selected_item.item, ba.Barrier):
                        if len(barriers) == 0:
                            if len(cannons) == 0:
                                barriers.append(ba.Barrier((mx / 1600) * screen_width_z - player.x_offset - 32, (my / 900) * screen_height_z - player.y_offset - 32, stage))
                                if not tutorial:
                                    player.gold -= selected_item.item.cost
                                selected_item.alpha = 0
                                selected_item = 0
                            else:
                                for cannon in cannons:
                                    if abs((mx * x_mul - player.x_offset - 32) - (cannon.x - 20)) < 80 and abs((my * y_mul - player.y_offset - 32) - cannon.y) < 50:
                                        spawn2 = False
                                if spawn2:
                                    barriers.append(ba.Barrier((mx / 1600) * screen_width_z - player.x_offset - 32, (my / 900) * screen_height_z - player.y_offset - 32, stage))
                                    if not tutorial:
                                        player.gold -= selected_item.item.cost
                                    selected_item.alpha = 0
                                    selected_item = 0
                        else:
                            for barrier in barriers:
                                if abs((mx * x_mul - player.x_offset - 32) - barrier.x) < 100 and abs((my * y_mul - player.y_offset - 32) - barrier.y) < 50:
                                    spawn2 = False
                            for cannon in cannons:
                                if abs((mx * x_mul - player.x_offset - 32) - (cannon.x - 20)) < 80 and abs((my * y_mul - player.y_offset - 32) - cannon.y) < 50:
                                    spawn2 = False
                            if spawn2:
                                barriers.append(ba.Barrier((mx / 1600) * screen_width_z - player.x_offset - 32, (my / 900) * screen_height_z - player.y_offset - 32, stage))
                                if not tutorial:
                                    player.gold -= selected_item.item.cost
                                selected_item.alpha = 0
                                selected_item = 0
                        if not spawn2:
                            paint_red = True

                    if spawn2:
                        pygame.mixer.Sound.play(place_down)
                if paint_red and selected_item != 0:
                    selected_item.alpha = 255

        voice = pygame.mixer.Channel(5)
        if(player.check_keys(event, enemies)):
            if not voice.get_busy():
                voice.play(walking_sound)
        else:
            voice.fadeout(250)

    #player.move([bushes, cannons, [castle]])
    player.move([bushes, trees, cannons, barriers, [castle]])

    if stage == 0:
        screen.fill((100, 150, 50))
    elif stage == 1:
        screen.fill((220, 170, 120))
    elif stage == 2:
        screen.fill((200, 230, 250))
    elif stage == 3:
        screen.fill((90, 40, 20))


    #screen.blit(start_bg, (0, 0))
    player_with_offset.x = player.x - player.x_offset
    player_with_offset.y = player.y - player.y_offset

    objects_to_draw = []
    objects_to_draw_first = []


    #castle.draw(screen, player.x_offset, player.y_offset)
    objects_to_draw.append(castle)
    #player.draw_shadow(screen, frame)

    for tree in trees:
        #bush.draw(screen, player.x_offset, player.y_offset)
        objects_to_draw.append(tree)

    for bush in bushes:
        #bush.draw(screen, player.x_offset, player.y_offset)
        if bush.offset == 20:
            objects_to_draw_first.append(bush)
        else:
            objects_to_draw.append(bush)

    for cannon in cannons:
        cannon.shoot(enemies, pygame.time.get_ticks(), player_with_offset)
        cannon.move_canonballs(screen, player.x_offset, player.y_offset, enemies)
        #cannon.draw(screen, enemies, player.x_offset, player.y_offset)
        if cannon.hp <= 0:
            cannons.remove(cannon)
            del cannon
        else:
            objects_to_draw.append(cannon)


    for enemy in enemies:
        enemy.move([[castle], [player_with_offset], cannons, barriers], [bushes, trees, enemies, cannons, [player_with_offset], [castle], barriers], player, player.x_offset, player.y_offset, arrows, frame)
        #enemy.draw(screen, frame, [bushes, enemies, cannons, [player_with_offset], [castle]], player.x_offset, player.y_offset, player)
        if enemy.hp <= 0:
            coins_to_spawn = randint(1, 2)
            for i in range(coins_to_spawn):
                coins.append(co.Coin(enemy.x + randint(0, 20), enemy.y + randint(90, 110), coin_img))
            enemies.remove(enemy)
            del enemy
        else:
            objects_to_draw.append(enemy)


    for coin in coins:
        if coin.picked_up(player_with_offset.x, player_with_offset.y):
            coins.remove(coin)
            del coin
            player.gold += randint(5, 10)
            pygame.mixer.Sound.play(coin_sound)
        else:
            objects_to_draw.append(coin)

    for barrier in barriers:
        if barrier.hp <= 0:
            barriers.remove(barrier)
            del barrier
        else:
            objects_to_draw.append(barrier)

    if player.hp <= 0 or castle.hp <= 0:
        screen_width_z = 1600
        screen_height_z = 900
        screen = pygame.transform.scale(screen, (int(screen_width_z), int(screen_height_z)))
        player.x = (screen.get_width() / 2 - 64)
        player.y = (screen.get_height() / 2 - 128)
        zoom_level = 0

        player.gold = 400
        player.hp = player.max_hp
        castle.hp = castle.max_hp
        cannons = []
        barriers = []
        enemies = []
        coins = []
        waves = open("waves.txt", "r")
        player.x_offset = 470
        player.y_offset = -75
        player.movement = [0, 0, 0, 0]
        start = False
        sc = False
        game_over = True
        while game_over:
            if not sc:
                screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
                image = Image.fromarray(np.uint8(screenshot))
                blurred = image.filter(ImageFilter.GaussianBlur(5))
                blurred_arr = np.array(blurred, dtype=np.uint8)
                tmp_bg_img = pygame.surfarray.make_surface(blurred_arr)
                sc = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = False

            ui.blit(tmp_bg_img, (0, 0))
            if player.score >= 999999:
                scr = "999999..."
            else:
                scr = player.score

            score_text = font3.render("Wave: " + str(scr), True, (40, 40, 40))
            ui.blit(score_text,(802 - int(score_text.get_width() / 2), 527))

            score_text = font3.render("Wave: " + str(scr), True, (252, 160, 3))
            ui.blit(score_text,(800 - int(score_text.get_width() / 2), 525))

            ui.blit(game_over_img, (800 - int(game_over_img.get_width() / 2), 450 - int(game_over_img.get_height() / 2)))
            cursor_img_rect.center = (pygame.mouse.get_pos()[0] / actual_screen.get_width() * 1600,
                                      pygame.mouse.get_pos()[1] / actual_screen.get_height() * 900)
            ui.blit(pygame.transform.scale(cursor_img, (int(30 * x_scaling), int(36 * y_scaling))),
                        cursor_img_rect)
            actual_screen.blit(
                pygame.transform.scale(ui, (actual_screen.get_width(), actual_screen.get_height())),
                (0, 0))
            pygame.display.flip()
            clock.tick(60)
        player.score = 0


    #player.draw(screen, frame, [bushes, cannons, [castle]])
    #print(player.x - player.x_offset, player.y - player.y_offset)

    objects_to_draw.append(player_with_offset)

    objects_to_draw.sort()

    for object in objects_to_draw_first:
        if isinstance(object, b.Bush):
            object.draw(screen, player.x_offset, player.y_offset, stage)

    for object in objects_to_draw:
        if isinstance(object, p.tmp_player):
            player.draw(screen, frame, start)
            player.draw_shadow(screen, frame)
        elif 0 < object.x + object.img.get_width() + player.x_offset and object.x + player.x_offset - object.img.get_width() < screen_width_z and \
            0 < object.y + object.img.get_height() * 2 + player.y_offset and object.y + player.y_offset - object.img.get_height() < screen_height_z:
            if isinstance(object, b.Bush):
                object.draw(screen, player.x_offset, player.y_offset, stage)
            elif isinstance(object, t.Tree):
                object.draw(screen, player.x_offset, player.y_offset)
            elif isinstance(object, c.Cannon):
                object.draw(screen, player.x_offset, player.y_offset, start)
            elif isinstance(object, e.Enemy):
                object.draw(screen, frame, player.x_offset, player.y_offset)
                object.draw_shadow(screen, frame, player.x_offset, player.y_offset)
            elif isinstance(object, cst.Castle):
                object.draw(screen, player.x_offset, player.y_offset, start)
            elif isinstance(object, co.Coin):
                object.draw(screen, frame, player.x_offset, player.y_offset)
            elif isinstance(object, ba.Barrier):
                object.draw(screen, player.x_offset, player.y_offset, start)


    draw_ui()

    cursor_img_rect.center = (pygame.mouse.get_pos()[0] / actual_screen.get_width() * 1600, pygame.mouse.get_pos()[1] / actual_screen.get_height() * 900)
    ui.blit(pygame.transform.scale(cursor_img, (int(30 * x_scaling), int(36 * y_scaling))),
                cursor_img_rect)

    actual_screen.blit(pygame.transform.scale(screen, (actual_screen.get_width(), actual_screen.get_height())), (0, 0))
    actual_screen.blit(pygame.transform.scale(ui, (actual_screen.get_width(), actual_screen.get_height())), (0, 0))
    pygame.display.flip()
    clock.tick(60)

    ui.fill((0, 0, 0, 0))

file = open("config/config.txt", "w")
file.write("volume:" + str(int(volume)) + "\nmusic:" + str(int(music)) + "\nmute_all:" + str(mute)+ "\ntutorial:" + str(tutorial))
pygame.quit()
