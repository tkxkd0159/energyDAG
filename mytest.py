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

def postfile(url):
    flist = [open('test_rest.json', 'rb'), open('pyrightconfig.json', 'rb')]
    myfiles = [('file', flist[0]), ('file', flist[1])]
    r = requests.post(url=url, files=myfiles)

    for f in flist:
        f.close()

    print(r.text)
    return 200

def gettx(url, key) -> dict:
    tx = requests.get(url=url).json()
    return tx[key]

class Crypto(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_keygen(self):
        self.assertTrue(keygen())



class Network(unittest.TestCase):
    def setUp(self):
        self.mytx = TX()
        self.url = ["http://127.0.0.1:5000/dag", 'http://127.0.0.1:5000/upload']
        self.header = {'Content-Type': 'application/json'}
        self.keyset = ["mytxid"]

    def test_1_post(self):
        self.assertEqual(posttx(self.mytx, self.url[0], self.header), 200)
        self.assertEqual(postfile(self.url[1]), 200)


    def test_2_get(self):
        for key in self.keyset:
            self.assertCountEqual(gettx(self.url[0], key), TX().serialize())





if __name__ == '__main__':
    unittest.main()   # python -m unittest -v mytest
                      # python -m unittest -v mytest.Crypto