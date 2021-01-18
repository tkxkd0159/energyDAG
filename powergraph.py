import random
import time
import os
from math import sqrt
import random

from components import *
from vars import *
from analysis import *
from events import *
from miner import *
import gui

Vb = False # verbose
GuiOn = True # gui on
LongRangeAttack = False #

## simulation params
# nS : number of (sources)
# nA :           (AMIs)
# nM :           (miners)
# nP :           (power-lines)
# T : pre-generated transactions (for using same-scenario multiple times))
# tBc : broadcasting delay)
##

class sim:
	def __init__(self):
		self.rap = 0.0 # race attack probability
		self.rapTime = 0.0001 # race attack interval
		self.lra = False # long range attack enabled

		self.verbose = False

		self.bct = 0.5 # default broadcasting delay

		self.events = dict() # {event_time: event()}
		self.txs = dict() # {tx.index: tx()}

	def setRaceAttackProb(self, prob):
		self.rap = prob

	def log(self, eventname, words=''):
		if Vb:
			print '{0:4.3f}|{1:^15}|{2:^20}'.format(self.t, eventname, words)

	def run(self, style, m, p, txReuse=False, folder='.', kwadd=''):
		self.style = style
		self.m = m
		self.p = p

		if not os.path.exists('results2/'+folder):
			os.makedirs('results2/'+folder)
		kw = '{0}/m{1}p{2}_{3}{4}'.format(folder, m, p, style,kwadd) # keyword (used for displaying / file naming)

		# S = [power(i) for i in range(nS)]
		# A = [ami(i) for i in range(nA)]
		# sigma = getSigma(nS, nA) # power-loss matrix

		self.miners = [Miner(i, style) for i in range(m)]

		if txReuse: [tx.reset() for tx in self.txs.values()]
		else: self.genTx(style)

		# put genesis into miner's dag
		[m.setGenesis(self.txs, nGenesis) for m in self.miners]

		# assign tx's arrivals to miners
		[tx.setMiner(random.choice(self.miners)) for tx in self.txs.values()]

		# pre-schedule tx arrivals
		self.events.update({tx.int:txIncome(tx) for tx in self.txs.values() if tx.index >= 0})

		# pre-schedule confirmation schedule (IOTA, BKCN only)
		if style == 'IOTA':
			self.events.update(getIotaConfSchedules(self.miners[0]))
		elif style == 'BKCN':
			self.events.update(getBlockchainConfSchedules(self.miners))

		# calculate broadcasting delay
		# self.bct = m * tBc
		self.bct = 0.1

		# now begins
		print line, 'Simulation begins\n', kw, line
		alert = AlertInterval
		self.t = 0 # time cursor
		while True:
			if self.t > alert:
				print alert, 'secs..'
				alert += AlertInterval
			self.t = min(self.events.keys())
			e = self.events.pop(self.t)
			e.do(self)

			if GuiOn:
				k = gui.show(self.miners[0], style, self.t) # show miner 0's dag
				# k = gui.show(M[1]) # show miner 1's dag
				if k == 1: return
			if not self.events: break # no next event

		## result analysis
		print 'recording..'
		with open('results2/{0}.txt'.format(kw), 'w') as f:
			s = []
			for tx in self.txs.values():
				if tx.index < 0: continue # genesis
				state = 0 if not tx.conflicts else tx.conflicts.index
				ts = [tx.index,
					  state,
					  tx.int,
					  max(0, tx.vlt - tx.int),
					  max(0, tx.cft - tx.int),
					  max(0, tx.dat - tx.int)
					  ]
				if style == 'PWGR':
					ts.append(tx.trusty)
					ts.append(tx.good)
					ts.append(tx.bad)
					ts.append(tx.fp)
				s.append('\t'.join(map(str, ts)))
			f.write('\n'.join(s))

		d = 0
		ws = list()
		while True:
			sameDepths = [tx for tx in self.txs.values() if tx.depth == d]
			if not sameDepths: break
			ws.append(len(sameDepths))
			d += 1

		if style != 'BKCN':
			with open('results2/{0}_width.txt'.format(kw), 'w') as f:
				f.write('\n'.join(map(str, ws)))

		print 'Done!'
		# close gui
		if GuiOn:
			gui.kill()

	## tx generation - classic poisson style
	def genTx(self, style):
		p = self.p
		t = 0 # tx incoming time
		txi = 0 # tx index
		itxs = 0 # invalid txs (counter)

		# generate genesis
		self.txs = {gi: Tx(0, gi, confirmed=True) for gi in range(-nGenesis, 0)}

		while t < Runtime:
			t += random.expovariate(p)
			ntx = Tx(t, txi)
			self.txs[txi] = ntx
			txi += 1
			if style != 'IOTA' or t > Runtime * IOTADoubleSpendingStarts:
				# race attack
				if random.random() < self.rap:
					ntx2 = Tx(t + self.rapTime, txi)
					ntx2.conflicts = ntx
					ntx.conflicted = True
					self.txs[txi] = ntx2
					txi += 1
					itxs += 1
		print line
		print txi,'tx queued'
		print itxs, 'tx invalid'
		print line

	## tx generation by smart grid style
	def genTx_SG(self, style, nP): # nP : number of powerlines
		# generate genesis
		self.txs = {gi: Tx(0, gi, confirmed=True) for gi in range(-nGenesis, 0)}

		txi = 0
		itxs = 0
		for i in range(0, nP):
			# each powerline periodically generates tx
			start = random.uniform(0, Runtime)
			end = random.uniform(start, Runtime)
			t = start
			while t < end:
				ntx = Tx(t, txi)
				self.txs[txi] = ntx
				txi += 1
				if style != 'IOTA' or t > Runtime * IOTADoubleSpendingStarts:
					# race attack
					if random.random() < self.rap:
						ntx2 = Tx(t + self.rapTime, txi)
						ntx2.conflicts = ntx
						ntx.conflicted = True
						self.txs[txi] = ntx2
						itxs += 1
						txi += 1
				t += TxCycle
		print line
		print txi,'tx queued'
		print itxs, 'tx invalid'
		print line

def getSigma(nS, nA):
	sigma = list()
	for i in range(0, nS):
		sigma_row = list()
		for j in range(0, nA):
			sigma_row.append(random.gauss(Sp, Sq))
		sigma.append(sigma_row)
	print 'sigma matrix obtained'
	return sigma

def getIotaConfSchedules(m):
	cfis = dict()
	start = random.uniform(0, IotaConfCycle)
	while start < Runtime:
		cfis[start] = confirm(m)
		start += IotaConfCycle
	print len(cfis), 'IOTA conf. schedules queued'
	return cfis

def getBlockchainConfSchedules(M):
	cfis = dict()
	start = BlockchainConfCycle
	while start < Runtime:
		cfis[start] = blockGen(random.choice(M)) # one of miner generates block
		start += BlockchainConfCycle
	print len(cfis), 'Blockchain block generation schedules queued'
	return cfis

if __name__ == '__main__':
	s = sim()
	## style, nMiners, lambda

	# s.run('IOTA', 10, 5)
	# s.run('IOTA', 10, 10)

	# s.run('PWGR', 5, 10)
	# s.run('PWGR', 10, 10)
	s.run('PWGR', 10, 10)

	# run once
	# run('PWGR', 10, 50, 30, 4)
	# run('BKCN', 10, 50, 30, 40)

	# comp only
	# nP = 20
	# txs = genTx(nP, 'IOTA')
	# txs = genTx(nP)
	# run('PWGR', 10, 50, 30, nP=nP, txs=txs)
	# [tx.reset() for tx in txs]
	# run('IOTA', 10, 50, 30, nP=nP, txs=txs)
	# [tx.reset() for tx in txs]
	# run('BKCN', 10, 50, 30, nP=nP, txs=txs)

	# # varying traffic
	# s.setRaceAttackProb(0.0)
	# for l in range(30, 41):
	# 	s.run('PWGR', 20, l, folder='traffic_vary_noattack')
	# 	s.run('IOTA', 20, l, txReuse=True, folder='traffic_vary_noattack')
	# 	s.run('BKCN', 20, l, txReuse=True, folder='traffic_vary_noattack')

	# # varying network size
	# l = 10
	# for m in [5, 15, 25, 35, 40]:
	# 	s.run('PWGR', m, l, folder='network_vary')
	# 	s.run('IOTA', m, l, txReuse=True, folder='network_vary')
	# 	s.run('BKCN', m, l, txReuse=True, folder='network_vary')

	# # varying network delay
	# l = 20
	# bct = 1.0 # change from 0.1 to 1.0
	# while bct < 21.0:
	# 	s.bct = bct
	# 	s.run('PWGR', 20, l, folder='bct_vary20', kwadd='_bct{0}'.format(int(bct*1000)))
	# 	s.run('IOTA', 20, l, txReuse=True, folder='bct_vary20', kwadd='_bct{0}'.format(int(bct*1000)))
	# 	s.run('BKCN', 20, l, txReuse=True, folder='bct_vary20', kwadd='_bct{0}'.format(int(bct*1000)))
	# 	bct += 1.0

	# varying attack prob.
	# l = 10
	# for p in [0.0, 0.1, 0.2]:
	# 	s.setRaceAttackProb(p)
	# 	p_percent = str(int(p * 100))
		# s.run('PWGR', 20, l, folder='attack{0}%'.format(p_percent))
		# s.run('BKCN', 20, l, txReuse=True, folder='attack{0}%'.format(p_percent))
		# s.run('IOTA', 20, l, txReuse=True, folder='attack{0}%'.format(p_percent))

		# s.run('BKCN', 20, l, folder='attack{0}%'.format(p_percent))

	# # practical scenario - IEEE 16nodes
	# s.genTx_SG('IOTA', 50)
	# s.run('PWGR', 20, 20, txReuse=True, folder='IEEE16')
	# s.run('BKCN', 20, 20, txReuse=True, folder='IEEE16')
	# s.run('IOTA', 20, 20, txReuse=True, folder='IEEE16')

	# # practical scenario - EV charging station
	# s.genTx_SG('IOTA', 20)
	# s.run('PWGR', 20, 20, txReuse=True, folder='EVstation')
	# s.run('BKCN', 20, 20, txReuse=True, folder='EVstation')
	# s.run('IOTA', 20, 20, txReuse=True, folder='EVstation')