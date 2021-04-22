from json import dumps, loads
import requests

from lib.dag import TX, DAG
from lib.crypto import createPublicKey, createPrivateKey


mykey = createPrivateKey()
myvkey = createPublicKey(mykey)
test = TX()
test.addSign(mykey)

print(myvkey.verify(bytes.fromhex(test.id), test.hash().digest()))


mytx = TX()
myjson = dumps(mytx.serialize())

# curl -d @request.json -H "Content-Type: application/json" https://my.co.kr
url = "http://127.0.0.1:5000/dag"
mYheader = {'Content-Type': 'application/json'}
payload = myjson
print(payload)

r = requests.post(url=url, headers=mYheader, data=payload)

print("My status code is", r.text)