from pathlib import Path
import plyvel
import json

from kudag.param import P2P_PORT



db_path = Path(__file__).parents[2].joinpath("db/")
if not db_path.exists():
    db_path.mkdir(parents=True)
dag_path = db_path.joinpath(P2P_PORT)
DB = plyvel.DB(str(dag_path), create_if_missing=True)

state_path = Path(__file__).parents[2].joinpath("state/")
if not state_path.exists():
    state_path.mkdir(parents=True)
statedb_path = state_path.joinpath(P2P_PORT)
STATE_DB = plyvel.DB(str(statedb_path), create_if_missing=True)

# sample_dict = {"a":2314, "b":1111}
# target = json.dumps(sample_dict).encode('utf-8')
# db.put(b'main', target)
# print(db.get(b'main'))

# db.put(b'key4', b'value33333')
# db.put(b'another-key2', b'another-value')
# print(db.get(b'key2'))
# print(db.get(b'another-key2'))


# if __name__ == "__main__":
#     from kudag.dag import DAG, TX

#     testdb = plyvel.DB(str(dag_path), create_if_missing=True)
#     db_snapshot = testdb.snapshot()
#     mydag = DAG()
#     mytx = TX()
#     tx_key = mytx.hash(make_txid=True).hexdigest()
#     mydag.txs[tx_key] = mytx.serialize()
#     target = json.dumps(mytx.serialize()).encode()
#     testdb.put(tx_key.encode(), target)

#     for k, v in testdb:
#         print(k, v)

#     print("Snapshot Test")
#     for k, v in  db_snapshot:
#         print(k, v)

#     db_snapshot.close()
#     testdb.close()

