from dataclasses import dataclass
from uuid import uuid4
from pathlib import Path
from ecdsa.keys import SigningKey, VerifyingKey

from kudag.crypto import createPrivateKey, createPublicKey, createAddr
from kudag.param import P2P_PORT

class Wallet:
    def __init__(self):
        self.path = Path(__file__).parents[2].joinpath(f"wallet/{P2P_PORT}")
        if not self.path.exists():
            self.path.mkdir(parents=True)

    def init_wallet(self):
        if not self.path.joinpath('private.pem').exists():
            self.sk = createPrivateKey()
            vk = createPublicKey(self.sk)
            with open(str(self.path)+"/private.pem", 'wb') as f:
                f.write(self.sk.to_pem())
            with open(str(self.path)+"/public.pem", 'wb') as f:
                f.write(vk.to_pem())
        else:
            with open(str(self.path)+"/private.pem", 'rb') as f:
                self.sk = SigningKey.from_pem(f.read())
            vk = createPublicKey(self.sk)

        self.addr, _ = createAddr(vk)


my_wallet = Wallet()
my_wallet.init_wallet()
print(my_wallet.addr)

#! Deprecated
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