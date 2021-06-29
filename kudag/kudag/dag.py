import sys
from dataclasses import dataclass, field
from time import time
from typing import NewType, TypeVar, Union
from enum import Enum, auto
import json
from copy import deepcopy

from kudag.crypto import sha3_256


Tx = NewType("Tx", object)
TxHash = TypeVar("TxHash", str, bytes)
TxID = NewType("TxID", str)

TX_POOL = []




class Status(Enum):
    pending = auto()
    confirmed = auto()
    conflicted = auto()
    stale = auto()

@dataclass
class TX:
    ver: int = 0
    timestamp: float = time()
    nonce: int = 0
    height: int = 0
    from_: str = ""
    to_: str = ""
    sign: str = ""
    data: dict[str, Union[int, str]] = field(default_factory=lambda: {"value": 0})
    prts: set[Tx] = field(default_factory=set)
    clds: set[Tx] = field(default_factory=set)
    id: TxID = ""

    # Parameter for finality
    trusty: int = 0


    # Validation
    status: int = Status.pending
    conflTX: set[Tx] = field(default_factory=set) # conflicted TX with this TX
    tArriv: int = 0
    tConfl: int = 0
    tConf: int = 0
    tStale: int = 0
    validators: set = field(default_factory=lambda: set(['LJS']))

    def reset(self):
        self.ver = 1
        self.timestamp = 0
        self.nonce = 0
        self.height = 0
        self.from_ = ""
        self.to_ = ""
        self.sign = ""
        self.data = {}
        self.prts = set()
        self.clds = set()
        self.id = None

        # meta data
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
    def deserialize(serialTX: str) -> Tx:
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
    """[summary]
    :param db: levelDB instance
    """
    def __init__(self, db):

        self.txs: dict[TxHash, dict] = {}
        self.txid_list: list[str] = []
        self.balances: dict[str, int] = {}
        self.db = db

    def add_tx(self, TX: Tx):
        tx_key = TX.hash(make_txid=True).hexdigest()
        tx_value = TX.serialize()
        self.txs[tx_key] = tx_value
        tx_str = json.dumps(tx_value)
        self.db.put(tx_key.encode(), tx_str.encode())

        return tx_key, tx_str

    def rm_tx(self, txids: list[TxID]):
        for txid in txids:
            self.db.delete(txid.encode())
            del self.txs[txid]
            self.txid_list.remove(txid)

    def _make_state(self, is_initial=False, tx_data: Tx=None):
        if is_initial:
            if tx_data.status == Status.confirmed:
                pass

    @staticmethod
    def get_state():
        pass

    def load_dag(self):
        try:
            for k, v in self.db:
                k = k.decode()
                v = v.decode()
                self.txs[k] = json.loads(v)
                self.txid_list.append(k)

                tx_data = TX.deserialize(v)
                if tx_data.status == Status.confirmed:
                    if tx_data.from_ != "":
                        self.balances[tx_data.from_] = self.balances.get(tx_data.from_, 0) - tx_data.data['value']
                    if tx_data.to_ != "":
                        self.balances[tx_data.to_] = self.balances.get(tx_data.to_, 0) + tx_data.data['value']

            return True

        except:
            e = sys.exc_info()[0]
            print(e)
            return False

