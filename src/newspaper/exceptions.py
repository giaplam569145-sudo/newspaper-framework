"""Custom exceptions for the Newspaper Framework."""


class NewspaperFrameworkError(Exception):
    """Raised for hard validation errors (empty title, short content, etc.)."""
    pass


class NewspaperFrameworkWarning(UserWarning):
    """Emitted for non-critical issues (missing images, missing logo)."""
    pass
