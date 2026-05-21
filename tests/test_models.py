import pytest
import warnings
from src.newspaper.models import Article, LayoutConfig, MediaConfig, Question
from src.newspaper.exceptions import NewspaperFrameworkError, NewspaperFrameworkWarning


class TestArticle:
    def test_valid_article(self):
        a = Article(title="Test", content="A valid article content here")
        assert a.title == "Test"
        assert a.content == "A valid article content here"
        assert a.author == "Unbekannt"
        assert a.priority == 1

    def test_title_trimmed(self):
        a = Article(title="  Spaces  ", content="Valid content here...")
        assert a.title == "Spaces"

    def test_content_too_short_raises_error(self):
        with pytest.raises(NewspaperFrameworkError):
            Article(title="Test", content="kurz")

    def test_empty_content_raises_error(self):
        with pytest.raises(NewspaperFrameworkError):
            Article(title="Test", content="")

    def test_priority_clamped_low(self):
        a = Article(title="T", content="Valid content here...", priority=-5)
        assert a.priority == 1

    def test_priority_clamped_high(self):
        a = Article(title="T", content="Valid content here...", priority=100)
        assert a.priority == 5

    def test_missing_image_path_warns(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            a = Article(title="T", content="Valid content here...", image_path="nonexistent.png")
            assert a.image_path is None
            assert len(w) == 1
            assert issubclass(w[0].category, NewspaperFrameworkWarning)

    def test_valid_image_path_accepted(self, tmp_path):
        img = tmp_path / "logo.png"
        img.write_text("fake")
        a = Article(title="T", content="Valid content here...", image_path=str(img))
        assert a.image_path == str(img)

    def test_kwargs_passed(self):
        a = Article(
            title="T", content="Valid content here...",
            author="Max", category="Tech", priority=3,
            image_caption="A caption"
        )
        assert a.author == "Max"
        assert a.category == "Tech"
        assert a.priority == 3
        assert a.image_caption == "A caption"


class TestQuestion:
    def test_valid_question(self):
        q = Question(question="What is AI?", options=["AI", "BI"], correct_index=0)
        assert q.question == "What is AI?"
        assert len(q.options) == 2

    def test_question_too_short(self):
        with pytest.raises(NewspaperFrameworkError):
            Question(question="Hi", options=["A", "B"], correct_index=0)

    def test_empty_question(self):
        with pytest.raises(NewspaperFrameworkError):
            Question(question="", options=["A", "B"], correct_index=0)

    def test_too_few_options(self):
        with pytest.raises(NewspaperFrameworkError):
            Question(question="Valid question?", options=["Only one"], correct_index=0)

    def test_correct_index_out_of_bounds(self):
        with pytest.raises(NewspaperFrameworkError):
            Question(question="Valid question?", options=["A", "B"], correct_index=5)


class TestLayoutConfig:
    def test_defaults(self):
        lc = LayoutConfig()
        assert lc.font_family == "Arial"
        assert lc.max_width == 800
        assert lc.spacing == 20

    def test_custom(self):
        lc = LayoutConfig(font_family="Helvetica", max_width=1200)
        assert lc.font_family == "Helvetica"
        assert lc.max_width == 1200


class TestMediaConfig:
    def test_defaults(self):
        mc = MediaConfig()
        assert mc.logo_path is None
        assert mc.supported_formats == ["png", "jpg", "jpeg", "gif", "svg"]

    def test_custom_formats(self):
        mc = MediaConfig(supported_formats=["webp"])
        assert mc.supported_formats == ["webp"]
