class named:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


PASS = named('PASS')
FAIL = named('FAIL')
