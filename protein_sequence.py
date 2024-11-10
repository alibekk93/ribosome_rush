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