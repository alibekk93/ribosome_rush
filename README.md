md
# Ribosome Rush

A simple Pygame-based game where you control a ribosome to collect amino acids in a sequence to match a target protein sequence.

## How to Play
- **Objective**: Collect amino acids to match the target sequence displayed at the top.
- **Controls**: Use arrow keys (←↑↓→) to move the ribosome.
- **Scoring**:
  - Exact match: 10 points
  - Adjacent match: 5 points
  - Group match: 2 points
- **Game Over**: Ends when time (180s) runs out or 10 amino acids are collected. Win by scoring ≥50%.

## Installation
1. Ensure Python and Pygame are installed:
   ```bash
   pip install pygame
2. Clone the repo and run:
    ```bash
    python main.py
    ```

## Requirements
- Python 3.x
- Pygame