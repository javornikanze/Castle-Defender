import pygame
import cannon
import barrier
import heal
from asset_loader import *


class ShopItem:
    x = 0
    y = 0
    width = 128
    height = 128

    img = shop_icon_img

    def __init__(self, x, y, item):
        self.x = x
        self.y = y
        self.item_img = item.img
        self.item = item
        self.alpha = 0
        self.font = font
        if not isinstance(item, barrier.Barrier):
            self.surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            self.surface.blit(self.item_img, (0, 0))
            self.colouredImage = pygame.Surface(self.surface.get_size())
            self.colouredImage.fill((255, 0, 0, 0))
        else:
            self.surface = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
            self.surface.blit(self.item_img, (0, 0))
            self.colouredImage = pygame.Surface(self.surface.get_size())
            self.colouredImage.fill((255, 0, 0, 0))



    def draw(self, screen, size, zoom_level, player_gold):
        screen.blit(pygame.transform.scale(self.img, (self.width - size, self.height - size)), (self.x + (size / 2), self.y + (size / 2)))

        if isinstance(self.item, cannon.Cannon):
            screen.blit(pygame.transform.scale(self.surface, (self.width - 32 - size, self.height - 32 - size)), (self.x + 16 + (size / 2), self.y + 16 + (size / 2)))
        else:
            screen.blit(pygame.transform.scale(self.surface, (self.width - 32 - size, self.height - 32 - size)), (self.x + 16 + (size / 2), self.y + 32 + (size / 2)))

        if isinstance(self.item, heal.Zoom):
            if zoom_level < 5:
                s = str(self.item.cost * (zoom_level + 1))
                if self.item.cost * (zoom_level + 1) <= player_gold:
                    color = (252, 198, 3)
                else:
                    color = (200, 50, 50)
            else:
                s = "Max."
                color = (200, 50, 50)
        else:
            s = str(self.item.cost)
            if self.item.cost <= player_gold:
                color = (252, 198, 3)
            else:
                color = (200, 50, 50)

        gold_text = self.font.render(s, False, (0, 0, 0))
        screen.blit(
            pygame.transform.scale(gold_text, (int(gold_text.get_width() * 1.5), int(gold_text.get_height() * 1.2))),
            (self.x + 22 + size/2, self.y + 7 + size/2))



        gold_text = self.font.render(s, False, color)
        screen.blit(
            pygame.transform.scale(gold_text, (int(gold_text.get_width() * 1.5), int(gold_text.get_height() * 1.2))),
            (self.x + 20 + size/2, self.y + 5 + size/2))

    def draw_on_mouse(self, screen, mx, my, x_scaling, y_scaling, screen_width_z, screen_height_z):
        if isinstance(self.item, cannon.Cannon):
            screen.blit(pygame.transform.scale(self.surface, (int((self.width - 64) * (1600 / screen_width_z)), int((self.height - 64) * (900 / screen_height_z)))), (mx, my))
            image = self.surface.copy()
            image.fill((255, 0, 0, self.alpha), None, pygame.BLEND_RGBA_MULT)
            screen.blit(pygame.transform.scale(image, (int((self.width - 64) * (1600 / screen_width_z)), int((self.height - 64) * (900 / screen_height_z)))), (mx, my))
        else:
            screen.blit(pygame.transform.scale(self.surface, (int((self.width - 32) * (1600 / screen_width_z)), int((self.height - 32) * (900 / screen_height_z)))), (mx, my))
            image = self.surface.copy()
            image.fill((255, 0, 0, self.alpha), None, pygame.BLEND_RGBA_MULT)
            screen.blit(pygame.transform.scale(image, (int((self.width - 32) * (1600 / screen_width_z)), int((self.height - 32) * (900 / screen_height_z)))), (mx, my))

        if self.alpha > 0:
            self.alpha -= (1 / self.alpha) * 750

        if self.alpha < 0:
            self.alpha = 0


