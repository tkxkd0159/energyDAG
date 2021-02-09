Sp = 10 # sigma, avg. percentage
Sq = 3 # sigma, std. percentage
Cp = 5 # Conf. cycle, avg. seconds
Cq = 0.5 # Conf. cycle, std. seconds

Runtime = 5 # seconds
MaxkW = 50 # per power line
TxCycle = 0.5 # transaction issuance cycle (second)
AlertInterval = 50 # '~seconds passed' alert cycle (second)

# DAG-related
nGenesis = 4 # number of genesis(reference) txs

# PowerGraph
ConfirmTrusty = 1
InvalidTrusty = -1

# delays
tPoW = 0.1 # seconds
tVal = 0.001 # seconds
tBc = 0.1 # seconds

line = '\n' + ('=' * 20) + '\n'

# comparison
IotaConfCycle = 3 # secs
BlockchainConfCycle = 20 # secs

# IOTA
IOTAMaxValidationTrial = 10
ReValidationInterval = 3 # sec
IOTADoubleSpendingStarts = 0.2 # of total tx flows
ConfTh = 0.9 # threshold of confirmation
IOTATxTimeout = 30 # sec
IOTAMinTermsToConfirm = 20