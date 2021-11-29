# -----------------------------------------------------------------------------
# base_agent.py
# -----------------------------------------------------------------------------

import time

from swapl_agent import *

class Agent(SWAPL_Agent):

    def on_create(self, *args):
        super().on_create()
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.delta_t = 0.1
        self.export_field( [ 'x', 'y', 'vx', 'vy', 'delta_t' ] )
        self.run_thread()

    def run(self, args):
        while self.running:
            time.sleep(self.delta_t)
            self.x += self.vx * self.delta_t
            self.y += self.vy * self.delta_t


