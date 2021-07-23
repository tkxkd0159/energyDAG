import socketio

DATA = {"test":"SSAMPLE"}
DATA2 = {"test2222":"777SSAMPLE"}

sio = socketio.Client()
sio2 = socketio.Client()
sio.connect("ws://127.0.0.1:5000")
sio2.connect("ws://127.0.0.1:5001")
# sio.emit('msg_from_client', DATA)
# sio2.emit('msg_from_client', DATA2)
print(sio.connected)
print(sio2.connected)



@sio.event
def connect(sid, environ):
    print("connect", sid)

@sio2.event
def connect(sid, environ):
    print("connect", sid)

@sio.event
def my_response(data):
    print(data)

@sio2.event
def my_response(data):
    print(data)