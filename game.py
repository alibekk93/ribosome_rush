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
            center_x = random.randint(self.gameplay_rect.left, self.gameplay_rect.right)
            center_y = random.randint(self.gameplay_rect.top, self.gameplay_rect.bottom)
            new_amino_acid.set_position((center_x, center_y))
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
        if score_percentage >= 50:
            end_text = font.render(f"You Win! Score: {final_score}/{max_possible_score}", True, GREEN)
        else:
            end_text = font.render(f"Game Over. Score: {final_score}/{max_possible_score}", True, RED)
        self.screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    
    def show_game_over_screen(self):
        self.draw()  # Draw the game state behind the game over screen

        # Load fonts (use custom font if available, otherwise fallback to default)
        try:
            title_font = pygame.font.Font('path/to/font.ttf', 40)
            explanation_font = pygame.font.Font('path/to/font.ttf', 26)
        except:
            title_font = pygame.font.Font(None, 40)
            explanation_font = pygame.font.Font(None, 26)

        # Calculate score and explanation
        final_score, explanation = self.protein_sequence.calculate_alignment_score()
        max_possible_score = len(self.protein_sequence.sequence) * 10
        score_percentage = (final_score / max_possible_score) * 100

        # Render title text
        if score_percentage >= 50:
            title_text = title_font.render(f"You Win! Score: {final_score}/{max_possible_score}", True, (0, 255, 0))
        else:
            title_text = title_font.render(f"Game Over. Score: {final_score}/{max_possible_score}", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))

        # Create a semi-transparent background for the explanation
        explanation_bg = pygame.Surface((SCREEN_WIDTH - 80, 350))
        explanation_bg.set_alpha(220)
        explanation_bg.fill((240, 240, 240))
        explanation_bg_rect = explanation_bg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))

        # Create explanation text surfaces and their positions
        explanation_surfaces = []
        explanation_rects = []
        y_pos = explanation_bg_rect.top + 20
        for idx, entry in enumerate(explanation):
            text = f"Pos {idx+1}: Target: {entry['target']} | Collected: {entry['collected']} | Score: {entry['score']} | {entry['reason']}"
            text_surface = explanation_font.render(text, True, (50, 50, 50))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            explanation_surfaces.append(text_surface)
            explanation_rects.append(text_rect)
            y_pos += 35

        # Animation: Fade in each line sequentially, keeping all previous lines visible
        current_fade_index = 0
        current_alpha = 0
        while current_fade_index < len(explanation):
            # Redraw background and title
            self.screen.blit(explanation_bg, explanation_bg_rect)
            self.screen.blit(title_text, title_rect)

            # Draw all lines up to and including the current one being faded in
            for j in range(current_fade_index + 1):
                text_surface = explanation_surfaces[j]
                if j < current_fade_index:
                    # Previous lines stay fully visible
                    temp_surface = text_surface.copy()
                    temp_surface.set_alpha(255)
                else:
                    # Current line fades in
                    temp_surface = text_surface.copy()
                    temp_surface.set_alpha(min(current_alpha, 255))
                self.screen.blit(temp_surface, explanation_rects[j])

            pygame.display.flip()
            pygame.time.delay(10)  # Small delay for smooth animation

            # Update alpha for the current line
            current_alpha += 8
            if current_alpha >= 255:
                current_fade_index += 1
                current_alpha = 0

        # After animation, ensure all lines are fully visible
        self.screen.blit(explanation_bg, explanation_bg_rect)
        self.screen.blit(title_text, title_rect)
        for j in range(len(explanation)):
            temp_surface = explanation_surfaces[j].copy()
            temp_surface.set_alpha(255)
            self.screen.blit(temp_surface, explanation_rects[j])

        # Draw the "Play Again" button
        play_again_button = pygame.Rect(0, 0, 200, 60)
        play_again_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        pygame.draw.rect(self.screen, (100, 150, 255), play_again_button, border_radius=10)
        play_again_text = title_font.render("Play Again", True, (255, 255, 255))
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        self.screen.blit(play_again_text, play_again_text_rect)

        pygame.display.flip()

        # Handle input to restart or quit
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

