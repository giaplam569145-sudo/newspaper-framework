import pytest
from src.newspaper.exceptions import NewspaperFrameworkError, NewspaperFrameworkWarning


class TestExceptionHierarchy:
    def test_error_is_exception(self):
        assert issubclass(NewspaperFrameworkError, Exception)

    def test_warning_is_user_warning(self):
        assert issubclass(NewspaperFrameworkWarning, UserWarning)

    def test_error_can_be_raised_and_caught(self):
        with pytest.raises(NewspaperFrameworkError):
            raise NewspaperFrameworkError("test error")

    def test_warning_not_caught_by_exception(self):
        with pytest.warns(NewspaperFrameworkWarning):
            import warnings
            warnings.warn("test", NewspaperFrameworkWarning)
