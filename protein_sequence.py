import pygame
import random
from constants import *

class ProteinSequence:
    def __init__(self, images):
        self.sequence = [random.choice(ALL_AMINO_ACIDS) for _ in range(10)]
        self.collected_sequence = []
        self.current_index = 0
        self.amino_acid_images = images

    def current_amino_acid(self):
        return self.sequence[self.current_index] if self.current_index < len(self.sequence) else None

    def next_amino_acid(self):
        self.current_index += 1

    def add_collected(self, amino_acid):
        self.collected_sequence.append(amino_acid)
    
    def calculate_alignment_score(self):
        alignment_score = 0
        min_len = min(len(self.sequence), len(self.collected_sequence))
        for i in range(min_len):
            target_aa = self.sequence[i]
            collected_aa = self.collected_sequence[i]
            if collected_aa == target_aa:
                alignment_score += 10  # Exact match at the same position
            else:
                # Check for adjacent matches
                adjacent_match = False
                if i > 0 and self.collected_sequence[i-1] == target_aa:
                    adjacent_match = True
                if i < min_len - 1 and self.collected_sequence[i+1] == target_aa:
                    adjacent_match = True
                if adjacent_match:
                    alignment_score += 5  # Correct AA at adjacent position
                elif self.get_amino_acid_group(collected_aa) == self.get_amino_acid_group(target_aa):
                    alignment_score += 2  # Same group at the same position
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
            aa_image = self.amino_acid_images[aa]
            aa_rect = aa_image.get_rect()
            aa_rect.topleft = (x_offset + i * (aa_size + spacing), y_offset)
            surface.blit(aa_image, aa_rect)
            if i == self.current_index:
                pygame.draw.rect(surface, GREEN, aa_rect, 2)  # Highlight current AA

        # Draw collected sequence
        collected_y_offset = y_offset + aa_size + 10
        for i, collected_aa in enumerate(self.collected_sequence):
            aa_image = self.amino_acid_images[collected_aa]
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