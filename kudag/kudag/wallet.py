from os import listdir
from dataclasses import dataclass
from uuid import uuid4
from pathlib import Path
from ecdsa import SigningKey
from hashlib import sha256

from kudag.crypto import createPrivateKey, createPublicKey, createAddr
from kudag.param import HTTP_PORT


class Wallet:

    def __init__(self, user_id, pwhash):
        s = user_id + pwhash
        m = sha256()
        m.update(s.encode())
        self.seed = m.hexdigest()
        self.path = Path(__file__).parents[2].joinpath(f"wallet/{self.seed}")
        if not self.path.exists():
            self.path.mkdir(parents=True)

        self.key_nums: int = 0
        self.sk = {}
        self.vk = {}
        self.addr = {}

    def init(self):
        if not self.path.joinpath('private0.pem').exists():
            self.sk['0'] = createPrivateKey(self.seed)
            self.vk['0'] = createPublicKey(self.sk['0'])
            with open(str(self.path)+"/private0.pem", 'wb') as f:
                f.write(self.sk['0'].to_pem())
            with open(str(self.path)+"/public0.pem", 'wb') as f:
                f.write(self.vk['0'].to_pem())
        else:
            self.key_nums = int(len(listdir(self.path)) / 2)
            round = self.key_nums

            for i in range(round):
                j = str(i)
                with open(str(self.path)+f"/private{i}.pem", 'rb') as f:
                    self.sk[j] = SigningKey.from_pem(f.read())
                self.vk[j] = createPublicKey(self.sk[j])
                self.addr[j], _ = createAddr(self.vk[j])

    def add_newkey_from_master(self):
        i = f'{self.key_nums}'
        tmp_seed = self.seed + i
        target_skname = f'private{i}.pem'
        target_vkname = f'public{i}.pem'
        self.sk[i] = createPrivateKey(tmp_seed)
        self.vk[i] = createPublicKey(self.sk[i])
        with open(str(self.path) + f'/{target_skname}', 'wb') as f:
            f.write(self.sk[i].to_pem())
        with open(str(self.path) + f'/{target_vkname}', 'wb') as f:
            f.write(self.vk[i].to_pem())
        self.addr[i], _ = createAddr(self.vk[i])
        self.key_nums += 1



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
