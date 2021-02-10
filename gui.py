import numpy as np
import cv2
from math import cos, sin
class GUI:
    def __init__(self):
        x = 1800
        y = 900
        xm = 100 # x-axis margin
        ym = 50 # y=axis margin
        canvas = np.full((y,x,3), 255, np.uint8)
        vtx_size = 20
        thk = 10 # thickness
        vtx_ym = vtx_size * 4 + 10

    def show(self, miner, style, t):
        cv2.putText(self.canvas, f'Time : {round(t,3)} secs')
        txs = miner.dag.txs

    def kill(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __get_next_gens(self, gv):
        pass