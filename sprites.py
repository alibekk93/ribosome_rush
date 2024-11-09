import pygame
import random
from constants import *

class Ribosome(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

class AminoAcid(pygame.sprite.Sprite):
    def __init__(self, amino_type, images):
        super().__init__()
        self.image = images[amino_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.type = amino_type
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 10000:  # 10 seconds
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        
        # Randomly choose a starting edge
        self.start_edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        # Set initial position based on the starting edge
        if self.start_edge == 'top':
            self.rect.bottom = 0
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)
        elif self.start_edge == 'bottom':
            self.rect.top = SCREEN_HEIGHT
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)
        elif self.start_edge == 'left':
            self.rect.right = 0
            self.rect.top = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        else:  # right
            self.rect.left = SCREEN_WIDTH
            self.rect.top = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        
        # Calculate direction to move across the screen
        target_x = random.randint(0, SCREEN_WIDTH)
        target_y = random.randint(0, SCREEN_HEIGHT)
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        self.speed = random.uniform(1, 3)
        self.dx = dx / distance * self.speed
        self.dy = dy / distance * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Check if the obstacle has moved off the screen
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()