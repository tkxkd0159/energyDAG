import numpy as np
import cv2
from math import cos, sin, atan2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (255, 255, 0)
RED = (0, 0, 255)
GREEN = (0, 128, 0)
SKYBLUE = (235, 206, 135)
YELLOW = (0, 255, 255)
GRAY = (180,180,180)
class GUI:
    def __init__(self):
        self.x = 1800
        self.y = 900
        self.xm = 100 # x-axis margin
        self.ym = 50 # y=axis margin
        self.canvas = np.full((self.y, self.x, 3), 255, np.uint8)
        self.vtx_size = 20
        self.thk = 10 # thickness
        self.vtx_ym = self.vtx_size * 4 + 10

        self.font = cv2.FONT_HERSHEY_COMPLEX

    def show(self, miner, style, t):
        cv2.putText(self.canvas, f'Time : {round(t,3)} secs', (10,50), self.font, fontScale=1, color=(0,0,0), thickness=2)

        txs = miner.dag.txs
        tx_grp = []
        genesis_tx = set([v[1] for v in txs.items() if v[0] < 0])
        tx_grp.append(genesis_tx)

        while True:
            next_gen_tx = self.__get_next_gens(tx_grp)
            if not next_gen_tx:
                break
            tx_grp.append(next_gen_tx)

        vtx_pos = {}
        x_offset = self.x / (len(tx_grp) + 1)
        x_pos = x_offset
        for grp in tx_grp:
            y_pos = (self.y / 2) - len(grp) * self.vtx_ym / 2
            if y_pos < self.ym:
                y_offset = (self.y - self.ym) / len(grp)
                y_pos = self.ym
            else:
                y_offset = self.vtx_ym

            for tx in grp:
                if not tx.index in vtx_pos:
                    vtx_pos[tx.index] = (x_pos, y_pos)
                y_pos += y_offset
            x_pos += x_offset

    def kill(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __get_next_gens(self, tx_grp: list):
        next_gen_tx = set()
        curr_tx_ls = set()
        for grp in tx_grp:
            curr_tx_ls.update(grp)

        for tx in tx_grp[-1]:
            for c in tx.clds:
                if c in curr_tx_ls:
                    continue
                next_gen_tx.add(c)

        return next_gen_tx


if __name__ == "__main__":
    a = GUI()
    a.show(1,1,2)