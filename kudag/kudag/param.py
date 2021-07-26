from os import getenv
## crpyto.py

READABLE_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' # For base58


## dag.py
DIFFICULTY = 0



# os.environ['P2P_PORT'] = '6001'
HTTP_PORT = getenv('HTTP_PORT') if getenv('HTTP_PORT') is not None else '6001'
if getenv('PEERS') is not None:
    p = getenv('PEERS')
    p = p.lstrip('[')
    p = p.rstrip(']')
    p = p.split(', ')
    PEERS = set(p)
else:
    PEERS = set(["ws://127.0.0.1:16001", "ws://127.0.0.1:16002"])
WSS = set()