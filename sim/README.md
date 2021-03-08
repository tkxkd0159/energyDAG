# Energy TX Platform
<!-- 
TODO
*
!
?
// @param
 -->

## Properties
fp / tn : false positive / true negative
confl : conflict  
conf : confirmed  
prts : parents (target of validation)  
clds : childs (childs of TX)  
`t_arriv` : arriv time  
`t_vldd` : validation done time  
`t_conf` : confirmed time  
`t_deact` : deactivated time  

### Sim (class)
```
events = {event_time: Event()}
txs = {tx.index: Tx()}
```
### GUI (class)
```
```

## legacy
```python
Cp = 5 # Conf. cycle, avg. seconds
Cq = 0.5 # Conf. cycle, std. seconds
nP       #  (power-lines)
MAX_KW = 50 # per power line
LR_ATK = False  # long-range attack


# S = [power(i) for i in range(nS)]
# A = [ami(i) for i in range(nA)]
# sigma = getSigma(nS, nA) # power-loss matrix

Sp = 10             # sigma, avg. percentage
Sq = 3              # sigma, std. percentage
def getSigma(nS, nA):
	sigma = list()
	for i in range(0, nS):
		sigma_row = list()
		for j in range(0, nA):
			sigma_row.append(random.gauss(Sp, Sq))
		sigma.append(sigma_row)
	print 'sigma matrix obtained'
	return sigma
```