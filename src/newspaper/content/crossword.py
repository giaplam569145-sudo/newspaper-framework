"""Crossword generator implementation."""

from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from pycrossword import generate_crossword
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
        """Initializes the CrosswordGenerator with words and clues.

        Args:
            words (List[str]): A list of words for the crossword.
            clues (Dict[str, str]): A dictionary of clues for the words.
        """
        self.words = words
        self.clues = clues
        self.generated_crossword = None

    def generate(self) -> Crossword:
        """Generates a new crossword puzzle.

        Returns:
            Crossword: The generated crossword puzzle.
        """
        # pycrossword-generator returns dimensions and placed words
        dimensions, placed_words = generate_crossword(self.words)

        # grid init with empty strings
        grid = [['' for _ in range(dimensions[0])] for _ in range(dimensions[1])]
        clues = {"horizontal": [], "vertical": []}
        word_starts = {}

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

    def to_dict(self) -> Dict:
        if not self.generated_crossword:
             return {}
        return asdict(self.generated_crossword)
