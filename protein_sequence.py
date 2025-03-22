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
        explanation = []
        # Iterate over all positions in the target sequence
        for i in range(len(self.sequence)):
            target_aa = self.sequence[i]
            # Check if a collected AA exists for this position
            if i < len(self.collected_sequence):
                collected_aa = self.collected_sequence[i]
                if collected_aa == target_aa:
                    score = 10
                    reason = "Exact match"
                else:
                    # Check for adjacent match
                    adjacent_match = False
                    if i > 0 and i-1 < len(self.collected_sequence) and self.collected_sequence[i-1] == target_aa:
                        adjacent_match = True
                    if i < len(self.sequence)-1 and i+1 < len(self.collected_sequence) and self.collected_sequence[i+1] == target_aa:
                        adjacent_match = True
                    if adjacent_match:
                        score = 5
                        reason = "Adjacent match"
                    elif self.get_amino_acid_group(collected_aa) == self.get_amino_acid_group(target_aa):
                        score = 2
                        reason = "Group match"
                    else:
                        score = 0
                        reason = "No match"
            else:
                # No AA collected for this position
                collected_aa = None
                score = 0
                reason = "Not collected"
            alignment_score += score
            explanation.append({
                'target': target_aa,
                'collected': collected_aa if collected_aa is not None else "None",
                'score': score,
                'reason': reason
            })
        return alignment_score, explanation

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

        for i, aa in enumerate(self.sequence):
            aa_image = self.amino_acid_images[aa]
            aa_rect = aa_image.get_rect()
            aa_rect.topleft = (x_offset + i * (aa_size + spacing), y_offset)
            surface.blit(aa_image, aa_rect)
            if i == self.current_index:
                pygame.draw.rect(surface, GREEN, aa_rect, 2)

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
                        pygame.draw.rect(surface, YELLOW, aa_rect, 2)
                    else:
                        pygame.draw.rect(surface, RED, aa_rect, 2)