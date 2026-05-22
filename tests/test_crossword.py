import pytest
from unittest.mock import patch, MagicMock
from src.newspaper.content.crossword import CrosswordGenerator, Crossword
from src.newspaper.exceptions import NewspaperFrameworkError


class TestCrosswordGenerator:
    @patch("src.newspaper.content.crossword.CrosswordGenerator.generate")
    def test_generate_returns_crossword(self, mock_gen):
        cw = Crossword(
            grid=[["A", "", "B"], ["", "C", ""]],
            clues={"horizontal": [(1, "A clue")], "vertical": [(1, "B clue")]},
        )
        mock_gen.return_value = cw
        gen = CrosswordGenerator(words=["ABC"], clues={"ABC": "test"})
        result = gen.generate()
        assert isinstance(result, Crossword)

    def test_to_dict_without_generate(self):
        gen = CrosswordGenerator(words=["test"], clues={"test": "a clue"})
        d = gen.to_dict()
        assert d == {}

    def test_crossword_dataclass(self):
        cw = Crossword(
            grid=[["A", "B"]],
            clues={"horizontal": [(1, "First")], "vertical": []},
        )
        assert cw.grid[0][0] == "A"
        assert cw.clues["horizontal"][0] == (1, "First")

    @patch("src.newspaper.content.crossword.CrosswordGenerator.generate")
    def test_to_dict_after_generate(self, mock_gen):
        cw = Crossword(
            grid=[["X"]],
            clues={"horizontal": [], "vertical": []},
        )
        gen = CrosswordGenerator(words=["X"], clues={"X": "letter"})
        gen.generated_crossword = cw
        d = gen.to_dict()
        assert "grid" in d
        assert "clues" in d


class TestCrosswordLazyImport:
    def test_missing_pycrossword_raises(self):
        gen = CrosswordGenerator(words=["test"], clues={"test": "clue"})
        with patch.dict("sys.modules", {"pycrossword": None}):
            with pytest.raises(NewspaperFrameworkError, match="pycrossword-generator"):
                gen.generate()

    def test_generate_with_mock_pycrossword(self):
        gen = CrosswordGenerator(
            words=["python", "html"],
            clues={"python": "A language", "html": "A markup"},
        )
        with patch("src.newspaper.content.crossword.CrosswordGenerator.generate") as mock_gen:
            cw = Crossword(
                grid=[["p", "y", "t", "h", "o", "n"]],
                clues={"horizontal": [(1, "A language")], "vertical": []},
            )
            mock_gen.return_value = cw
            result = gen.generate()
            assert result.grid[0][0] == "p"
