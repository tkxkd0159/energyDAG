import unittest
from json import dumps, loads
import requests

from lib.dag import TX, DAG
from lib.crypto import createPublicKey, createPrivateKey


def keygen():
    mykey = createPrivateKey()
    myvkey = createPublicKey(mykey)
    test = TX()
    test.addSign(mykey)

    return myvkey.verify(bytes.fromhex(test.id), test.hash().digest())

def posttx(tx, url, header):
    myjson = dumps(tx.serialize())
    payload = myjson

    # curl -d @request.json -H "Content-Type: application/json" https://my.co.kr
    r = requests.post(url=url, headers=header, data=payload)
    return int(r.text)

def gettx(url):
    requests.get(url=url).json()

class Crypto(unittest.TestCase):
    def setUp(self) -> None:
        """Execute before test method
        """
        pass

    def tearDown(self) -> None:
        """Execute after test method
        """
        pass

    def test_keygen(self):
        self.assertTrue(keygen())



class Network(unittest.TestCase):
    def setUp(self):
        self.mytx = TX()
        self.url = "http://127.0.0.1:5000/dag"
        self.header = {'Content-Type': 'application/json'}

    def test_post(self):
        self.assertEqual(posttx(self.mytx, self.url, self.header), 200)


    def test_get(self):
        gettx(self.url)





if __name__ == '__main__':
    unittest.main()   # python -m unittest -v mytest