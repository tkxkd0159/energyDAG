# pip install -e .
from kudag.param import PEERS
from kudag.network import deploy_ws_worker


try:
    for p in PEERS:
        deploy_ws_worker(p)
except:
    pass
