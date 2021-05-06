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

def posttx():
    mytx = TX()
    myjson = dumps(mytx.serialize())

    # curl -d @request.json -H "Content-Type: application/json" https://my.co.kr
    url = "http://127.0.0.1:5000/dag"
    mYheader = {'Content-Type': 'application/json'}
    payload = myjson
    r = requests.post(url=url, headers=mYheader, data=payload)
    print("My status code is", r.text)
    print(requests.get(url=url).json())

class MyTests(unittest.TestCase):
    def setUp(self) -> None:
        """Execute before test
        """
        pass

    def tearDown(self) -> None:
        """Execute after test
        """
        pass

    def test_func(self):
        keygen()
        posttx()





if __name__ == '__main__':
    unittest.main()