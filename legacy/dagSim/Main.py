import MainNet
import TradePool
import Params
import traceback
import Dag
import time

MaxCountdown = 99999

class Main:
    def __init__(self):
        pass

    def run(self, nParents=None): 
        self.mainNet = MainNet.MainNet(nParents)
        fileSuffix = ''
        if nParents:
            fileSuffix += '_np{0}'.format(nParents)
            self.mainNet.setNParents(nParents)
        else:
            fileSuffix += '_m2m2m'

        T = 0 # global timeline
        elapsed = 5 # elapsed time (unit : 5)

        # schedule
        schedule = {}

 
        confCycle = Params.tConfCycle
        simtime = Params.tSimtime

        # initial tx incoming
        newTx = TradePool.getTx()
        schedule[newTx.issuedTime] = newTx
        schedule[confCycle] = 'Confirmation'
        print'Simulation started'
        try:            
            while T < simtime:
                
                # make curve of tx rate
                if T > elapsed:
                    if T < simtime / 2: # up phase
                        Params.rTxRate += 5
                    else:
                        Params.rTxRate -= 5
                    elapsed += 5

                # print [round(t,2) for t in schedule.keys()]
                T = min([c for c in schedule.keys() if c > T])                
                if schedule[T] == 'Confirmation':
                    # time to do confirmation
                    print'[{0}] Confirmation in process..'.format(T)                
                    confirmedTx, warned = self.mainNet.confTx()
                    for tx in [TradePool.Pool[c] for c in confirmedTx]:
                        tx.status = 3
                        tx.tConfm = T - tx.tBroad
                        self.mainNet.nodes[tx.assignedNode].addContime(tx.tConfm)
                    schedule[T + confCycle] = 'Confirmation'                    
                    continue

                tx = schedule[T]
                if tx.status == 0: # incoming
                    # new Tx arrived -- start validation
                    # print'[{0}] tx Request ({1}) arrived : {2}, Validation starts'.format(T, tx.index, tx)
                        
                    # start validation
                    self.mainNet.valTx(tx)
                    self.mainNet.nodes[tx.assignedNode].addValtime(tx.tValid)
                    schedule[T + tx.tValid] = tx                    
                    
                    # depart next transaction
                    newTx = TradePool.getTx() # get next Tx event                
                    schedule[T + newTx.issuedTime] = newTx

                elif tx.status == -1:
                    # validation done -- do not attach to the assigned node's dag                
                    # print'[{0}] tx Validation ({1}) done -- INVALID'.format(T, tx.index)
                    pass

                elif tx.status == 1:
                    # validation done -- attach to the assigned node's dag
                    # print'[{0}] tx Validation ({1}) done -- VALID'.format(T, tx.index)
                    self.mainNet.nodes[tx.assignedNode].dag.attach(tx)
                    tx.status = 2

                    # get fee
                    self.mainNet.incomes[tx.assignedNode] += tx.fee

                    # start propagation
                    broadTime = self.mainNet.getBroadTime()
                    tx.tBroad = T + broadTime
                    schedule[T + broadTime] = tx

                elif tx.status == 2:
                    # propagation done -- waiting for confirmation
                    # print'[{0}] tx Propagation ({1}) done'.format(T, tx.index)
                    self.mainNet.broadTx(tx)
        except:
            traceback.print_exc()
            pass

        # statistics
        confirmedTxs = [tx for tx in TradePool.Pool.values() if tx.status == 3]
        s = self.mainNet.nodes[0].showDag('dagLog' + fileSuffix + '.txt')
        if s == len(self.mainNet.nodes[0].dag.txs.keys()):
            print 'dag scan : valid'

        with open('txLog' + fileSuffix + '.txt','w') as f:
            [f.write(tx.showResult()) for tx in TradePool.Pool.values() if tx.tConfm != 0]

        print 'Total Txs gen :',len(TradePool.Pool)
        print 'Node 0 dag size :',len(self.mainNet.nodes[0].dag.txs)
        if confirmedTxs:
            val_avg = sum([tx.tValid for tx in confirmedTxs]) / len(confirmedTxs)
            conf_avg = sum([tx.tConfm for tx in confirmedTxs]) / len(confirmedTxs)
            print 'Confirmed Txs :',len(confirmedTxs)
            print 'validation time avg. :',val_avg
            print 'confirmation time avg. :',conf_avg
            print 'nodes income :',self.mainNet.incomes
        else:
            print 'There is no confirmed Txs!'

        print 'reserved :',Dag.ResCount

        # reset
        TradePool.Pool = {}
        Dag.Tx.Reset()

if __name__ == '__main__':
    m = Main()
    m.run(2)
    m.run(3)
    m.run(4)
    m.run()