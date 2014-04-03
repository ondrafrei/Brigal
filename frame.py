class Frame:
    def __init__(self):
        self._variables = dict()

    def __setitem__(self, key, value):
        self._variables[key] = value

    def __getitem__(self, key):
        return self._variables[key]
