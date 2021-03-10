import os
import plyvel

# os.environ['P2P_PORT'] = '6001'

P2P_PORT = os.getenv('P2P_PORT') if os.getenv('P2P_PORT') is not None else 6001
db = plyvel.DB('/tmp/testdb/', create_if_missing=True)
print(db)