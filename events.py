import random
from vars import*

class event:
	def do(self, sim):
		raise NotImplemented

# txIncome : when tx arrives
class txIncome(event):
	def __init__(self, tx):
		self.tx = tx

	def do(self, sim):
		tx = self.tx		
		m = tx.miner

		sim.log('TX incoming', '<{0}> sent to miner {1}'.format(tx.index, m.index))

		# if not m.txqueue:
		# 	sim.events[sim.t] = valStarts(tx) # start validation now
		# else:
		# 	m.txqueue.append(tx)

		sim.events[sim.t] = valStarts(tx) # start validation now, without queueing

# txValidate : when miner starts validation
class valStarts(event):
	def __init__(self, tx):
		self.tx = tx

	def do(self, sim):
		tx = self.tx
		m = tx.miner
		valResult = m.validate(tx, sim.t) # validation done time

		# validation fail
		if valResult == None: 
			tReval = sim.t + ReValidationInterval
			sim.events[tReval] = valStarts(tx)
		# validation success
		else:
			# print valResult
			pts, vlt = valResult
			tValEnd = sim.t + vlt
			sim.log('Validation', '{0:4} --> {1}, takes {2}'.format(tx.index, [pt.index for pt in tx.pts], vlt))

			if sim.style != 'BKCN': # Blockchain's validation time is different
				tx.vlt = tValEnd # tx validation done time
			sim.events[tValEnd + sim.bct] = txBroadcast(tx) # schedule

			# # start next validation for queued tx
			# if m.txqueue:
			# 	sim.events[sim.t + vlt] = valStarts(m.txqueue.pop(0))

class txBroadcast(event):
	def __init__(self, tx):
		self.tx = tx

	def do(self, sim):
		tx = self.tx
		m = tx.miner
		sim.log('Broadcasted', tx.index)
		for miner in sim.miners:
			if miner == m: continue
			miner.addTx(tx)

class confirm(event):
	def __init__(self, m):
		self.m = m

	def do(self, sim):
		m = self.m
		confTxs = m.confirm(sim.t)
		word = 'miner {0:4} : {1:4} txs confirmed'.format(m.index, 'no' if not confTxs else len(confTxs))
		sim.log('Confirmed', word)
		if not confTxs: return
		for confTx in confTxs:
			tx = sim.txs[confTx]
			if tx.confirmed: # duplicated confirmation (for debugging)
				raise Exception
			tx.confirmed = True
			tx.cft = sim.t

class blockGen(event): # blockchain block generation
	def __init__(self, m):
		self.m = m

	def do(self, sim):
		m = self.m # block generating miner
		validated = set(m.chain.valTxs) # deep copy
		for tx in validated:
			tx.vlt = sim.t
		for om in sim.miners:
			om.chain.valTxs -= validated
			om.chain.valTxs |= om.chain.newTxs
			om.chain.newTxs = set()
			om.chain.blocks.append(validated)		
		if len(m.chain.blocks) >= 6:
			for tx in m.chain.blocks[-6]:
				tx.cft = sim.t		