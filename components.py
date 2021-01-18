import random
import math

nP = 2 # number of parents

## SG components ##
class power:
	def __init__(self, index):
		self.index = index

class ami:
	def __init__(self, index):
		self.index = index

## dag ##
class Tx:
	def __init__(self, income, index, confirmed=False):
		self.index = index # if no index set, it will invoke malfunction
		self.miner = None # the miner who did validate

		# time records
		self.int = income # income time
		self.vlt = 0 # validation done time
		self.cft = 0 # confirmed time
		self.dat = 0 # de-activated time

		# dag related		
		self.depth = 0
		self.pts = set() # parents
		self.cds = set() # childs

		# DLT related
		self.confirmed = confirmed
		self.deactivated = False

		# double spending
		self.conflicts = None
		self.conflicted = False
		self.trusty = 0
		self.good = 0
		self.bad = 0
		self.fp = 0

	def reset(self): # ready for the reuse (remain only self.ist)
		self.miner = None

		# time records (except income time)
		self.vlt = 0
		self.cft = 0
		self.dat = 0

		# dag related
		self.depth = 0
		self.pts = set()
		self.cds = set()

		# DLT related
		self.confirmed = False if self.index>=0 else True
		self.deactivated = False

		# double spending
		self.trusty = 0
		self.good = 0
		self.bad = 0
		self.fp = 0

	def setMiner(self, miner):
		self.miner = miner

class dag:
	def __init__(self):
		# dag's txs : the txs included in the dag
		self.txs = {} # {index : tx()}

	def childInDag(self, tx):
		return [child for child in tx.cds if child.index in self.txs]

	@property
	def terms(self):
		return [tx for tx in self.txs.values() if (not self.childInDag(tx))]

	@property
	def nterms(self):
		return [tx for tx in self.txs.values() if (self.childInDag(tx)) and (tx.confirmed==False) and (tx.deactivated==False)]

	@property
	def width(self):
		return 3 # not implemented

	# return set() of tx()
	def getPts(self):
		terms = self.terms
		# print 'terms : ', [tx.index for tx in terms]
		if len(terms) < nP:
			return terms
		else:
			return random.sample(terms, nP)

	def getPts_PowerGraph(self, T):
		terms = self.terms
		# print 'terms : ', [tx.index for tx in terms]
		nP = max(2, int(math.sqrt(T)))
		if len(terms) < nP:
			return terms
		else:
			return random.sample(terms, nP)

	# ascendant of a vertex
	# input : tx
	# return set() of tx
	# << this vertex is included!! >>
	def getAcs(self, tx):
		acs = set([tx])

		currents = set([tx])
		nexts = set()
		while True:			
			for current in currents: # pt : index of each parent
				for parent in current.pts: # parent's parents
					if parent.index not in self.txs: # not in the miner's dag
						continue
					if parent.index < 0:
						continue # already confirmed / deactivated
					nexts.add(parent)
			if not nexts:
				break
			acs |= nexts
			currents = set(nexts)
			nexts = set() # reset
		# print tx.index, 'acs : ', [ac.index for ac in acs]
		acs = set([ac for ac in acs if ((not ac.confirmed) or (ac.index < 0)) and not ac.deactivated])
		a = [ac for ac in acs if ac.deactivated]
		return acs

	# descendant of a vertex
	# return set() of vertex
	# << this vertex is included!! >>
	def getDcs(self, v):
		dcs = set([v])
		cds = set([v]) # childs
		while True:
			ncds = set() # next childs
			for c in cds:
				# print 'tx',c.index,'childs :',[cc.index for cc in c.child]
				for cc in c.cds:
					if cc.deactivated: continue
					if cc.confirmed: continue
					ncds.add(cc)
			if not ncds:
				break
			# print 'next childs :',[c.index for c in ncds]
			dcs |= ncds
			cds = set(ncds)

		# print 'tx',v.index,'dcs :',[dc.index for dc in dcs]
		return dcs

	def deactivate(self, v, t):
		# deactivate a vertex
		v.tx.active = False
		v.tx.int = t

		# # deactivate its dcs -> maybe not needed
		# for dc in self.getDcs(v):
		# 	dc.tx.active = False

	def setConfirm(self, v):
		v.tx.confirmed = True

	def setChild(self, v, cv):
		print v.index,'<-',cv.index
		v.child.add(cv)

class chain:
	def __init__(self):
		self.blocks = list()		
		self.valTxs = set()
		self.newTxs = set()