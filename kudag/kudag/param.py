import os

## crpyto.py

READABLE_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' # For base58


## dag.py
DIFFICULTY = 0

## network.py
# os.environ['P2P_PORT'] = '6001'
P2P_PORT = os.getenv('P2P_PORT') if os.getenv('P2P_PORT') is not None else '6001'

