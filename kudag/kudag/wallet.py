from os import listdir
from dataclasses import dataclass
from uuid import uuid4
from pathlib import Path
from ecdsa import SigningKey


from kudag.crypto import createPrivateKey, createPublicKey, createAddr
from kudag.param import P2P_PORT

# TODO : P2P port에서 DB에 등록된 로그인 해쉬로 폴더이름 변경
# TODO : 로그인 시 지갑 탐색 후 없으면 자동 생성, key store 개념 -> 실제 잔액은 statedb에서 indexing
class Wallet:
    def __init__(self, pwhash=P2P_PORT):
        self.seed = pwhash
        self.path = Path(__file__).parents[2].joinpath(f"wallet/{self.seed}")
        if not self.path.exists():
            self.path.mkdir(parents=True)

        self.key_nums = 0
        self.sk = {}
        self.vk = {}
        self.addr = {}

    def init(self):
        if not self.path.joinpath('private.pem').exists():
            self.sk['0'] = createPrivateKey(self.seed)
            self.vk['0'] = createPublicKey(self.sk['0'])
            with open(str(self.path)+"/private.pem", 'wb') as f:
                f.write(self.sk['0'].to_pem())
            with open(str(self.path)+"/public.pem", 'wb') as f:
                f.write(self.vk['0'].to_pem())
        else:
            with open(str(self.path)+"/private.pem", 'rb') as f:
                self.sk['0'] = SigningKey.from_pem(f.read())
            self.vk['0'] = createPublicKey(self.sk['0'])

        self.addr['0'], _ = createAddr(self.vk['0'])
        self.key_nums = len(self.sk)

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
        self.key_nums = len(self.sk)

    def load(self):
        pass

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
