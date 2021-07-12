from ecdsa import SigningKey, VerifyingKey, BadSignatureError, NIST192p
from ecdsa.util import randrange_from_seed__trytryagain


sk = SigningKey.generate() # uses NIST192p
vk = sk.verifying_key

mysig = sk.sign(b"LJS")
with open('sk.der', 'wb') as f:
    f.write(sk.to_der())

with open('vk.der', 'wb') as f:
    f.write(vk.to_der())

with open('mysig', 'wb') as f:
    f.write(mysig)

with open('sk.der', 'rb') as f:
    sk2 = SigningKey.from_der(f.read())
with open('vk.der', 'rb') as f:
    vk2 = VerifyingKey.from_der(f.read())
with open('mysig', 'rb') as f:
    loaded_sig = f.read()

try:
    vk2.verify(loaded_sig, b"LJS")
    print("Success verification")

except BadSignatureError as e:
    print(f'{e}, Signature and public key do not match.')


def make_key_from_seed(seed, curve=NIST192p):
    secexp = randrange_from_seed__trytryagain(seed, curve.order)
    return SigningKey.from_secret_exponent(secexp, curve)

try:
    base_seed = "LJS"
    sk_list = []
    for i in range(1, 4):
        new_seed = f'{base_seed}:{i}'
        sk_list.append(make_key_from_seed(new_seed))

    assert sk_list[0] != sk_list[1]
    assert sk_list[0] != sk_list[2]

except AssertionError:
    print("Same seed makes same private key")
