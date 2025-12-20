"""Sudoku generator implementation."""

import random
from typing import List, Dict
from .base import ContentGenerator

class SudokuGenerator(ContentGenerator):
    """Generates and formats Sudoku puzzles.

    Attributes:
        difficulty (str): The difficulty of the puzzle ('easy', 'medium', 'hard').
        grid (List[List[int]]): The 9x9 Sudoku grid.
    """

    def __init__(self, difficulty: str = "medium"):
        """Initializes the SudokuGenerator with a specified difficulty.

        Args:
            difficulty (str): The difficulty of the puzzle. Can be 'easy',
                'medium', or 'hard'. Defaults to 'medium'.
        """
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def generate(self) -> List[List[int]]:
        """Generates a new Sudoku grid based on the specified difficulty.

        This method uses a shuffling algorithm to create a valid, complete
        Sudoku grid and then removes a number of cells based on the
        difficulty level to create the puzzle.

        Returns:
            List[List[int]]: The generated 9x9 Sudoku grid with some cells
                set to 0 to represent empty spaces.
        """
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        r_base = range(base)
        rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
        cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
        nums = shuffle(range(1, base * base + 1))

        self.grid = [[nums[pattern(r, c)] for c in cols] for r in rows]

        cells_to_remove = {
            "easy": 30,
            "medium": 40,
            "hard": 50
        }.get(self.difficulty, 40)

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        for i in range(cells_to_remove):
            r, c = cells[i]
            self.grid[r][c] = 0

        return self.grid

    def to_dict(self) -> Dict:
        return {
            "difficulty": self.difficulty,
            "grid": self.grid
        }
