from math import cos, sin, atan2
from collections import namedtuple
import numpy as np
import cv2

coord = namedtuple("Coordinates", ["x", "y"])

RED = (0, 0, 255)
LRED = (84, 84, 255)
ORANGE = (0, 100, 250)
GREEN = (0, 128, 0)
MINT = (200, 250, 50)
YELLOW = (0, 255, 255)
CYAN = (255, 255, 0)
GRAY = (180,180,180)
SKYBLUE = (235, 206, 135)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class GUI:
    def __init__(self):
        self.x = 1800
        self.y = 900
        self.xm = 100 # x-axis margin
        self.ym = 50 # y=axis margin
        self.canvas = np.full((self.y, self.x, 3), 255, np.uint8)
        self.vtx_r = 20
        self.thk = 10 # thickness
        self.vtx_ym = self.vtx_r * 4 + 10

        self.font = cv2.FONT_HERSHEY_COMPLEX

    def show(self, miner, style, t):
        self.canvas.fill(255)   # 그릴 때마다 canvas 초기화
        cv2.putText(self.canvas, f'Time : {round(t,3)} secs', (10,50), self.font, fontScale=1, color=BLACK, thickness=2)

        txs = miner.dag.txs
        tx_grp = []
        genesis_tx = set([v[1] for v in txs.items() if v[0] < 0])
        tx_grp.append(genesis_tx)

        while True:
            next_gen_tx = self.__get_next_gens(tx_grp)
            if not next_gen_tx:
                break
            tx_grp.append(next_gen_tx)

        # Set vertex position
        vtx_pos = {}
        x_offset = self.x / (len(tx_grp) + 1)
        x_pos = x_offset
        for subgrp in tx_grp:
            y_pos = (self.y / 2) - len(subgrp) * self.vtx_ym / 2
            if y_pos < self.ym:
                y_offset = (self.y - self.ym) / len(subgrp)
                y_pos = self.ym
            else:
                y_offset = self.vtx_ym

            for tx in subgrp:
                if not tx.idx in vtx_pos:
                    vtx_pos[tx.idx] = coord(int(x_pos), int(y_pos))
                y_pos += y_offset
            x_pos += x_offset

        for subgrp in tx_grp:
            for tx in subgrp:
                tx_pos = vtx_pos[tx.idx]

                # Draw vertices
                if tx.idx < 0:
                    vtx_color = YELLOW
                elif tx.is_conf:
                    if tx.confl_tx:
                        vtx_color = MINT    # False positive
                    else:
                        vtx_color = GREEN # True positive
                elif tx.is_deact:
                    if not tx.confl_tx:
                        vtx_color = ORANGE # False negative
                    else:
                        vtx_color = RED   # True negative
                elif tx.confl_tx:
                    vtx_color = LRED
                elif len(tx.clds) == 0:
                    vtx_color = SKYBLUE  # tip vertices
                else:
                    vtx_color = CYAN     # pending txs

                cv2.circle(self.canvas, tx_pos, self.vtx_r, vtx_color, self.thk)
                cv2.putText(self.canvas, str(tx.idx), (tx_pos.x - 15, tx_pos.y), self.font, fontScale=0.8, color=BLACK, thickness=2)
                if style == "PWGR":
                    cv2.putText(self.canvas, str(round(tx.trusty, 2)), (tx_pos.x - 24, tx_pos.y + 18), self.font, fontScale=0.7, color=BLACK, thickness=2)

                # Draw connecting line
                for prt in tx.prts:
                    if prt.idx in vtx_pos:
                        sx, sy = tx_pos             # son coord.
                        px, py = vtx_pos[prt.idx]   # paretn coord.
                        theta = atan2(py-sy, px-sx)
                        start_x, start_y = int(sx + self.vtx_r * cos(theta)), int(sy + self.vtx_r * sin(theta))
                        end_x, end_y = int(px - (self.vtx_r + self.thk) * cos(theta)), int(py + (self.vtx_r + self.thk) * sin(theta))
                        cv2.arrowedLine(self.canvas, (start_x, start_y), (end_x, end_y), GRAY, thickness=2, line_type=8, tipLength=0.05)

        cv2.imshow(f'dag-miner{miner.idx}', self.canvas)
        paused = False
        while True:
            if paused: k = cv2.waitKey(0)   # unicode decimal
            else: k = cv2.waitKey(10)

            if k <= 122 and k > 0:
                print(f'key : {k}')
            if k == 27:     # ESC
                return True
            elif k == 32:   # space bar
                if paused: paused = False
                else: paused = True
            else: return

    def kill(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __get_next_gens(self, tx_grp: list):
        next_gen_tx = set()
        curr_tx_ls = set()
        for subgrp in tx_grp:
            curr_tx_ls.update(subgrp)

        for tx in tx_grp[-1]:
            for c in tx.clds:
                if c in curr_tx_ls:
                    continue
                next_gen_tx.add(c)

        return next_gen_tx

    # def __get_next_gens(self, tx_grp: list):
    #     next_gen_tx = set()
    #     for tx in tx_grp[-1]:
    #         for c in tx.clds:
    #             if [tx for tx in tx_grp if c in tx]: continue
    #             next_gen_tx.add(c)
    #     return next_gen_tx


if __name__ == "__main__":
    a = GUI()
    a.show(1,1,2)