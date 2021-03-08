"""Build the timefunc decorator."""




class Test:

    def __init__(self, inst):
        self.inst = inst

    def my_print(self):
        print(self.inst)


class Dummy:

    def __init__(self):
        pass

    def test(self):
        print("mine")


a = Test(Dummy())
a.inst.test()

