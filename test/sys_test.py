import unittest

from kudag.dag import TX, DAG
from kudag.crypto import createPublicKey, createPrivateKey

class Crypto(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_keygen(self):
        self.assertTrue(keygen())


def keygen():
    mykey = createPrivateKey()
    myvkey = createPublicKey(mykey)
    test = TX()
    test.addSign(mykey)

    return myvkey.verify(bytes.fromhex(test.sign), test.hash().digest())


if __name__ == '__main__':
    unittest.main()   # python -m unittest -v mytest
                      # python -m unittest -v mytest.Crypto