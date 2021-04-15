from dataclasses import dataclass, field
from time import time
from typing import TypeVar
from enum import Enum, auto
import json

from crypto import sha3_256

TX_ = TypeVar("TX_")
TXHASH = TypeVar("TXHASH", str, bytes)

class Status(Enum):
    leaf = auto()
    pending = auto()
    fixed = auto()
    conflicted = auto()
    stale = auto()

@dataclass
class TX:

    ver: int = 1
    timestamp: float = time()
    prts: set[TX_] = field(default_factory=set)
    clds: set[TX_] = field(default_factory=set)
    height: int = 0
    id: TXHASH = '0' * 64


    data: list[str] = field(default_factory=list)

    # Parameter for finality
    trusty: int = 0
    good: int = 0
    bad: int = 0

    # Validation
    status: int = 0
    nonce: int = 0
    conflTX: set[TX_] = field(default_factory=set) # conflicted TX with this TX
    tArriv: int = None
    tConfl: int = None
    tConf: int = None
    tStale: int = None
    validators: set = field(default_factory=lambda:set(['root']))

    def reset(self):
        self.ver = 1
        self.timestamp = 0
        self.prts = set()
        self.clds = set()
        self.nonce = 0
        self.height = 0
        self.id = '0' * 64
        self.data = None
        self.trusty  = 0
        self.good  = 0
        self.bad = 0
        self.status = 0
        self.conflTX = set()
        self.tArriv = 0
        self.tConfl = 0
        self.tFix = 0
        self.tStale = 0
        self.validators = set()

    def serialize(self):
        self.prts = list(self.prts)
        self.clds = list(self.clds)
        self.conflTX = list(self.conflTX)
        self.validators = list(self.validators)

        return json.dumps(vars(self))

    @staticmethod
    def deserialize(serializedTX):
        obj = TX(**json.loads(serializedTX))
        obj.prts = set(obj.prts)
        obj.clds = set(obj.clds)
        obj.conflTX = set(obj.conflTX)
        obj.validators = set(obj.validators)

        return obj

    def hash(self):
        myhash = sha3_256()
        myhash.update(self.serialize().encode())
        return myhash.digest()


class DAG:
    def __init__(self):
        self.txs: dict[TXHASH, TX] = {}

print(TX().hash())