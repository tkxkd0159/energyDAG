import random
import os

from component import Tx, Miner, GENESIS_NUM
from gui import GUI


VERBOSE = False      # debug
GUIon = False


RUN_TIME = 5        # seconds
TX_CYCLE = 0.5      # transaction issuance cycle (seconds)
ALERT_INTVL = 50    # '~seconds passed' alert cycle (seconds)
REVLD_INTVL = 3 # Revalidational interval (seconds)

# arrival set
UNI_START = 0
UNI_END = 1
POI_MEAN = 10
CONST_TIME = 1



if GUIon:
    gui = GUI()

class Event:
    def __init__(self):
        pass
    def do(self, sim: object):
        raise NotImplementedError

class Sim:
    """Simulation Instance

    Parameters
    ----------
    rap : Race attack probability
    rap_itv : Race attack interval
    lra (bool): Long range attack
    bc_delay : Broadcasting delay
    """
    def __init__(self, rap=0.5, rap_itv=0.0001, lra=False, bc_delay=0.5):

        self.rap = rap
        self.rap_itv = rap_itv
        self.__lra = lra
        self.bc_delay = bc_delay  # 나중에 node 개수 고려해서 필요

        self.events = dict()
        self.txs = dict()

    def gen_tx(self, arriv_type="poisson", start: float=None, end: float=None):
        if start is not None:
            t_arriv = start
        else:
            t_arriv = 0
        if end is None:
            end = RUN_TIME
        tx_idx = 0
        tx_invld_cnt = 0

        arriv_dist = {
            "poisson": random.expovariate(POI_MEAN),
            "uniform": random.uniform(UNI_START, UNI_END),
            "const": CONST_TIME
        }

        self.txs = {g_idx: Tx(0, g_idx, is_conf=True) for g_idx in range(-GENESIS_NUM, 0)} #generate genesis

        while t_arriv < end:
            t_arriv += arriv_dist.get(arriv_type)
            ntx = Tx(t_arriv, tx_idx)
            self.txs[tx_idx] = ntx
            tx_idx += 1


            if random.random() < self.rap:   # race attack
                ntx_invld = Tx(t_arriv + self.rap_itv, tx_idx)
                ntx_invld.confl_tx = ntx
                ntx.is_confl = True
                self.txs[tx_idx] = ntx_invld
                tx_idx += 1
                tx_invld_cnt += 1

        if VERBOSE:
            print("****gen_tx debug****")
            print(f'Stacked TX: {tx_idx} Invalid TX: {tx_invld_cnt}')


    def log(self, event_name, suffix=''):
        if VERBOSE:
            print(f'{self.time_cursor:.3f}|{event_name:^15}|{suffix:^20}')

    def run(self, style, miner_num, tx_reuse=False, folder='.', suffix=''):

        if not os.path.exists('results_new/' + folder):
            os.makedirs('results_new/' + folder)
        file_name = f'{folder}/m{miner_num}_{style}{suffix}'

        self.miners = [Miner(i, style) for i in range(miner_num)]

        if tx_reuse:
            [tx.reset() for tx in self.txs.values]
        else:
            self.gen_tx()

        # set genesis into miner's DAG and assign tx's arrivals to miners
        [miner.set_genesis(self.txs, GENESIS_NUM) for miner in self.miners]
        [tx.set_miner(random.choice(self.miners)) for tx in self.txs.values()]

        # pre-schedule tx arrivals
        self.events.update({tx.t_arriv:self.TxArriv(tx) for tx in self.txs.values() if tx.idx >= 0})

        print(f'Simulation begin : results_new/{file_name}')
        t_alert = ALERT_INTVL
        self.time_cursor = 0


        while True:
            if self.time_cursor > t_alert:
                print(f'{t_alert} secs passed')
                t_alert += ALERT_INTVL
            self.time_cursor = min(self.events.keys())
            if self.time_cursor > RUN_TIME:
                break

            deque_event = self.events.pop(self.time_cursor)
            deque_event.do(self)

            if GUIon:
                k = gui.show(self.miners[0], style, self.time_cursor) # miner 0's dag
                if k == 1: return
            if not self.events: break

        print("Writing...")
        with open(f'results_new/{file_name}.txt', 'w') as f:
            whole_log = []
            for tx in self.txs.values():
                if tx.idx <0: continue
                if not tx.confl_tx:
                    state = 0
                else:
                    state = tx.confl_tx.idx

                log = [tx.idx,
                        state,
                        round(tx.t_arriv, 4),
                        round(max(0, tx.t_vldd - tx.t_arriv), 4),
                        round(max(0, tx.t_conf - tx.t_arriv), 4),
                        round(max(0, tx.t_deact - tx.t_arriv), 4)]
                if style == "PWGR":
                    log.append(round(tx.trusty, 4))
                    log.append(tx.good)
                    log.append(tx.bad)
                    log.append(round(tx.fp, 4))
                whole_log.append('\t'.join(map(str, log)))
            f.write('\n'.join(whole_log))
        depth_cursor = 0
        width_info = []
        while True:
            same_depth_txs = [tx for tx in self.txs.values() if tx.depth == depth_cursor]
            if not same_depth_txs: break
            width_info.append(len(same_depth_txs))
            depth_cursor += 1
        with open(f'results_new/{file_name}_width.txt', 'w') as f:
            f.write('\n'.join(map(str, width_info)))

        print("Done")

        if GUIon:
            gui.kill()

    @property
    def lra(self):
        return self.__lra
    @lra.setter
    def lra(self, lra):
        if type(lra) != bool:
            raise TypeError("lra must be bool")
        self.__lra = lra

    class TxArriv(Event):
        """prescheduled TX arrival event
        """
        def __init__(self, tx: Tx):
            self.tx = tx

        def do(self, sim):
            m = self.tx.miner
            sim.log('TX arrival', f'<{self.tx.idx}> sent to miner {m}')
            sim.events[sim.time_cursor] = self.ValStart(self.tx)

        class TxBroadcast(Event):
            def __init__(self, tx: Tx):
                self.tx = tx

            def do(self, sim):
                m = self.tx.miner
                sim.log('Broadcasted', self.tx.idx)
                for miner in sim.miners:
                    if miner == m:
                        continue
                    miner.add_tx(self.tx)

        class ValStart(Event):
            def __init__(self, tx: Tx):
                self.tx = tx

            def do(self, sim):
                m = self.tx.miner
                vld_result = m.validate(self.tx, sim.time_cursor)

                prts, t_work = vld_result
                t_vldd = sim.time_cursor + t_work
                sim.log('Validation', f'{self.tx.idx} -> {[prt.idx for prt in self.tx.prts]}')
                self.tx.t_vldd = t_vldd
                sim.events[t_vldd + sim.bc_delay] = Sim.TxArriv.TxBroadcast(self.tx)






if __name__ == "__main__":
    s = Sim()
    s.run('PWGR', 10)