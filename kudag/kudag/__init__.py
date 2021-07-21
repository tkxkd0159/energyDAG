# pip install -e .
import threading
import asyncio
import json

from kudag.db import init_db, init_state_db
from kudag.param import HTTP_PORT, PEERS
from kudag.network import broadcast, deploy_ws_worker

DATA = [{"name":"LJS", "age":20}, {"name":"WAS", "age":30}]

try:
    MY_DB = init_db(HTTP_PORT)
    MY_SDB = init_state_db(HTTP_PORT)

    for p in PEERS:
        res = deploy_ws_worker(p)
        if not res:
            print("Your WebSocket Receiver can't be deployed")

    broadcast(json.dumps(DATA))

except:
    pass
