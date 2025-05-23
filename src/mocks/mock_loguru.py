class MockLogger:
    def info(self, *args, **kwargs):
        print(*args, **kwargs)

    def warning(self, *args, **kwargs):
        print(*args, **kwargs)

    def error(self, *args, **kwargs):
        print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        print(*args, **kwargs)

    def add(self, *args, **kwargs):
        print(*args, **kwargs)
