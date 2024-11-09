import pygame
import os
from constants import *

def load_image(name, size=None):
    path = os.path.join("images", name)
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_images():
    # Load all game images
    images = {
        'background': load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
        'ribosome': load_image("ribosome.png", (50, 50)),
        'obstacle': load_image("debris.png", (40, 40)),
    }
    images.update({aa: load_image(f"{aa}.png", (30, 30)) for aa in ALL_AMINO_ACIDS})
    return images

def load_sounds():
    # Load all game sounds
    return {
        # 'collect': pygame.mixer.Sound("collect.wav"),
        # 'collision': pygame.mixer.Sound("collision.wav"),
        # 'background_music': "background_music.mp3"
    }