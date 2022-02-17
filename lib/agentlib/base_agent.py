# -----------------------------------------------------------------------------
# base_agent.py
# -----------------------------------------------------------------------------

import time
import math

from swapl_agent import *
from swapl_geometry import *

class Agent(SWAPL_Agent):

    def on_create(self, *args):
        super().on_create()
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.heading = 0
        self.v = 0
        self.w = 0
        self.delta_t = 0.01
        self.image = 'arrow_white.png'
        self.add_attributes( [ 'x', 'y', 'vx', 'vy', 'heading', 'v', 'w', 'delta_t', 'image' ] )
        self.run_thread()

    def run(self, args):
        while self.running:
            time.sleep(self.delta_t)

            self.heading = self.heading + self.w * self.delta_t

            self.vx = self.v * math.cos(self.heading)
            self.vy = self.v * math.sin(self.heading)

            self.x += self.vx * self.delta_t
            self.y += self.vy * self.delta_t

