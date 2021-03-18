# The elliptic curve domain parameters over Fp associated with a Koblitz curve secp256k1
# are specified by the sextuple T = (p,a,b,G,n,h) where the finite field Fp
# The curve E: y^2 = x^3 + ax + b over Fp, a = 0, b = 7
# base point G = 04 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8
# the order n of G, n = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141
# cofactor h = 01
# * secp256k1 : y^2 = x^3 + 7

from secrets import token_hex
from binascii import b2a_hex

from typing import Union
from os import urandom
from functools import reduce, lru_cache
from hashlib import sha256, sha3_256, blake2s
from ecdsa import SigningKey, VerifyingKey, SECP256k1

from param import BITCOIN_ALPHABET



def createPrivateKey():
    return SigningKey.generate(curve=SECP256k1)

def createPublicKey(pvtK: SigningKey):
    return pvtK.verifying_key


def createAddr(pubK: VerifyingKey):
    hash1 = sha3_256()
    hash1.update(pubK.to_string())
    hash2 = blake2s(digest_size=16, salt=urandom(8))
    hash2.update(hash1.digest())
    return hash2.hexdigest()

def sha256ForTx(*args: str) -> str:
    res = reduce(lambda acc, cur: acc+cur, args)
    hash = sha3_256()
    hash.update(res.encode())
    return hash.hexdigest()


def b58encode(v: Union[str, bytes, int], char_set: bytes = BITCOIN_ALPHABET) -> bytes:
    if isinstance(v, str):
        v = v.encode()

    if isinstance(v, bytes):
        origlen = len(v)
        v = v.lstrip(b'\0')
        newlen = len(v)
        pad_len = origlen - newlen
    else:
        pad_len = 0

    decimal = int.from_bytes(v, byteorder='big')  # first byte is MSB
    if decimal == 0:
        return char_set[0:1]
    output = b""
    while decimal:
        decimal, idx = divmod(decimal, 58)
        output = char_set[idx:idx+1] + output

    return char_set[0:1] * pad_len + output

def b58decode(v: Union[str, bytes, int], char_set: bytes = BITCOIN_ALPHABET) -> bytes:
    if not isinstance(v, int):
        v = v.rstrip()
    if isinstance(v, str):
        v = v.encode()
    if isinstance(v, bytes):
        origlen = len(v)
        v = v.lstrip(char_set[0:1])
        newlen = len(v)
        pad_len = origlen - newlen
    else:
        pad_len = 0

    map = _get_base58_decode_map(char_set)
    decimal = 0
    try:
        for char in v:
            decimal = decimal * 58 + map[char]
    except KeyError as e:
        raise ValueError("Invalid char <{0}>".format(chr(e.args[0])))

    output = []
    while decimal > 0:
        decimal, remain = divmod(decimal, 256)   # mod 256 to convert int into bytes
        output.append(remain)

    return b'\0' * pad_len + bytes(reversed(output))


def b58encodeWithChecksum(v: Union[str, bytes, int], char_set: bytes = BITCOIN_ALPHABET) -> bytes:
    """
    Encode a string using Base58 with a 4 character checksum
    """
    if isinstance(v, str):
        v = v.encode()

    digest = sha256(sha256(v).digest()).digest()
    return b58encode(v + digest[:4], char_set=char_set)


def b58decodeWithChecksum(v: Union[str, bytes, int], char_set: bytes = BITCOIN_ALPHABET) -> bytes:
    """
    Decode and verify the checksum of a Base58 encoded string
    """

    result = b58decode(v, char_set=char_set)
    result, check = result[:-4], result[-4:]
    digest = sha256(sha256(result).digest()).digest()

    if check != digest[:4]:
        raise ValueError("Invalid checksum")

    return result


@lru_cache()
def _get_base58_decode_map(char_set: bytes) -> dict[int, int]:
    try:
        map = {char: index for index, char in enumerate(char_set)}

        groups = [b'0O', b'Il']
        for group in groups:
            for element in group:
                if element in map:
                    raise Exception("ERROR: The char_set is not valid")

        return map
    except Exception as e:
        print(e)
