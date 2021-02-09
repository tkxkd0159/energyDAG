import TradePool
import Params

T = 0

simtime = Params.tSimtime
confTime = 15
nextConfTime = confTime

txs = []

# 1st tx
tx = TradePool.getTx()
tx.tIssue = tx.issuedTime
txs.append(tx)
while T < simtime:    
    T += tx.issuedTime
    if T > nextConfTime:        
        for t in txs:
            t.tConfm = T - t.tIssue
        print '[{0}] {1} txs confirmed'.format(T, len(txs))
        txs = []
        nextConfTime += confTime
    tx = TradePool.getTx()
    tx.tIssue = T + tx.issuedTime
    txs.append(tx)


with open('txLog_bc.txt','w') as f:
    for t in TradePool.Pool.values():
        # print '{0}\t{1}\t{2}'.format(t.index, t.tIssue, t.tConfm)
        f.write('{0}\t{1}\t{2}\n'.format(t.index, t.tValid, t.tConfm))

