from math import sqrt, exp
from random import sample

# =======================  Miner ===================== #
t_pow = 0.1 # seconds
t_val = 0.001 # seconds

CONFIRM_TRUSTY = 1
INVLD_TRUSTY = -1
GENESIS_NUM = 4         # number of genesis(reference) txs

# ==================================================== #

class Tx:
    """Transaction instance

    assign miners on this intance
    """
    def __init__(self, t_arriv, idx, is_conf=False):
        self.idx = idx
        self.miner = None

        self.t_arriv = t_arriv
        self.t_vldd = 0
        self.t_conf = 0
        self.t_deact = 0

        self.depth = 0
        self.prts = set()
        self.clds = set()
        self.is_conf = is_conf
        self.is_deact = False

        # Double spending
        self.confl_tx = None
        self.is_confl = False
        self.trusty = 0
        self.good = 0
        self.bad = 0
        self.fp = 0

    def reset(self):
        self.miner = None
        self.t_vldd = 0
        self.t_conf = 0
        self.t_deact = 0
        self.depth = 0
        self.prts = set()
        self.clds = set()
        self.is_conf = False if self.index >= 0 else True
        self.is_deact = False
        self.trusty = 0
        self.good = 0
        self.bad = 0
        self.fp = 0


    def set_miner(self, miner):
        self.miner = miner

class DAG:
    """DAG instance
    """
    def __init__(self):
        self.txs = dict()

    def __get_childs(self, tx: Tx):
        return [child for child in tx.clds if child.idx in self.txs]

    def get_tips(self):
        return [tx for tx in self.txs.values() if (not self.__get_childs(tx))]

    def get_not_conf_tx(self):
        """get unconfirmed transactions except for the tips
        """
        return [tx for tx in self.txs.values() if (self.__get_childs(tx)) and (tx.is_conf == False) and (tx.is_deact == False)]

    def sel_prts(self, n_prt) -> list:
        if len(self.get_tips()) < n_prt:
            return self.get_tips()
        else:
            return sample(self.get_tips(), n_prt)


    def get_anc(self, prt: Tx) -> set:
        """Ancestor
        """
        total_anc = set([prt])
        curr_tgt = set([prt])
        next_tgt = set()

        while True:
            for prt in curr_tgt:
                for gprt in prt.prts:
                    if gprt.idx not in self.txs:
                        continue
                    if gprt.idx < 0:
                        continue
                    next_tgt.add(gprt)

            if not next_tgt:
                break
            total_anc |= next_tgt
            curr_tgt = set(next_tgt)
            next_tgt = set()

        total_anc = set([anc for anc in total_anc if (not anc.is_conf or anc.idx < 0) and not anc.is_deact])

        return total_anc

class Miner:
    """Miner instance

    It's a miner in the DAG-based ledger.
    Miner have their own DAG instance
    """
    def __init__(self, index: int, style: str):
        self.idx = index
        self.style = style  # PowerGraph

        self.dag = DAG()
        self.tx_queue = []

    def add_tx(self, tx: Tx):
        self.dag.txs[tx.idx] = tx

    def set_genesis(self, txs: dict, GENESIS_NUM):
        for i in range(-GENESIS_NUM, 0):
            self.dag.txs[i] = txs[i]

    def validate(self, tx: Tx, event_time) -> tuple[list[Tx], float]:
        """New TX validate DAG's tip
        ----------------------------
        Tips are the parent of new TX.
        Assign new TX's parents(DAG's tips)
        """
        t = event_time
        m = tx.miner

        n_prt = max(2, int(sqrt(max(1.0, float(len(m.dag.get_tips()))))))
        prts = m.dag.sel_prts(n_prt)
        tx.depth = min([prt.depth for prt in prts]) + 1

        # Add parents and childs to the TX
        tx.prts = prts
        for prt in prts:
            prt.clds.add(tx)

        anc_of_tip = set()
        for prt in prts:
            anc_of_tip.update(m.dag.get_anc(prt))

        A = float(len(anc_of_tip))
        N = max(A+1, float(len(m.dag.get_not_conf_tx())))

        fp = min(0.49, 2 * A * (N - A) / (N * (N - 1)))
        tn = (A ** 2 - A) / (N ** 2 - N)

        t_work = A * t_val + t_pow

        is_vld = True
        confl_tx_ls = []
        anc_with_confl = [anc for anc in anc_of_tip if anc.confl_tx]
        for anc in anc_with_confl:
            if anc.confl_tx in anc_of_tip:
                is_vld = False
                anc.trusty -= tn * A / N
                anc.bad += 1
                if anc.trusty < INVLD_TRUSTY:
                    anc.t_deact = t + t_work
                    anc.is_deact = True
                confl_tx_ls.append(anc)

        if is_vld:
            for anc in anc_of_tip:
                anc.fp = fp
                diff_depth = tx.depth - anc.depth
                anc.trusty += (0.5 - fp) * exp(diff_depth - 8)
                anc.good += 1
                if anc.trusty > CONFIRM_TRUSTY:
                    anc.t_conf = t + t_work
                    anc.is_conf = True

        m.dag.txs[tx.idx] = tx
        return (prts ,t_work)