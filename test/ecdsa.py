from ecdsa import SigningKey, VerifyingKey, BadSignatureError


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
