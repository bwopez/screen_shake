import pygame
from pygame.locals import *

from PIL import Image, ImageFilter


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image,  x=0, y=0):
        super().__init__()
        # used for images that have transparency 
        self.image = pygame.image.load(player_image).convert_alpha()
        # use this copy for scaling
        self.image_copy = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

        self.move_speed = 5

    def reset_rect(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def scale(self, up_or_down):
        scaler = 20
        if up_or_down == 1:
            scaled = pygame.transform.scale(self.image_copy, (self.image.get_width() + scaler, self.image.get_height() + scaler))
            self.image = scaled
            self.reset_rect(self.rect.x - int(scaler/2), self.rect.y - int(scaler/2))
        elif up_or_down == -1:
            # if the image is wider than it's original width
            if self.image.get_width() > self.image_copy.get_width():
                scaled = pygame.transform.scale(self.image_copy, (self.image.get_width() - scaler, self.image.get_height() - scaler))
                self.image = scaled
                self.reset_rect(self.rect.x + int(scaler/2), self.rect.y + int(scaler/2))
        else:
            self.reset_rect(self.rect.x, self.rect.y)
    
    def blur(self):
        # TODO: this can probably be cleaned up
        image_string = pygame.image.tostring(self.image, "RGBA", False)
        image_bytes = Image.frombytes("RGBA", (self.image.get_width(), self.image.get_height()), image_string)
        blurred = image_bytes.filter(ImageFilter.BLUR)
        blurred_image = pygame.image.fromstring(blurred.tobytes(), blurred.size, blurred.mode).convert_alpha()
        self.image = blurred_image
        self.scale(0)

    def unblur(self):
        # TODO: this can probably be cleaned up
        scaled = pygame.transform.scale(self.image_copy, (self.image.get_width(), self.image.get_height()))
        self.image = scaled
        self.scale(0)

    def draw(self, canvas, camera):
        # use this one if you want jiggle physics on your player movement   
        # self.rect.x -= camera.offset.x 
        # self.rect.y -= camera.offset.y 
        # canvas.blit(self.image, (self.rect.x, self.rect.y))
        canvas.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))

    # TODO: maybe name this move_input() or something
    def update(self, keys):
        # this controls the movement of the character
        if (keys[K_a] or keys[K_LEFT]) and (keys[K_d] or keys[K_RIGHT]):
            # stopping holding down left and right
            pass
        else:
            if keys[K_a] or keys[K_LEFT]:
                # self.move(win, "left")
                self.move("left")
            if keys[K_d] or keys[K_RIGHT]:
                # self.move(win, "right")
                self.move("right")
        if (keys[K_w] or keys[K_UP]) and (keys[K_s] or keys[K_DOWN]):
            # stopping holding down up and down
            pass
        else:
            if keys[K_w] or keys[K_UP]:
                # self.move(win, "up")
                self.move("up")
            if keys[K_s] or keys[K_DOWN]:
                # self.move(win, "down")
                self.move("down")

    # def move(self, win, direction):
    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.move_speed
        if direction == "right":
            self.rect.x += self.move_speed
        if direction == "up":
            self.rect.y -= self.move_speed
        if direction == "down":
            self.rect.y += self.move_speed