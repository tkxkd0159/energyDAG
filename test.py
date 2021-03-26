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

#
print(bytes.fromhex("7E7F"))

a = bytearray(b'2F')
print(int.from_bytes(a, byteorder="little")) # 0x4632
print(int.from_bytes(a, byteorder="big"))    # 0x3246
print(bytes.fromhex("0A"))