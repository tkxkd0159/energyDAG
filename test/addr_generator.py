from kudag.crypto import createAddr, createPrivateKey, createPublicKey
from secrets import token_hex


if __name__ == "__main__":
    mypvt = createPrivateKey(token_hex(32))
    mypub = createPublicKey(mypvt)
    myaddr, pubhash = createAddr(mypub)
    print(myaddr)
