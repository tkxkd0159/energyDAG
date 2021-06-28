from dataclasses import dataclass, field
from time import time
from typing import NewType
from enum import Enum, auto
import json
from copy import deepcopy

from kudag.crypto import sha3_256
from kudag.db import db

Tx = NewType("Tx")
TxHash = NewType("TxHash", str, bytes)
TxID = NewType("TxID", str)

class Status(Enum):
    pending = auto()
    confirmed = auto()
    conflicted = auto()
    stale = auto()

@dataclass
class TX:

    timestamp: float = time()
    prts: set[Tx] = field(default_factory=set)
    clds: set[Tx] = field(default_factory=set)
    height: int = 0
    id: TxID = ""
    sign: str = ""


    data: list[str] = field(default_factory=list)

    # Parameter for finality
    trusty: int = 0

    # Validation
    status: int = Status.pending
    nonce: int = 0
    conflTX: set[Tx] = field(default_factory=set) # conflicted TX with this TX
    tArriv: int = 0
    tConfl: int = 0
    tConf: int = 0
    tStale: int = 0
    validators: set = field(default_factory=lambda:set(['root', 'lord']))

    def reset(self):
        self.ver = 1
        self.timestamp = 0
        self.prts = set()
        self.clds = set()
        self.nonce = 0
        self.height = 0
        self.id = None
        self.data = None
        self.trusty  = 0
        self.good  = 0
        self.bad = 0
        self.status = Status.pending
        self.conflTX = set()
        self.tArriv = 0
        self.tConfl = 0
        self.tFix = 0
        self.tStale = 0
        self.validators = set()

    def serialize(self) -> dict:
        self.prts = list(self.prts)
        self.clds = list(self.clds)
        self.conflTX = list(self.conflTX)
        self.validators = list(self.validators)

        if isinstance(self.status, Status):
            self.status = self.status.value


        return vars(self)

    @staticmethod
    def deserialize(serialTX: dict) -> Tx:
        obj = TX(**json.loads(serialTX))
        obj.prts = set(obj.prts)
        obj.clds = set(obj.clds)
        obj.conflTX = set(obj.conflTX)
        obj.validators = set(obj.validators)

        status_map = {1: Status.pending, 2: Status.confirmed, 3: Status.conflicted, 4: Status.stale}

        if isinstance(obj.status, int):
            obj.status = status_map[obj.status]


        return obj

    def hash(self, make_txid=False) -> bytes:
        serialTX = deepcopy(self.serialize())
        serialTX.pop("id")
        serialTX.pop("sign")
        myhash = sha3_256()
        myhash.update(json.dumps(serialTX).encode())
        if make_txid:
            self.id = myhash.digest().hex()
        return myhash

    def addSign(self, pvtK):
        txhash = self.hash().digest()
        signature = pvtK.sign_deterministic(txhash)
        self.sign = signature.hex()


class DAG:
    def __init__(self):
        self.txs: dict[TxHash, TX] = {}

    def add_tx(self):
        pass

    def compare(self):
        pass
