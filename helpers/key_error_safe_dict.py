class KeyErrorSafeDict(dict):
    def __missing__(self, key) -> None: return None