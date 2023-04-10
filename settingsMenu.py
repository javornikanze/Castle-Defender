import pygame
import menuItem as m
from asset_loader import *

class SettingsMenu:
    width = 256
    height = 128
    x = 0
    y = 0

    menu = menu_img
    return_button = return_button_img

    def __init__(self, screen):
        width, height = screen.get_size()
        self.width = int((width / 2.75))
        self.height = int((height / 3))
        self.x = (width / 2) - (self.width / 2)
        self.y = (height / 3) - (self.height / 2)

    def draw(self, screen, volume, music, mute, size):
        screen.blit(pygame.transform.scale(self.menu, (self.width, self.height)), (self.x, self.y))
        screen.blit(pygame.transform.scale(self.return_button, (230 + size, 64 + size)), (835 - size / 2, 370 - size / 2))

        pygame.draw.rect(screen, (255, 190, 90), pygame.Rect(self.x + 223, self.y + 106, volume * 2.45, 20))
        pygame.draw.rect(screen, (193, 143, 73), pygame.Rect(self.x + 223, self.y + 123, volume * 2.45, 3))

        pygame.draw.rect(screen, (255, 190, 90), pygame.Rect(self.x + 223, self.y + 154, music * 2.45, 20))
        pygame.draw.rect(screen, (193, 143, 73), pygame.Rect(self.x + 223, self.y + 171, music * 2.45, 3))
        if mute:
            pygame.draw.rect(screen, (175, 127, 75), pygame.Rect(736, 357, 10, 10))
        #screen.blit(pygame.transform.scale(self.img, (self.width - size, self.height - size)),
        #            (self.x + (size / 2), self.y + (size / 2)))