import time
from random import *

import pygame
import pygame_gui

pygame.init()
clock = pygame.time.Clock()

screen_width = 1600
screen_height = 900
screen_width_z = 1600
screen_height_z = 900

actual_screen = pygame.display.set_mode([screen_width, screen_height], pygame.RESIZABLE)

screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
screen = screen.convert_alpha()
ui = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
ui = ui.convert_alpha()


manager = pygame_gui.UIManager((screen_width, screen_height))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=manager,
                                               object_id='#main_text_entry')

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.init()

s1 = pygame.transform.scale(pygame.image.load('images/s1.png').convert_alpha(), (640, 360))
s2 = pygame.transform.scale(pygame.image.load('images/s2.png').convert_alpha(), (640, 360))
s3 = pygame.transform.scale(pygame.image.load('images/s3.png').convert_alpha(), (640, 360))
s4 = pygame.transform.scale(pygame.image.load('images/s4.png').convert_alpha(), (640, 360))


enemy_img = pygame.image.load('images/enemy_animated.png').convert_alpha()
attack_img = pygame.image.load('images/slash.png').convert_alpha()
arrow_img = pygame.image.load('images/arrow.png').convert_alpha()
coin_img = pygame.image.load('images/coin.png').convert_alpha()
ui_img = pygame.image.load('images/shop_icon2.png').convert_alpha()
shop_img = pygame.image.load('images/shop_icon3.png').convert_alpha()
start_img = pygame.image.load('images/start.png').convert_alpha()
start_bg = pygame.image.load('images/bg.png').convert_alpha()
cursor_img = pygame.image.load('images/cursor.png').convert_alpha()
cursor_img_rect = cursor_img.get_rect()
castle_img = pygame.transform.scale(pygame.image.load('images/castle.png').convert_alpha(), (512, 512))
castle_img_blue = pygame.transform.scale(pygame.image.load('images/castle_blue.png').convert_alpha(), (512, 512))
castle_img_red = pygame.transform.scale(pygame.image.load('images/castle_red.png').convert_alpha(), (512, 512))

slash_img = pygame.image.load('images/slash.png').convert_alpha()
player_img = pygame.image.load('images/player_animated.png').convert_alpha()

bush_img = pygame.transform.scale(pygame.image.load('images/bush.png').convert_alpha(), (64, 64))
bush_img_blue = pygame.transform.scale(pygame.image.load('images/bush_blue.png').convert_alpha(), (64, 64))
bush_img_red = pygame.transform.scale(pygame.image.load('images/bush_red.png').convert_alpha(), (64, 64))
bush_img_yellow = pygame.transform.scale(pygame.image.load('images/bush_yellow.png').convert_alpha(), (64, 64))

menu_img = pygame.image.load('images/pause_menu.png').convert_alpha()
return_button_img = pygame.image.load('images/return.png').convert_alpha()
shop_icon_img = pygame.image.load('images/shop_icon.png').convert_alpha()
pause_menu_img = pygame.image.load('images/pause.png').convert_alpha()
quit_img = pygame.image.load('images/quit.png').convert_alpha()
resume_img = pygame.image.load('images/resume.png').convert_alpha()
settings_img = pygame.image.load('images/settings.png').convert_alpha()
cannon_img = pygame.image.load('images/cannon.png').convert_alpha()
cannonball_img = pygame.image.load('images/cannonball.png').convert_alpha()
shot_img = pygame.image.load('images/shot.png').convert_alpha()
barrier_img = pygame.image.load('images/barrier.png').convert_alpha()
game_over_img = pygame.image.load('images/game_over.png').convert_alpha()

tree_img = pygame.transform.scale(pygame.image.load('images/tree.png').convert_alpha(), (int(64 * 3), int(91 * 3)))
tree_img_blue = pygame.transform.scale(pygame.image.load('images/tree_blue.png').convert_alpha(), (int(64 * 3), int(91 * 3)))
tree_img_red = pygame.transform.scale(pygame.image.load('images/tree_red.png').convert_alpha(), (int(64 * 3), int(91 * 3)))
tree_img_palm = pygame.transform.scale(pygame.image.load('images/tree_palm.png').convert_alpha(), (int(64 * 3), int(91 * 3)))

tree_shadow = pygame.transform.flip(tree_img.copy(), False, True)
tree_shadow.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)

tree_shadow2 = pygame.transform.flip(tree_img_palm.copy(), False, True)
tree_shadow2.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)

tree_shadow3 = pygame.transform.flip(tree_img_red.copy(), False, True)
tree_shadow3.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)


tree_img_flipped = pygame.transform.scale(pygame.transform.flip(pygame.image.load('images/tree.png'), True, False).convert_alpha(), (int(64 * 3), int(91 * 3)))
tree_img_blue_flipped = pygame.transform.scale(pygame.transform.flip(pygame.image.load('images/tree_blue.png'), True, False).convert_alpha(), (int(64 * 3), int(91 * 3)))
tree_img_red_flipped = pygame.transform.scale(pygame.transform.flip(pygame.image.load('images/tree_red.png'), True, False).convert_alpha(), (int(64 * 3), int(91 * 3)))
tree_img_palm_flipped = pygame.transform.scale(pygame.transform.flip(pygame.image.load('images/tree_palm.png'), True, False).convert_alpha(), (int(64 * 3), int(91 * 3)))

tree_shadow_flipped = pygame.transform.flip(tree_img_flipped.copy(), False, True)
tree_shadow_flipped.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)

tree_shadow_flipped2 = pygame.transform.flip(tree_img_palm_flipped.copy(), False, True)
tree_shadow_flipped2.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)

tree_shadow_flipped3 = pygame.transform.flip(tree_img_red_flipped.copy(), False, True)
tree_shadow_flipped3.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)


heal_img = pygame.image.load('images/heal.png').convert_alpha()
zoom_img = pygame.image.load('images/zoom.png').convert_alpha()

t1_img = pygame.image.load('images/t1.png').convert_alpha()
t2_img = pygame.image.load('images/t2.png').convert_alpha()
t3_img = pygame.image.load('images/t3.png').convert_alpha()
t4_img = pygame.image.load('images/t4.png').convert_alpha()
t5_img = pygame.image.load('images/t5.png').convert_alpha()

font = pygame.font.SysFont("javanesetext", 20)
font3 = pygame.font.SysFont("javanesetext", 40)
coin_sound = pygame.mixer.Sound("sounds/coin.mp3")
cannon_sound_r = pygame.mixer.Sound("sounds/cannon_l.mp3")
cannon_sound_l = pygame.mixer.Sound("sounds/cannon_r.mp3")
walking_sound = pygame.mixer.Sound("sounds/walking.mp3")
place_down = pygame.mixer.Sound("sounds/place_down.mp3")
slash1_sound = pygame.mixer.Sound("sounds/slash1.mp3")
slash2_sound = pygame.mixer.Sound("sounds/slash2.mp3")
slash3_sound = pygame.mixer.Sound("sounds/slash3.mp3")
slash4_sound = pygame.mixer.Sound("sounds/slash4.mp3")
slash5r_sound = pygame.mixer.Sound("sounds/slash5_r.mp3")
slash5l_sound = pygame.mixer.Sound("sounds/slash5_l.mp3")
pygame.mixer.music.load('sounds/music.mp3')

coin_sound.set_volume(0.5)
pygame.mixer.music.set_volume(0.1)
cannon_sound_l.set_volume(0.1)
cannon_sound_r.set_volume(0.1)
walking_sound.set_volume(0.1)
place_down.set_volume(0.1)
slash1_sound.set_volume(0.1)
slash2_sound.set_volume(0.1)
slash3_sound.set_volume(0.1)
slash4_sound.set_volume(0.1)
slash5r_sound.set_volume(0.1)
slash5l_sound.set_volume(0.1)
