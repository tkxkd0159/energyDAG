## params ##
nNodes = 5
nTraders = 2000
nGenesis = 4
nAddresses = nTraders
nMaxConfTerms = 100
nMaxConfVertices = 35

tSimtime = 100 # sec
tPow = 0.00 # sec
tNodeNetwork = 0.2 # sec
tHttpRequest = 0.2 # sec
tUnitVal = 0.003 # sec
tUnitValVar = 10 ** -7 # sec
tConfCycle = 1.0 # sec
tBroad = 0.01 # sec

rTxRate = 50 # 
rConfTh = 0.8

amounts = [500] * nTraders # a 'confirmed' amounts

cTimesAvg = 20

### desired results at ###
# r : 50
# unit : 0.003
# conf cycle : 1.0