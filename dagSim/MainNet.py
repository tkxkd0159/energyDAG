from Node import Node
import Params
import TradePool
import random

class MainNet:
    def __init__(self, globalN):
        self.nodes = [Node(i) for i in range(Params.nNodes)]
        self.incomes = [0] * Params.nNodes
        self.globalN = globalN
        if globalN == 1:
            self.confAll = True
        else:
            self.confAll = False
    
    # about config #
    def setNParents(self, nParents):
        for n in self.nodes:
            n.nParents = nParents 

    def valTx(self, tx):        
        # decide which one to assign the node
        if not self.globalN:
            if tx.minFee:
                node, fee = self.getMinFee()
                tx.assignedNode = node
                tx.fee = fee
            else:
                node, fee = self.getFastest()
                tx.assignedNode = node
                tx.fee = fee

        return self.nodes[tx.assignedNode].valTx(tx)            


    def broadTx(self, tx):
        # attach tx except of assigned node
        for i in range(Params.nNodes):
            if i == tx.assignedNode: continue
            self.nodes[i].dag.attach(tx)

    def confTx(self):
        confirmed = random.choice(self.nodes).doConf()
        # if confirmed:
        #     print confirmed,'confirmed'
        print len(confirmed),'confirmed'
        warned = self.broadConfirm(confirmed)
        [TradePool.execute(tx) for tx in confirmed]
        return (confirmed, warned)

    def getBroadTime(self):
        # return len(self.nodes) * 0.5
        return Params.tBroad

    def broadConfirm(self, confirmed):
        for node in self.nodes:
            for tx in confirmed:
                if tx in node.dag.txs.keys():
                    node.dag[tx].status = 3

    def report(self, tx):
        n = tx.assignedNode
        v,c = tx.tValid, tx.tConfm
        self.nodes[n].record(v,c)

    def getMinFee(self):
        lowestFees = [n.fp.keys()[0] for n in self.nodes]
        minFee = min(lowestFees)
        node = lowestFees.index(minFee)
        return node, minFee

    def getFastest(self):
        Tspeed = [n.getAvgValtime() + n.getAvgContime() for n in self.nodes]
        fastest = min(Tspeed)
        node = Tspeed.index(fastest)
        return node, self.nodes[node].fp.keys()[-1]