import pygame
import sys
from sprites import Ribosome, AminoAcid, Obstacle
from protein_sequence import ProteinSequence
from constants import *
from assets import load_images, load_sounds
import random

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ribosome Rush")
        self.gameplay_rect = pygame.Rect(0, 80, SCREEN_WIDTH, SCREEN_HEIGHT - 80)
        self.clock = pygame.time.Clock()
        self.images = load_images()
        self.sounds = load_sounds()
        self.setup_game()

    def setup_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.ribosome = Ribosome(self.images['ribosome'])
        self.all_sprites.add(self.ribosome)
        self.amino_acids = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.protein_sequence = ProteinSequence(self.images)
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.game_active = True

    def run(self):
        # pygame.mixer.music.play(-1)  # Loop background music
        while True:
            self.handle_events()
            if self.game_active:
                self.update()
                self.draw()
            else:
                self.show_game_over_screen()
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.ribosome.move(dx, dy)

        self.ribosome.rect.clamp_ip(self.gameplay_rect)

        self.spawn_game_objects()
        self.all_sprites.update()
        self.amino_acids.update()
        self.obstacles.update()

        self.handle_collisions()
        self.check_game_over()

    def spawn_game_objects(self):
        if random.randint(1, 60) == 1:
            new_amino_acid = AminoAcid(random.choice(ALL_AMINO_ACIDS), self.images)
            new_amino_acid.rect.center = (
                random.randint(self.gameplay_rect.left, self.gameplay_rect.right),
                random.randint(self.gameplay_rect.top, self.gameplay_rect.bottom)
            )
            self.amino_acids.add(new_amino_acid)

        if random.randint(1, 120) == 1:
            new_obstacle = Obstacle(self.images['obstacle'])
            self.obstacles.add(new_obstacle)

    def handle_collisions(self):
        collected = pygame.sprite.spritecollide(self.ribosome, self.amino_acids, True)
        for amino in collected:
            self.protein_sequence.add_collected(amino.type)
            self.protein_sequence.next_amino_acid()
            # self.sounds['collect'].play()

        if pygame.sprite.spritecollide(self.ribosome, self.obstacles, False):
            self.ribosome.speed = 2  # Slow down ribosome
            # self.sounds['collision'].play()
        else:
            self.ribosome.speed = 5  # Normal speed

    def check_game_over(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        if elapsed_time >= ALLOWED_TIME or self.protein_sequence.current_amino_acid() is None:
            self.game_active = False

    def draw(self):
        self.screen.blit(self.images['background'], (0, 0))
        # Create and draw the white overlay
        white_overlay = pygame.Surface((SCREEN_WIDTH, 80))
        white_overlay.fill(WHITE)
        self.screen.blit(white_overlay, (0, 0))
        self.all_sprites.draw(self.screen)
        self.amino_acids.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.protein_sequence.draw(self.screen)
        self.draw_ui()

    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = font.render(f"Time: {ALLOWED_TIME - elapsed_time}", True, BLACK)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    def draw_game_over(self):
        self.draw()  # Draw the game state in the background
        font = pygame.font.Font(None, 36)
        final_score = self.protein_sequence.calculate_alignment_score()
        max_possible_score = len(self.protein_sequence.sequence) * 10
        score_percentage = (final_score / max_possible_score) * 100
        if score_percentage >= 80:
            end_text = font.render(f"You Win! Score: {final_score}/{max_possible_score}", True, GREEN)
        else:
            end_text = font.render(f"Game Over. Score: {final_score}/{max_possible_score}", True, RED)
        self.screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    def show_game_over_screen(self):
        self.draw()  # Draw the game state in the background
        font = pygame.font.Font(None, 36)
        final_score = self.protein_sequence.calculate_alignment_score()
        max_possible_score = len(self.protein_sequence.sequence) * 10
        score_percentage = (final_score / max_possible_score) * 100
        if score_percentage >= 80:
            end_text = font.render(f"You Win! Score: {final_score}/{max_possible_score}", True, GREEN)
        else:
            end_text = font.render(f"Game Over. Score: {final_score}/{max_possible_score}", True, RED)
        self.screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        play_again_button = self.create_play_again_button()
        pygame.draw.rect(self.screen, WHITE, play_again_button)
        play_again_text = font.render("Play Again", True, BLACK)
        text_rect = play_again_text.get_rect(center=play_again_button.center)
        self.screen.blit(play_again_text, text_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        self.reset_game()
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        waiting = False

    
    def create_play_again_button(self):
        button_width, button_height = 200, 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = SCREEN_HEIGHT * 3 // 4
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        return button_rect
    
    def reset_game(self):
        # Remove all sprites
        for sprite in self.all_sprites:
            sprite.kill()
        
        # Clear sprite groups
        self.amino_acids.empty()
        self.obstacles.empty()
        
        # Reset game state
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        
        # Use setup_game to reinitialize the game
        self.setup_game()

