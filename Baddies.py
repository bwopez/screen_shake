import pygame


class Baddies(pygame.sprite.Sprite):
    def __init__(self, baddie_image, x=0, y=0):
        super().__init__()