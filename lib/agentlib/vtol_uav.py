# -----------------------------------------------------------------------------
# vtol_uav.py
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
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.wz = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.heading = 0
        self.delta_t = 0.01
        self.image = 'arrow.png'
        self.export_field( [ 'x', 'y', 'z',
                             'vx', 'vy', 'vz', 'wz',
                             'roll', 'pitch', 'yaw', 'heading',
                             'delta_t', 'image' ] )
        self.export(self.set_v, 'set_v')
        self.run_thread()

    def set_v(self, terms):
        v = terms[0]
        self.vx = v * math.cos(self.yaw)
        self.vy = v * math.sin(self.yaw)

    def run(self, args):
        while self.running:
            time.sleep(self.delta_t)

            self.yaw = normalize_angle_radians(self.yaw + self.wz * self.delta_t)
            self.heading = self.yaw

            self.x += self.vx * self.delta_t
            self.y += self.vy * self.delta_t
            self.z += self.vz * self.delta_t

