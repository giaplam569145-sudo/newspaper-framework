import pytest
from src.newspaper.content.sudoku import SudokuGenerator


class TestSudokuGenerator:
    def test_default_difficulty(self):
        sg = SudokuGenerator()
        assert sg.difficulty == "medium"

    def test_generate_returns_9x9(self):
        sg = SudokuGenerator("easy")
        grid = sg.generate()
        assert len(grid) == 9
        for row in grid:
            assert len(row) == 9

    def test_easy_has_30_blanks(self):
        sg = SudokuGenerator("easy")
        grid = sg.generate()
        blanks = sum(cell == 0 for row in grid for cell in row)
        assert blanks == 30

    def test_medium_has_40_blanks(self):
        sg = SudokuGenerator("medium")
        grid = sg.generate()
        blanks = sum(cell == 0 for row in grid for cell in row)
        assert blanks == 40

    def test_hard_has_50_blanks(self):
        sg = SudokuGenerator("hard")
        grid = sg.generate()
        blanks = sum(cell == 0 for row in grid for cell in row)
        assert blanks == 50

    def test_generate_returns_copy(self):
        sg = SudokuGenerator()
        grid1 = sg.generate()
        grid1[0][0] = 999
        assert sg.grid[0][0] != 999

    def test_values_in_range(self):
        sg = SudokuGenerator()
        grid = sg.generate()
        for row in grid:
            for cell in row:
                assert 0 <= cell <= 9

    def test_to_dict(self):
        sg = SudokuGenerator("hard")
        sg.generate()
        d = sg.to_dict()
        assert d["difficulty"] == "hard"
        assert len(d["grid"]) == 9
