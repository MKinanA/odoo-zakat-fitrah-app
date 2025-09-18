class KeyErrorSafeDict(dict):
    to_return_on_missing_key = None
    def __init__(self, value, to_return_on_missing_key: object = None):
        self.to_return_on_missing_key = (lambda self, key: to_return_on_missing_key(key)) if callable(to_return_on_missing_key) else to_return_on_missing_key
        super().__init__(value)
    def __missing__(self, key): return self.to_return_on_missing_key(self, key) if callable(self.to_return_on_missing_key) else self.to_return_on_missing_key