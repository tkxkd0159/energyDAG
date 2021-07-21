import asyncio
import threading
import websockets
import json
from enum import Enum, auto

from kudag.param import WSS

class QueryType(Enum):
    EXT_TX = auto()
    INT_TX = auto()

async def init_ws_connection(uri):
    try:
        ws = await websockets.connect(uri)
        return ws
    except ConnectionRefusedError:
        print(f" \n >>> {uri} is unhealthy\n")

async def recv_handler(ws, addr):

    await ws.send("Complete ping-pong test")
    print(f" * WebSocket receiver connect to {addr}", flush=True)
    async for msg in ws:
        print(f"<<<< {msg}")


async def ws_worker(addr):

    task = asyncio.create_task(init_ws_connection(addr))
    ws = await task
    if ws is not None:
        WSS.add(ws)
    else:
        return False

    task = asyncio.create_task(recv_handler(ws, addr))
    await task

    await ws.close()

def deploy_ws_worker(p):
    t = threading.Thread(target=asyncio.run, args=(ws_worker(p),))
    t.daemon = True
    t.start()
    return True

async def _broadcast(msg):
    await asyncio.sleep(0.1)
    # print("my websocket list :", WSS, flush=True)
    for ws in WSS:
        await ws.send(msg)


def broadcast(msg):
    print(" * Broadcasting your TX")
    t = threading.Thread(target=asyncio.run, args=(_broadcast(msg),))
    t.daemon = True
    t.start()
    t.join()
    print(" * Complete broadcasting ")