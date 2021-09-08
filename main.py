import pygame, random
from pygame.locals import *

from PIL import Image, ImageFilter

from Player import Player
from Camera import *


def main_game():
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_W, DISPLAY_H = 400, 300
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    win = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption("new_game")

    # player = Player("images/player.png", 100, 100)
    player = Player("images/new_player1.png", 100, 100)

    # TODO: Create a bad guys class and add a damage on collision 
    buildings = []
    for thing in range(0, 100):
        buildings.append(Player("images/building_windows_thing.png", random.randint(0, 1000) - 500, random.randint(0, 1000) - 500))

    camera = Camera(player)
    follow = Follow(camera, player)
    camera.setmethod(follow)

    second_char = Player("images/second_character.png", 0, 0)
    image_scaler = 15
    sound_playing = False
    sound_obj = pygame.mixer.Sound("sounds/running.mp3")

    running = True
    while running:
        camera.shake_and_zoom_work()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        if keys[K_ESCAPE]:
            running = False
        
        player.update(keys)
        # TODO: change this to a "taking damage" trigger
        if keys[K_SPACE]:
            # setting screen_shake and screen_zoom makes a screen flexing effect
            camera.screen_shake = 8
            camera.screen_zoom = 8
        if keys[K_p]:
            # do blur
            second_char.blur()
        if keys[K_u]:
            second_char.unblur()

        # scale the second player image up and down
        # b for big, l for littler
        if keys[K_b]:
            second_char.scale(1)
        if keys[K_l]:
            second_char.scale(-1)

        # Update window ===========================
        canvas.fill("White")

        camera.scroll()
        for building in buildings:
            building.draw(canvas, camera)
        player.draw(canvas, camera)
        second_char.draw(canvas, camera)

        if camera.screen_zoom:
            camera.zoom_and_blit(10, canvas, win)
        else:
            win.blit(canvas, (0, 0))
            
        clock.tick(60)
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main_game()