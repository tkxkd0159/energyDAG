# pip install -e .
import threading
import asyncio
import json

from kudag.db import init_db, init_state_db
from kudag.param import HTTP_PORT, PEERS
from kudag.network import broadcast, deploy_ws_worker


try:
    MY_DB = init_db(HTTP_PORT)
    MY_SDB = init_state_db(HTTP_PORT)

    for p in PEERS:
        deploy_ws_worker(p)
except:
    pass
