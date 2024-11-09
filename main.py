import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ALLOWED_TIME = 180

# Amino Acid Groups
AMINO_ACIDS = {
    'Nonpolar': ['A', 'V', 'L', 'I', 'M', 'F', 'W', 'P'],
    'Uncharged': ['G', 'S', 'T', 'C', 'Y', 'N', 'Q'],
    'Positive': ['K', 'R', 'H'],
    'Negative': ['D', 'E']
}

ALL_AMINO_ACIDS = [aa for group in AMINO_ACIDS.values() for aa in group]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ribosome Rush")

# Load and resize images
def load_image(name, size=None):
    path = os.path.join("images", name)
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

background_img = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
ribosome_img = load_image("ribosome.png", (50, 50))
obstacle_img = load_image("debris.png", (40, 40))

# Load amino acid images
amino_acid_images = {aa: load_image(f"{aa}.png", (30, 30)) for aa in ALL_AMINO_ACIDS}

# Sounds (placeholder - replace with actual sounds)
# collect_sound = pygame.mixer.Sound("collect.wav")
# collision_sound = pygame.mixer.Sound("collision.wav")
# pygame.mixer.music.load("background_music.mp3")

class Ribosome(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ribosome_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

class AminoAcid(pygame.sprite.Sprite):
    def __init__(self, amino_type):
        super().__init__()
        self.image = amino_acid_images[amino_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.type = amino_type
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 10000:  # 10 seconds
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img
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

class ProteinSequence:
    def __init__(self):
        self.sequence = [random.choice(ALL_AMINO_ACIDS) for _ in range(5)]
        self.collected_sequence = []
        self.current_index = 0

    def current_amino_acid(self):
        return self.sequence[self.current_index] if self.current_index < len(self.sequence) else None

    def next_amino_acid(self):
        self.current_index += 1

    def add_collected(self, amino_acid):
        self.collected_sequence.append(amino_acid)
    
    def calculate_alignment_score(self):
        alignment_score = 0
        for i in range(min(len(self.sequence), len(self.collected_sequence))):
            if self.sequence[i] == self.collected_sequence[i]:
                alignment_score += 10
            elif self.collected_sequence[i] in AMINO_ACIDS[self.get_amino_acid_group(self.sequence[i])]:
                alignment_score += 5  # Partial score for correct group
        return alignment_score

    def get_amino_acid_group(self, amino_acid):
        for group, aas in AMINO_ACIDS.items():
            if amino_acid in aas:
                return group
        return None

    def draw(self, surface):
        x_offset = 10
        y_offset = 10
        aa_size = 30
        spacing = 5

        # Draw target sequence
        for i, aa in enumerate(self.sequence):
            aa_image = amino_acid_images[aa]
            aa_rect = aa_image.get_rect()
            aa_rect.topleft = (x_offset + i * (aa_size + spacing), y_offset)
            surface.blit(aa_image, aa_rect)

            if i == self.current_index:
                pygame.draw.rect(surface, GREEN, aa_rect, 2)  # Highlight current AA

        # Draw collected sequence
        collected_y_offset = y_offset + aa_size + 10  # 10 pixels below the target sequence
        for i, collected_aa in enumerate(self.collected_sequence):
            aa_image = amino_acid_images[collected_aa]
            aa_rect = aa_image.get_rect()
            aa_rect.topleft = (x_offset + i * (aa_size + spacing), collected_y_offset)
            surface.blit(aa_image, aa_rect)

            if i < len(self.sequence):
                target_aa = self.sequence[i]
                if collected_aa != target_aa:
                    if self.get_amino_acid_group(collected_aa) == self.get_amino_acid_group(target_aa):
                        pygame.draw.rect(surface, YELLOW, aa_rect, 2)  # Yellow outline for same group
                    else:
                        pygame.draw.rect(surface, RED, aa_rect, 2)  # Red outline for different group

# Game setup
clock = pygame.time.Clock()
ribosome = Ribosome()
all_sprites = pygame.sprite.Group(ribosome)
amino_acids = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
protein_sequence = ProteinSequence()

score = 0
start_time = pygame.time.get_ticks()
game_duration = ALLOWED_TIME * 1000  # 60 seconds
game_active = True

# Main game loop
# pygame.mixer.music.play(-1)  # Loop background music

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_active:
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        ribosome.move(dx, dy)

        # Spawn amino acids
        if random.randint(1, 60) == 1:
            amino_acids.add(AminoAcid(random.choice(ALL_AMINO_ACIDS)))

        # Spawn obstacles
        if random.randint(1, 120) == 1:
            obstacles.add(Obstacle())

        # Update
        all_sprites.update()
        amino_acids.update()
        obstacles.update()

        # Collisions
        collected = pygame.sprite.spritecollide(ribosome, amino_acids, True)
        for amino in collected:
            protein_sequence.add_collected(amino.type)
            protein_sequence.next_amino_acid()

        if pygame.sprite.spritecollide(ribosome, obstacles, False):
            ribosome.speed = 2  # Slow down ribosome
            # collision_sound.play()
        else:
            ribosome.speed = 5  # Normal speed

        # Check win/lose conditions
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        if elapsed_time >= ALLOWED_TIME or protein_sequence.current_amino_acid() is None:
            game_active = False
            final_score = protein_sequence.calculate_alignment_score()

    # Drawing
    screen.blit(background_img, (0, 0))  # Draw background
    all_sprites.draw(screen)
    amino_acids.draw(screen)
    obstacles.draw(screen)

    # Draw protein sequence using images
    protein_sequence.draw(screen)

    # Draw score and timer
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 50))
    timer_text = font.render(f"Time: {ALLOWED_TIME - elapsed_time}", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    if not game_active:
        final_score = protein_sequence.calculate_alignment_score()
        max_possible_score = len(protein_sequence.sequence) * 10
        score_percentage = (final_score / max_possible_score) * 100

        if score_percentage >= 80:
            end_text = font.render(f"You Win! Score: {final_score}/{max_possible_score}", True, GREEN)
        else:
            end_text = font.render(f"Game Over. Score: {final_score}/{max_possible_score}", True, RED)
        screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)