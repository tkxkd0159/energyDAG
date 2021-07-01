import plyvel
from pathlib import Path
import json

mypath = Path(__file__).parent
mypath = mypath.joinpath('testdb')
print(mypath)
db = plyvel.DB(str(mypath), create_if_missing=True)
db.put(b'key', b'value')
print(db.get(b'key'))

sample_dict = {"a":2314, "b":1111}
target = json.dumps(sample_dict).encode('utf-8')
db.put(b'main', target)
print(db.get(b'main'))

target = db.get(b'main').decode()
target_update = json.loads(target)
target_update.update({"my":2, "new": "dict"})
print(target_update)
db.put(b'main', json.dumps(target_update).encode())
print(db.get(b'main'))
