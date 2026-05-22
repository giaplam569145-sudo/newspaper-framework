"""Sudoku generator implementation."""

import random
from typing import Any, Dict, List
from .base import ContentGenerator

class SudokuGenerator(ContentGenerator):
    """Generates and formats Sudoku puzzles.

    Attributes:
        difficulty (str): The difficulty of the puzzle ('easy', 'medium', 'hard').
        grid (List[List[int]]): The 9x9 Sudoku grid (with blanks as 0).
        solution (List[List[int]]): The complete 9x9 solution grid.
    """

    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]

    def generate(self) -> List[List[int]]:
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
        self.solution = [row[:] for row in self.grid]

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

        return [row[:] for row in self.grid]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "difficulty": self.difficulty,
            "grid": self.grid,
            "solution": self.solution,
        }
