# get W
def getW(dag):
	ws = list()
	for ivt in dag.vts.keys():
		pt = dag.vts[ivt]
		h = 0 # height
		lost = False
		while not lost:
			lost = True
			while pt.pts:
				npt = pt.pts.pop() # parent's parent
				if npt in dag.vts:
					h += 1
					pt = dag.vts[npt]
					lost = False
					break
		while len(ws) <= h:
			ws.append(0)
		ws[h] += 1
	return ws