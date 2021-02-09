import cv2
import numpy as np
import random
from vars import*
import math

X = 1800
Y = 900
XM = 100 # width margin
YM = 50 # height margin
I = np.full((Y,X,3), 255, np.uint8)
C = 20 # vertex size
CW = 10 # vertex linewidth

CM = C * 4 + 10 # vertex y-margin

VY = dict()
Ypool = range(YM, Y-YM, CM)
random.shuffle(Ypool)

def show(miner, style, t):
	# global Ypool

	I.fill(255)
	txs = miner.dag.txs
	cv2.putText(I,'Time : {0} secs'.format(round(t,3)), (10,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0),2)
	
	# # locate vertices with continuous x
	# x = XM
	# latestTx = max([v.tx.int for v in vts.values()])
	# if latestTx == 0: scale = 0.1
	# else:
	# 	scale = (X - XM * 2) / latestTx
	# 	scale = min(150, scale)
	# 	scale = max(CM/4, scale)
	# xshift = (X-XM) - latestTx * scale

	# vpos = dict()

	# for v in vts.values():
	# 	x = int(XM + scale * v.tx.int + xshift)
	# 	if not v in VY:
	# 		if len(Ypool) == 1:
	# 			newpool = range(YM, Y-YM, CM)
	# 			newpool.remove(Ypool[0])
	# 			random.shuffle(newpool)				
	# 			Ypool += newpool

	# 		y = Ypool.pop()
	# 		VY[v] = y
	# 	vpos[v.index] = (x,VY[v])

	# for v in vts.values():
	# 	vi = v.index
	# 	for pi in v.pts:
	# 		if pi in vpos:
	# 			cv2.arrowedLine(I, vpos[vi], vpos[pi], (180,180,180), 2, line_type=8, tipLength=0.01)

	# for v in vts.values():
	# 	# print v.index, v.child
	# 	vp = vpos[v.index]
	# 	if v.index < 0: # genesis
	# 		vc = (50, 230, 250)
	# 	elif v.confirmed: # confirmed
	# 		if v.conflicts: # false positive
	# 			vc = (0, 0, 255)
	# 		else: # true positive
	# 			vc = (200, 100, 0)
	# 	elif v.deactivated: # deactivated
	# 		if not v.conflicts: # false negative
	# 			vc = (0, 100, 250) 
	# 		else: # true negative
	# 			vc = (255, 150, 0) 
	# 	elif v.conflicts:
	# 		vc = (50, 50, 150)
	# 	elif len(v.child) == 0:
	# 		vc = (200, 200, 200)
	# 	else:
	# 		vc = (200, 200, 100)

	# 	cv2.circle(I, vp, C+5, (0,0,0), 2)
	# 	cv2.circle(I, vp, C, vc, 5)
	# 	cv2.putText(I, str(v.index), (vp[0]-17,vp[1]),cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 2)
	# 	if style == 'PWGR':
	# 		cv2.line(I, (vp[0],vp[1]+8), (vp[0]+int(C*v.trusty),vp[1]+8), ((255,0,0) if v.trusty>0.5 else (0,0,255)), 6)
	# 		# cv2.putText(I, str(v.trusty), (vp[0]-17,vp[1]+18),cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 2)
	# 	elif style == 'IOTA':
	# 		cv2.putText(I, str(len(miner.dag.getDcs(v))), (vp[0]-17,vp[1]+18),cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 2)

	# locate vertices along generation
	gv = [] # vertices listed by generation

	# get gens
	gens = [v[1] for v in txs.items() if v[0] < 0]
	
	gv.append(gens)
	while True:
		ng = getNextGens(gv) # next generation vertices
		if not ng: break
		gv.append(ng)

	# set positions of vertices
	vpos = {}
	xw = X / (len(gv) + 1) # x-size width
	x = xw
	for g in gv:
		y = (Y / 2) - len(g) * CM / 2
		if y < YM:
			yw = ((Y-YM) / len(g))
			y = YM
		else:
			yw = CM
		y = max(y, YM)
		for v in g:
			if not v.index in vpos:
				vpos[v.index] = (x,y)			
			y += yw
		x += xw

	for g in gv:
		for v in g:
			vp = vpos[v.index]
			for p in v.pts:
				if p.index in vpos:
					sx, sy = vp
					ex, ey = vpos[p.index]
					theta = math.atan2(float(ey - sy), float(ex - sx))
					lsx, lsy = int(sx + C * math.cos(theta)), int(sy + C * math.sin(theta))
					lex, ley = int(ex - (C + CW) * math.cos(theta)), int(ey - (C + CW) * math.sin(theta))
					cv2.arrowedLine(I, (lsx, lsy), (lex, ley), (180,180,180), 2, line_type=8, tipLength=0.05)
			# for c in v.child:
			# 	if c.index in vpos:
			# 		cv2.arrowedLine(I, vp, vpos[c.index], (210,210,210), 3, line_type=8, tipLength=0.01)
	# draw each
	for g in gv:
		for v in g:
			# print v.index, v.child
			vp = vpos[v.index]
			if v.index < 0: # genesis - yellow
				vc = (50, 230, 250)
			elif v.confirmed: # confirmed
				if v.conflicts: # false positive - red
					vc = (0, 0, 255)
				# elif v.conflicted: # conflicted but anyway confirmed
				# 	vc = (200, 150, 150)
				else: # true positive - light blue
					vc = (250, 200, 100)
			elif v.deactivated: # deactivated
				if not v.conflicts: # false negative
					vc = (0, 100, 250) 
				else: # true negative - light green
					vc = (200, 250, 50)
			elif v.conflicts:
				vc = (50, 50, 150)
			elif len(v.cds) == 0:
				vc = (200, 200, 200)
			else:
				vc = (200, 200, 100)

			# cv2.circle(I, vp, C+5, (0,0,0), 2)
			cv2.circle(I, vp, C, vc, CW)
			cv2.putText(I, str(v.index), (vp[0]-15,vp[1]),cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0), 2)
			if style == 'PWGR':
				# cv2.line(I, (vp[0],vp[1]+8), (vp[0]+int(C*v.trusty),vp[1]+8), ((255,0,0) if v.trusty>0.5 else (0,0,255)), 6)
				cv2.putText(I, str(round(v.trusty,2)), (vp[0]-24,vp[1]+20),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
				# cv2.putText(I, str(v.depth), (vp[0]-24,vp[1]+50),cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 2)
			elif style == 'IOTA':
				cv2.putText(I, str(len(miner.dag.getDcs(v))), (vp[0]-17,vp[1]+18),cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 2)
			# cv2.putText(I, str(v.hash), (vp[0]-15,vp[1]+18),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))

	cv2.imshow('dag-miner{0}'.format(miner.index), I)
	paused = False
	while True:
		if paused: k = cv2.waitKey(0)
		else: k = cv2.waitKey(10)

		if k < 255 and k > 0:
			print 'key',k
		if k == 27:
			return True
		elif k == 32:
			if paused: paused = False
			else: paused = True
		else:
			return

def getNextGens(gv):
	nextgens = set()
	for v in gv[-1]:
		# print 'tx',v.index,'child ->',[c.index for c in v.cds]
		for c in v.cds:
			if [g for g in gv if c in g]: continue
			nextgens.add(c)
	return nextgens

def kill():
	k = cv2.waitKey(0)	
	cv2.destroyAllWindows()