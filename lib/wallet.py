from dataclasses import dataclass
from uuid import uuid4

from .crypto import createPrivateKey, createPublicKey, createAddr

def initWallet():
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
