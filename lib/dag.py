from dataclasses import dataclass
from uuid import uuid4

class TX:
    def __init__(self):
        self.clds = set() # hash value
        self.prts = set() # hash value
        self.data = str()

        self.timestamp = 0
        self.index = 0
        self.nonce = 0
        self.depth = 0
        self.trusty = 0
        self.good = 0
        self.bad = 0

        # Validation
        self.status = None   # conflicted / confirmed / deactivated / None
        self.conflTx = None # conflicted TX with this TX
        self.tConfl = None
        self.tConf = None
        self.tDeact = None
        self.validators = set()


class DAG:
    def __init__(self):
        pass


@dataclass
class UTXO:
    id: str = uuid4().hex     # int(id, base=16), bin : binary
    balance: int = 0

    def divide(self):
        """Use this method when you need small UTXO
        """
        pass

    def sum(self):
        """Use this method when you need large UTXO
        """
        pass
