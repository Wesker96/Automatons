"""Mocks for difference class."""


class MockLogger:
    """Mock for loguru.logging."""

    def info(self, *args: tuple, **kwargs: dict) -> None:
        """Mock for info."""
        print(*args, **kwargs)

    def warning(self, *args: tuple, **kwargs: dict) -> None:
        """Mock for warning."""
        print(*args, **kwargs)

    def error(self, *args: tuple, **kwargs: dict) -> None:
        """Mock for error."""
        print(*args, **kwargs)

    def debug(self, *args: tuple, **kwargs: dict) -> None:
        """Mock for debug."""
        print(*args, **kwargs)

    def add(self, *args: tuple, **kwargs: dict) -> None:
        """Mock for add."""
        print(*args, **kwargs)

    def exception(self, *args: tuple, **kwargs: dict) -> None:
        """Mock for add."""
        print(*args, **kwargs)
