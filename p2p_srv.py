import argparse
import asyncio
import signal
import websockets
import requests
import threading

from os import getenv
HTTP_PORT = getenv('HTTP_PORT') if getenv('HTTP_PORT') is not None else '6002'
ADDR = "127.0.0.1"

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def consumer(msg, ws, path):
    if path == "/test":
        await ws.send("route to /test")
    else:
        print(msg)
        url = f"http://{ADDR}:{HTTP_PORT}/api/extx"
        h = {'Content-Type': 'application/json'}
        t = threading.Thread(target=requests.post, kwargs={'url':url, 'headers':h, 'data':msg})
        t.start()
        t.join()
        # await ws.send(msg)

async def consumer_handler(websocket, path):
    # await websocket.send("Start WebSocket ping test")
    try:
        async for message in websocket:
            await consumer(message, websocket, path)
    except:
        print("Connection loss abnormally")

async def ws_server(stop, addr, port):
    async with websockets.serve(consumer_handler, addr, port):
        print(f"\n * WebSocket Server : Listening to {addr}:{port} \n")
        await stop

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs='?')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    loop.run_until_complete(ws_server(stop, ADDR, int(args.port)))