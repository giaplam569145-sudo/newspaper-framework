"""Crossword generator implementation."""

from typing import Any, Dict, List, Tuple
from dataclasses import dataclass, asdict
from ..exceptions import NewspaperFrameworkError
from .base import ContentGenerator

@dataclass
class Crossword:
    """Represents a crossword puzzle.

    Attributes:
        grid (List[List[str]]): The crossword grid.
        clues (Dict[str, List[Tuple[int, str]]]): The clues for the crossword.
    """
    grid: List[List[str]]
    clues: Dict[str, List[Tuple[int, str]]]


class CrosswordGenerator(ContentGenerator):
    """Generates and formats crossword puzzles.

    Attributes:
        words (List[str]): A list of words to be included in the crossword.
        clues (Dict[str, str]): A dictionary of clues for the words.
    """

    def __init__(self, words: List[str], clues: Dict[str, str]):
        self.words = words
        self.clues = clues
        self.generated_crossword = None

    def generate(self) -> Crossword:
        try:
            from pycrossword import generate_crossword
        except ImportError:
            raise NewspaperFrameworkError(
                "pycrossword-generator is required for crossword generation. "
                "Install with: pip install pycrossword-generator"
            )

        dimensions, placed_words = generate_crossword(self.words)

        grid = [['' for _ in range(dimensions[0])] for _ in range(dimensions[1])]
        clues: Dict[str, List[Tuple[int, str]]] = {"horizontal": [], "vertical": []}
        word_starts: Dict[tuple, int] = {}

        clue_number = 1
        for word, x, y, is_horizontal in placed_words:
            if (x, y) not in word_starts:
                word_starts[(x, y)] = clue_number
                clue_number += 1

            num = word_starts[(x, y)]

            if is_horizontal:
                clues["horizontal"].append((num, self.clues[word]))
                for i, char in enumerate(word):
                    if x < len(grid) and (y + i) < len(grid[0]):
                        grid[x][y + i] = char
            else:
                clues["vertical"].append((num, self.clues[word]))
                for i, char in enumerate(word):
                    if (x + i) < len(grid) and y < len(grid[0]):
                        grid[x + i][y] = char

        for (x, y), num in word_starts.items():
            if x < len(grid) and y < len(grid[0]):
                grid[x][y] = f"{grid[x][y]}{num}"

        self.generated_crossword = Crossword(grid=grid, clues=clues)
        return self.generated_crossword

    def to_dict(self) -> Dict[str, Any]:
        if not self.generated_crossword:
            return {}
        return asdict(self.generated_crossword)
