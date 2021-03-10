import json

class blocks:
    def __init__(self):
        self.mine = 1
        self.two = "two"
        self.three = [1, 2, 3]

    @property
    def getChain(self):
        return {
            "mine": self.mine,
            "two": self.two,
            "three": self.three
        }

a = blocks()
b = json.dumps(a.getChain)
print(b)

