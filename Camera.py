import pygame, random
vec = pygame.math.Vector2
from abc import ABC, abstractmethod


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        # self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.DISPLAY_W, self.DISPLAY_H = 400, 300
        # self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.player.ground_y + 20)
        self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.DISPLAY_H / 2 + player.rect.h + 2)

        self.screen_shake = 0
        self.screen_shake_max = 20
        self.screen_shake_max_half = self.screen_shake_max / 2
        self.screen_zoom = 0

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

    def shake_and_zoom_work(self):
        if self.screen_shake:
            self.offset_float.x += random.randint(0, self.screen_shake_max) - self.screen_shake_max_half
            self.offset_float.y += random.randint(0, self.screen_shake_max) - self.screen_shake_max_half
        
        if self.screen_shake > 0: # this is so that it doesn't last forever
            self.screen_shake -= 1
        if self.screen_zoom > 0:
            self.screen_zoom -= 1

    def zoom_and_blit(self, scale_multiplier, canvas, win):
        total_zoom = self.screen_zoom * scale_multiplier
        half_width = int(canvas.get_width() / 2)
        half_height = int(canvas.get_height() / 2)

        new_canvas = pygame.transform.scale(canvas, (canvas.get_width() + total_zoom, canvas.get_height() + total_zoom))
        win.blit(new_canvas, (int(0 - (total_zoom / 2)), int(0 - (total_zoom / 2))))


class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x) / 8 # this is to make the camera lag a little
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y) / 8 # this is to make the camera lag a little
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.player.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)


class Auto(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset.x += 1