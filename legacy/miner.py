from components import*
from vars import*
import math

class Miner:
	def __init__(self, index, style):
		self.index = index
		self.style = style # IOTA / PowerGraph / Blockchain

		self.dag = dag() # IOTA, PowerGraph
		self.chain = chain() # BlockChain	
		self.txqueue = list() # tx queue

	def addTx(self, tx):
		if self.style == 'BKCN':
			self.chain.newTxs.add(tx)
		else:
			self.dag.txs[tx.index] = tx

	def setGenesis(self, txs, nGenesis):
		# genesis txs' index : -1 ~ -nG
		for i in range(-nGenesis, 0):
			self.dag.txs[i] = txs[i]

	def validate(self, tx, t):
		if self.style == 'PWGR':
			return self.validate_PowerGraph(tx, t)
		elif self.style == 'IOTA':
			return self.validate_IOTA(tx, t)
		elif self.style == 'BKCN':
			return self.validate_BlockChain(tx, t)

	def validate_PowerGraph(self, tx, t):
		m = tx.miner # miner

		T = max(1.0, float(len(m.dag.terms)))

		# select parents
		pts = m.dag.getPts_PowerGraph(T)
		tx.pts = pts
		# print tx.index,'has',len(pts),'parents'
		tx.depth = min([pt.depth for pt in pts]) + 1
		[pt.cds.add(tx) for pt in pts]

		# collect ancestors
		acs = set()
		[acs.update(m.dag.getAcs(pt)) for pt in pts]

		A = float(len(acs))
		N = max(A+1, float(len(m.dag.nterms)))

		fp = min(0.49, 2 * A * (N - A) / N / (N - 1))
		tn = (A * A - A) / (N * N - N)

		vlt = A * tVal + tPoW

		# validation
		valid = True
		detected = list()
		iacs = [ac for ac in acs if ac.conflicts]
		for iac in iacs:
			if iac.conflicts in acs:
				valid = False
				# print 'Double-spending detected! -> {0} and {1} (by {2})'.format(iac.conflicts.index, iac.index, m.index)
				iac.trusty -= tn * A / N
				# print 'Decrease trusty of', iac.index, 'about', -tn
				iac.bad += 1 # for debugging
				# iac.tx.trusty -= 1
				if iac.trusty < InvalidTrusty:
					iac.dat = t + vlt
					iac.deactivated = True
				detected.append(iac)

		# print 'terms :', [term.index for term in m.dag.terms]
		# print T
		# print 'non-terms :', [nterm.index for nterm in m.dag.nterms]
		# print N		
		# increase trusty except bad txs

		if valid:
			for ac in acs:
				ac.fp = fp
				dw = tx.depth - ac.depth
				# print ac.index,':',dw, 'so, ', min(0.5, dw * T * T / N)
				ac.trusty += (0.5 - fp) * math.exp(dw-8)

				ac.good += 1
				if ac.trusty > ConfirmTrusty:
					ac.cft = t + vlt
					ac.confirmed = True

		# for ac in acs:
		# 	if ac not in detected:
		# 		ac.fp = fp
		# 		dw = tx.depth - ac.depth
		# 		# print ac.index,':',dw, 'so, ', min(0.5, dw * T * T / N)
		# 		ac.trusty += (0.5 - fp) * math.exp(dw-20)

		# 		ac.good += 1
		# 		if ac.trusty > ConfirmTrusty:
		# 			ac.cft = t + vlt
		# 			ac.confirmed = True

		m.dag.txs[tx.index] = tx
		return (pts, vlt)

	def validate_IOTA(self, tx, t):
		m = tx.miner
		vlt = 0 # validation overhead (can be accumulated)
		nTrial = 0
		while nTrial < IOTAMaxValidationTrial:
			pts = m.dag.getPts() # choose parents
			acs = set()
			for pt in pts:
				acs.update(m.dag.getAcs(pt))
			acs = [ac for ac in acs if not ac.deactivated]
			vlt += len(acs) * tVal # overhead added

			# validation
			valid = True
			iacs = [ac for ac in acs if ac.conflicts]
			for iac in iacs:
				if iac.conflicts in acs:
					valid = False
					# if Vb:
					# print 'Double-spending detected! -> {0} and {1} (by {2})'.format(iac.conflicts.index, iac.index, m.index)
					nTrial += 1				
					if not iac.deactivated and (t - iac.int) > IOTATxTimeout:
						iac.deactivated = True
						iac.dat = t
						# print iac.index, 'deactivated'
			if valid: # submit to tx
				tx.pts = pts
				m.dag.txs[tx.index] = tx
				[pt.cds.add(tx) for pt in pts]
				tx.depth = min([pt.depth for pt in pts]) + 1
				vlt += tPoW
				return (pts, vlt)
		# trial exceeded: re-validation
		return None

	# blockchain's
	def validate_BlockChain(self, tx, t):
		m = tx.miner
		vlt = len(m.chain.newTxs) * tVal
		# if (tx.conflicts not in m.chain.newTxs) and (tx.conflicts not in m.chain.valTxs):
		m.chain.newTxs.add(tx)
		return None, vlt

	# miner
	# def doConfirm(m, t, MinTerms):
	# 	[m.dag.deactivate(v, t) for v in m.dag.txs.values() if v.trusty < -10]

	# 	# by trusty
	# 	return [v.index for v in m.dag.txs.values() if v.trusty > 10 and (not v.confirmed)]


	def confirm(self, t):
		# print 'currently',len(m.dag.terms),'terminals'
		minterms = IOTAMinTermsToConfirm
		# MCMC
		terms = set(self.dag.terms)
		if len(terms) < minterms:
			return

		C = dict() # {index : be-valid-count}
		confirmed = list()

		# selected terms
		sterms = random.sample(terms, min(minterms, int(len(terms) * 0.9)))
		th = len(sterms) * ConfTh

		for stx in sterms:
			for stxa in self.dag.getAcs(stx):
				si = stxa.index # index of the selected term's anscestor
				if si in C:
					C[si] += 1
				else:
					C[si] = 1
		return [s for (s,i) in C.items() if i > th]
		# for v in m.dag.nterms:
		# 	dcs = m.dag.getDcs(v)
		# 	if len(dcs & terms) > th:
		# 		if v.conflicts:
		# 			print 'False Positive of',v.index,':', len(dcs & terms), 'of', len(terms), 'txs validate this one!'
		# 		confirmed.append(v.index)
		# return confirmed
