import pygame
import random
from constants import *
import math

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
        # Initialize position variables
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.original_x = None
        self.original_y = None
        self.type = amino_type
        self.spawn_time = pygame.time.get_ticks()
        self.wobble_timer = 0
        self.wobble_angle = random.uniform(0, 2 * math.pi)

    def set_position(self, center):
        """Set the initial position and store it as the original position."""
        self.rect.center = center
        self.pos_x = self.rect.x  # Use rect.x as the starting point after centering
        self.pos_y = self.rect.y
        self.original_x = self.pos_x
        self.original_y = self.pos_y

    def update(self):
        """Update position to wobble around the original position."""
        if self.original_x is None or self.original_y is None:
            return  # Skip update if position hasn't been set
        self.wobble_timer += 1
        wobble_offset = 1.25 * math.sin(self.wobble_timer * 0.5)
        offset_x = wobble_offset * math.cos(self.wobble_angle)
        offset_y = wobble_offset * math.sin(self.wobble_angle)
        # Set position as original position plus current offset
        self.pos_x = self.original_x + offset_x
        self.pos_y = self.original_y + offset_y
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        if pygame.time.get_ticks() - self.spawn_time > 10000:
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
            self.rect.bottom = 80
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)
        elif self.start_edge == 'bottom':
            self.rect.top = SCREEN_HEIGHT-80
            self.rect.left = random.randint(0, SCREEN_WIDTH - self.rect.width)
        elif self.start_edge == 'left':
            self.rect.right = 0
            self.rect.top = random.randint(0, SCREEN_HEIGHT-80 - self.rect.height)
        else:  # right
            self.rect.left = SCREEN_WIDTH
            self.rect.top = random.randint(0, SCREEN_HEIGHT-80 - self.rect.height)
        
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
            self.rect.bottom < 80 or self.rect.top > SCREEN_HEIGHT):
            self.kill()