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

        self.move_speed = 3
        self.dash_speed = 20
        self.cooldown = 0

        self.max_dash_charges = 2
        # self.dash_charges_used = 0
        self.dash_cooldowns = []

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
    # TODO: refactor this to use helper functions
    # TODO: both dash charges are being used if two directions are being held
        # at the same time
    def update(self, keys, events):
        # this controls the movement of the character
        dash = 0
        cooldown = 40
        space_pressed = False
        
        for dash_cd in self.dash_cooldowns:
            if dash_cd > 0:
                index = self.dash_cooldowns.index(dash_cd)
                self.dash_cooldowns[index] -= 1
        
        # remove all the zeroes from self.dash_cooldowns
        try:
            while True:
                self.dash_cooldowns.remove(0)
        except ValueError:
            pass

        # check to see if space has been pressed down
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                space_pressed = True
        print(self.dash_cooldowns)

        if (keys[K_a] or keys[K_LEFT]) and (keys[K_d] or keys[K_RIGHT]):
            # stopping holding down left and right
            pass
        else:
            if keys[K_a] or keys[K_LEFT]:
                # self.move(win, "left")
                flipped = pygame.transform.flip(self.image_copy, True, False)
                self.image = pygame.transform.scale(flipped, (self.image.get_height(), self.image.get_width()))
                if space_pressed and len(self.dash_cooldowns) < self.max_dash_charges:
                    dash = self.dash_speed
                    # add a cooldown to self.dash_cooldowns
                    self.dash_cooldowns.append(cooldown)
                self.move("left", dash)
            if keys[K_d] or keys[K_RIGHT]:
                # self.move(win, "right")
                self.image = pygame.transform.scale(self.image_copy, (self.image.get_width(), self.image.get_height()))
                if space_pressed and len(self.dash_cooldowns) < self.max_dash_charges:
                    dash = self.dash_speed
                    # add a cooldown to self.dash_cooldowns
                    self.dash_cooldowns.append(cooldown)
                self.move("right", dash)
        if (keys[K_w] or keys[K_UP]) and (keys[K_s] or keys[K_DOWN]):
            # stopping holding down up and down
            pass
        else:
            if keys[K_w] or keys[K_UP]:
                # self.move(win, "up")
                if space_pressed and len(self.dash_cooldowns) < self.max_dash_charges:
                    dash = self.dash_speed
                    # add a cooldown to self.dash_cooldowns
                    self.dash_cooldowns.append(cooldown)
                self.move("up", dash)
            if keys[K_s] or keys[K_DOWN]:
                # self.move(win, "down")
                if space_pressed and len(self.dash_cooldowns) < self.max_dash_charges:
                    dash = self.dash_speed
                    # add a cooldown to self.dash_cooldowns
                    self.dash_cooldowns.append(cooldown)
                self.move("down", dash)

    # def move(self, win, direction):
    def move(self, direction, extra_speed):
        if direction == "left":
            self.rect.x -= (self.move_speed + extra_speed)
        if direction == "right":
            self.rect.x += (self.move_speed + extra_speed)
        if direction == "up":
            self.rect.y -= (self.move_speed + extra_speed)
        if direction == "down":
            self.rect.y += (self.move_speed + extra_speed)