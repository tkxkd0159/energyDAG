from os import getenv
## crpyto.py

READABLE_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' # For base58


## dag.py
DIFFICULTY = 0



# os.environ['P2P_PORT'] = '6001'
HTTP_PORT = getenv('HTTP_PORT') if getenv('HTTP_PORT') is not None else '6001'
P2P_PORT = getenv('P2P_PORT') if getenv('P2P_PORT') is not None else '16001'