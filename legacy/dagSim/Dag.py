import Params
import copy
import random

ResCount = 0

class Dag:
    def __init__(self):
        self.txs = dict() # {tx.index} : {Tx}
        for i in range(Params.nGenesis):
            self.txs[i] = Tx.Genesis(i)

    def __getitem__(self, i):        
        return self.txs[i]

    ####################################################
    ## getSth() funcs all returns list of <<indices>> ##
    ####################################################

    def getTerms(self): # get Txs that do not have children
        return [tx.index for tx in self.txs.values() if not tx.childs]
    
    def getUnconfirmed(self): # get Txs that awaiting confirmation
        return [tx.index for tx in self.txs.values() if tx.status == 2]

    def attach(self, iTx): # input tx (not index)        
        global ResCount
        tx = Tx.Clone(iTx)

        self.txs[tx.index] = tx

        for p in tx.parents:
            if p in self.txs.keys():
                self.txs[p].childs.append(tx.index)
            else:
                self.txs[p] = Tx.Reserved(tx.index)
                print 'reservation occured'                
                ResCount += 1
                self.txs[p].childs.append(tx.index)
        # get depth
        tx.depth = max([self.txs[p].depth for p in tx.parents]) + 1

        # print 'Tx',tx,'attached'
    def indices(self, txs):
        return [tx.index for tx in txs]

    def getAll(self, iTxs):
        return [self.txs[i] for i in iTxs]

    def ls(self):
        return [tx.index for tx in self.txs]

TxCounter = Params.nGenesis

class Tx:    
    @staticmethod
    def Genesis(index):
        return Tx(0, [], -1, index)

    @staticmethod
    def Reserved(index):
        return Tx(0, [], -1, index)

    @staticmethod
    def Reset():
        global TxCounter
        TxCounter = Params.nGenesis
        print 'Tx counter set to',TxCounter

    @staticmethod
    def Clone(tx):
        return copy.deepcopy(tx)

    def __init__(self, issuedTime, contents, assignedNode, index=None):
        global TxCounter
        # contents : [{Sender}, {Receiver}, {Amount}] -- general transaction
        #            [{address}, {balance}] -- reference block
        self.issuedTime = issuedTime
        self.contents = contents
        self.assignedNode = assignedNode        

        self.nParents = None
        self.parents = None
        self.childs = []
        if index != None: # pre-designated index: used for genesis
            self.index = index
        else:
            self.index = TxCounter # replaces 'Hash' of the Tx
            TxCounter += 1

        self.status = 0 # 0 for incoming, 1 for validating, 2 for confirmation awaiting, 3 for confirmed

        self.tIssue = 0 # differ from issuedTime
        self.tValid = 0
        self.tBroad = 0
        self.tConfm = 0

        self.depth = 0

        # condition
        self.fee = 1 # init desig
        self.minFee = random.choice([True, False]) # minimum Fee or shortest T

    def __str__(self):
        if not self.contents:
            return '<Genesis>'
        else:
            return '[{0} --({1})--> {2}], by Node {3}'.format(self.contents[0], self.contents[2], self.contents[1], self.assignedNode)

    def showResult(self):
        # print '[{0}] : | tValid [{1}] | tConfm [{2}] |'.format(self.index, self.tValid, self.tConfm)
        return '{0}\t{1}\t{2}\n'.format(self.index, self.tValid, self.tConfm)