from os import getenv

## crpyto.py

READABLE_ALPHABET = (
    b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"  # For base58
)


## dag.py
DIFFICULTY = 0


# os.environ['P2P_PORT'] = '6001'
HTTP_PORT = getenv("HTTP_PORT") if getenv("HTTP_PORT") is not None else "6001"


def PEERS() -> set:
    if getenv("PEERS") is not None:
        peers = getenv("PEERS")
        peers = peers.lstrip("[")
        peers = peers.rstrip("]")
        peers = peers.split(", ")
        for p in peers:
            if not p.startswith("ws://"):
                raise Exception("Peer address must start with ws://")
        PEERS = set(peers)
        print(f" * PEERS : {PEERS}", flush=True)
    else:
        raise Exception("PEERS is not set")

    return PEERS


WSS = set()
