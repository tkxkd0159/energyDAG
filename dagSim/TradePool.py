import math
import random
import Dag

from Params import nTraders, nNodes, nAddresses, rTxRate, amounts

Pool = {}

def getTx():
    # print amounts
    tx = Dag.Tx(getTA(), getTC(), getTN())
    Pool[tx.index] = tx
    return tx

# TA : Transaction arrival time
def getTA():
    l = rTxRate
    # p = random.uniform(0.0, l)
    # return (-l * math.log(p * l)) # poisson
    p = random.random()
    return math.log(1-p) / (-l)

# TC : Transaction's contents
def getTC():
    # good one
    AvSenders = [i for i in range(nAddresses) if amounts[i] > 0]
    sender = random.sample(AvSenders, 1)[0]
    AvReceivers = [i for i in range(nAddresses) if i != sender]
    receiver = random.sample(AvReceivers, 1)[0]

    amount = random.randrange(1, amounts[sender]/5)
    return [sender, receiver, amount]

    # bad one ## TODO

# TN : Transaction issuing node
def getTN():
    return random.randrange(0, nNodes)

def execute(txIndex):
    s,r,a = Pool[txIndex].contents
    amounts[s] -= a
    amounts[r] += a
    # print 'Tx ({0}) executed -- {1}'.format(txIndex, str(Pool[txIndex]))