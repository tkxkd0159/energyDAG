import os
import json
import plyvel

# os.environ['P2P_PORT'] = '6001'

P2P_PORT = os.getenv('P2P_PORT') if os.getenv('P2P_PORT') is not None else 6001
db = plyvel.DB('./db/', create_if_missing=True)

# sample_dict = {"a":2314, "b":1111}
# target = json.dumps(sample_dict).encode('utf-8')
# db.put(b'blockchain', target)
print(db.get(b'blockchain'))

# db.put(b'key4', b'value33333')
# db.put(b'another-key2', b'another-value')
# print(db.get(b'key2'))
# print(db.get(b'another-key2'))

