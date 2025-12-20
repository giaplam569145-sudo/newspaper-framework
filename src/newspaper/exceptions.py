"""Custom exceptions for the Newspaper Framework."""

class NewspaperFrameworkWarning(Exception):
    """Custom exception for framework-specific warnings.

    This exception is raised for non-critical errors that should be
    communicated to the LLM in a user-friendly manner.
    """
    pass
