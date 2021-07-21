import asyncio
import socketio

class WsClient:
    def __init__(self, addr):
        self.addr = addr
        sio = socketio.AsyncClient(engineio_logger=True)
        self.sio = sio

        @sio.on('pong_from_server')
        async def on_pong(data):
            await sio.sleep(5)
            await self.send_ping()

        @sio.event
        async def connect():
            print('connection established')
            await self.send_ping()

        @sio.event
        async def my_message(data):
            print('message received with ', data)
            await sio.emit('my response', {'response': 'my response'})

        @sio.event
        async def disconnect():
            print('disconnected from server')


    async def send_ping(self):
        await self.sio.emit('ping_from_client')

    async def start(self):
        await self.sio.connect(self.addr)
        await self.sio.wait()

    # @sio.on('connect')
    # async def on_connect():
    #     print('connected to server')
    #     await send_ping()


# async def main():
#     await sio.connect('http://localhost:5000')
#     await sio.connect('http://localhost:5001')
#     await sio.wait()

if __name__ == '__main__':
    cl1 = WsClient("http://localhost:5000")
    cl2 = WsClient("http://localhost:5001")
    asyncio.run(cl1.start())
    asyncio.run(cl2.start())
    print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
