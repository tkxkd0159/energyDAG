from Dag import Dag
import Params
import random

class Node:
    def __init__(self, index):
        self.dag = Dag()
        self.nParents = None
        self.index = index

        self.valtimes = []
        self.contimes = []

        self.fp = {random.uniform(3,6) : 4,
                   random.uniform(6,10) : 3,
                   random.uniform(10,15) : 2,
                   random.uniform(15,30) : 1}

    def addValtime(self, tValid):
        self.valtimes.append(tValid)
        if len(self.valtimes) > Params.cTimesAvg:
            self.valtimes.pop(0)

    def addContime(self, tConfm):        
        self.contimes.append(tConfm)        
        if len(self.contimes) > Params.cTimesAvg:
            self.contimes.pop(0)

    def getAvgValtime(self):
        if self.valtimes:
            return sum(self.valtimes) / len(self.valtimes)
        else:
            return -1

    def getAvgContime(self):
        if self.contimes:            
            return sum(self.contimes) / len(self.contimes)
        else:
            return -1

    def valTx(self, tx):
        terms = self.dag.getTerms()
        if not self.nParents:
            np = self.fp[tx.fee]
        else:
            np = self.nParents
        tx.parents = random.sample(terms, min(np, len(terms)))
        tx.nParents = len(tx.parents)
        self.isValid(tx)

    def isValid(self, root): # calc balance of the tree(tx)                
        B = dict() # balances -- [{User} : {balance}]
        B[root.contents[0]] = -root.contents[2]
        B[root.contents[1]] = root.contents[2]        

        T = self.getTree(root)
        for iTx in T:
            if not iTx in self.dag.txs.keys():
                continue
            tx = self.dag[iTx]
            if not tx.contents: #reference
                continue
            if tx.status == 3:
                continue
            s,r,a = tx.contents # sender(s), receiver(r), amount(a)
            if s in B.keys(): B[s] -= a
            else: B[s] = -a
            if r in B.keys(): B[r] += a
            else: B[r] = a

        # calc validation overhead
        vtAvg = Params.tUnitVal * len(T)
        vtStd = (Params.tUnitValVar * len(T)) ** 0.5
        valTime = random.gauss(vtAvg, vtStd) + Params.tPow        
        root.tValid = valTime        
        # print 'Node::isValid():: {0} Tx balance is measured for {1} secs'.format(len(T), valTime)

        for (u,b) in B.items(): # (User, Balance) pair            
            if Params.amounts[u] + b < 0: # negative balance : invalid
                # print 'Node::isValid():: Invalid balance found -- result {0} at trader {1}'.format(b,u)
                root.status = -1
        root.status = 1

    # return should be the set of <<indices>>
    def doConf(self):        
        terms = self.dag.getTerms()[0:Params.nMaxConfTerms] # index of terminals
        lTerms = float(len(terms))
        threshold = len(terms) * Params.rConfTh
        confStatus = dict()

        for term in self.dag.getAll(terms): # term : Tx (not indices)
            for tx in self.getTree(term): # set of tx.index
                if tx in confStatus.keys():
                    confStatus[tx] += 1
                else:
                    confStatus[tx] = 1

        # for debug
        # self.showDag()
        # print '\n'.join(['{0} : {1}%'.format(k,v/lTerms*100) for (k,v) in confStatus.items()])

        # get confirmed
        confirmed = [k for (k,v) in confStatus.items() if v >= threshold]
        confirmed = confirmed[:Params.nMaxConfVertices]
        for tx in self.dag.getAll(confirmed):
            tx.status = 3 # confirmed
        return confirmed

    # getTree() inputs Tx, and output Tx (not indices!)
    def getTree(self, root):        
        queue = [root]
        tree = set()
        while queue:            
            v = queue.pop(0)                        
            if (v.parents) and (v.status != 3) and (v.index not in tree):
                tree.add(v.index)                
                # print '[{0}] --> {1}'.format(v.index, v.parents)
                queue += self.dag.getAll(v.parents)            
        return tree

    def showDag(self, filename):
        f = open(filename,'w')
        d = 0
        s = 0
        while True:
            gens = [tx for tx in self.dag.txs.values() if tx.depth == d]
            if not gens:
                break
            print d,'depth :',len(gens)
            f.write('{0}\t{1}\n'.format(d, len(gens)))
            d += 1
            s += len(gens)
        f.close()
        return s

        # queue = self.dag.getAll(range(4))        
        # lens = [4]
        # lev = 0        
        # while True:            
        #     genStr = '<<'
        #     nextGen = set()
        #     print '[level {0} -- {1} vertices]'.format(lev,len(queue))
        #     f.write('{0}\t{1}\n'.format(lev, len(queue)))
        #     while queue:                
        #         tx = queue.pop(0)                
        #         [nextGen.add(c) for c in tx.childs]                
        #         # pStr = 'G' if not tx.parents else ','.join(map(str, tx.parents))
        #         cStr = 'T' if not tx.childs else ','.join(map(str, tx.childs))
        #         genStr += '{0}({1})'.format(tx.index, cStr).rjust(15)
        #     genStr += '>>'
        #     # print genStr
        #     if not nextGen: break
        #     queue = self.dag.getAll(nextGen)
        #     lens.append(len(queue))
        #     lev += 1        
        # f.close()
        # return sum(lens) / float(len(lens))