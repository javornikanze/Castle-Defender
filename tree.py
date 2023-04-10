import pygame
from asset_loader import *

class Tree:
    x = 0
    y = 0
    width = 55
    height = 60

    draw_width = 64 * 3
    draw_height = 91 * 3

    draw_offset_x = -75
    draw_offset_y = -215

    def __lt__(self, other):
        return self.y + self.height / 2 < other.y + other.height / 2

    def __init__(self, x, y, mirror, stage):
        self.x = x
        self.y = y
        if mirror:
            if stage == 0:
                self.img = tree_img_flipped
                self.shadow = tree_shadow_flipped
            elif stage == 1:
                self.img = tree_img_palm_flipped
                self.shadow = tree_shadow_flipped2
            elif stage == 2:
                self.img = tree_img_blue_flipped
                self.shadow = tree_shadow_flipped
            elif stage == 3:
                self.img = tree_img_red_flipped
                self.shadow = tree_shadow_flipped3
        else:
            if stage == 0:
                self.img = tree_img
                self.shadow = tree_shadow
            elif stage == 1:
                self.img = tree_img_palm
                self.shadow = tree_shadow2
            elif stage == 2:
                self.img = tree_img_blue
                self.shadow = tree_shadow
            elif stage == 3:
                self.img = tree_img_red
                self.shadow = tree_shadow3


    def draw(self, screen, x_offset, y_offset):
        screen.blit(self.shadow, (self.x + x_offset + self.draw_offset_x, self.y + self.draw_height * 0.7 + y_offset - 138))
        screen.blit(self.img, (self.x + x_offset + self.draw_offset_x, self.y + y_offset + self.draw_offset_y))



