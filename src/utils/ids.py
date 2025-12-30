import itertools

class IDGenerator:
    _counter = itertools.count(1)

    @classmethod
    def next_id(cls) -> int:
        return next(cls._counter)
