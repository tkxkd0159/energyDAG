from kudag.crypto import createPrivateKey
from kudag.dag import TX
import json

if __name__ == "__main__":
    print(createPrivateKey())
    print(json.dumps(TX().serialize()))
    print(type(TX().hash().digest().hex()))

