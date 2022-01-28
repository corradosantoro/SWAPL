# -*- coding: utf-8 -*-
#
#  UNICT CRAZYFLIE SWARM LIBRARY
#
#  Copyright (C) Corrado Santoro, santoro@dmi.unict.it
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc., 51
#  Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import os
import time
import math
import threading
import traceback
import types
import sys

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger

from swapl_geometry import *
from swapl_agent import *
from swapl_logger import *


X_THRESHOLD = 0.1 # 10cm
Y_THRESHOLD = 0.1 # 10cm
Z_THRESHOLD = 0.2 # 20cm

QFE_THRESHOLD = 0.5

LANDING_VZ = -0.5 #50cm/s

TX_DELAY = 0.2
LOGGING_PERIOD = 1000

def get_p(_name, _p):
    if _name in _p:
        return _p[_name]
    else:
        return None

class SWAPL_CF_Factory:

    factory = None

    @classmethod
    def create(cls):
        if cls.factory is None:
            cflib.crtp.init_drivers(enable_debug_driver=False)
            cls.factory = CachedCfFactory(rw_cache='./cache')


class ForceLandingException(Exception):
    pass


class Agent(SWAPL_Agent):

    def on_create(self, *args):
        self.scf = None
        self.cf = None
        self._id = None
        self.flying = False
        self.rtl = [ 0, 0 ]
        self.origin = None
        self.force_landing = False
        self.is_async = False
        self.target_x = 0
        self.target_y = 0
        self.target_z = 0
        self.target_yaw = 0
        self.z = 0
        self.vz = 0
        self.export_field( ['z', 'vz'] )
        SWAPL_CF_Factory.create()
        self.uri = self.swapl_agent.get_field('uri')
        self.scf = SWAPL_CF_Factory.factory.construct(self.uri)
        self.scf.open_link()
        self.cf = self.scf.cf
        super().on_create(*args)

    def log(self, _str):
        if self.cf is None:
            Console.info(_str)
        else:
            Console.info("[{}] {}".format(self.cf.link_uri, _str))

    def reset_estimator(self):
        self.cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(TX_DELAY)
        self.cf.param.set_value('kalman.resetEstimation', '0')
        self._wait_for_position_estimator()
        self._start_log_position()
        time.sleep((LOGGING_PERIOD * 2)/1000.0)
        self.log('Estimator OK: Battery {}'.format(self.battery))

    def _wait_for_position_estimator(self):
        print('Waiting for estimator to find position...')

        log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
        log_config.add_variable('kalman.varPX', 'float')
        log_config.add_variable('kalman.varPY', 'float')
        log_config.add_variable('kalman.varPZ', 'float')
        log_config.add_variable('pm.vbat', 'float')

        var_y_history = [1000] * 10
        var_x_history = [1000] * 10
        var_z_history = [1000] * 10

        threshold = 0.001

        with SyncLogger(self.scf, log_config) as logger:
            for log_entry in logger:
                data = log_entry[1]

                var_x_history.append(data['kalman.varPX'])
                var_x_history.pop(0)
                var_y_history.append(data['kalman.varPY'])
                var_y_history.pop(0)
                var_z_history.append(data['kalman.varPZ'])
                var_z_history.pop(0)

                min_x = min(var_x_history)
                max_x = max(var_x_history)
                min_y = min(var_y_history)
                max_y = max(var_y_history)
                min_z = min(var_z_history)
                max_z = max(var_z_history)

                self.battery = data['pm.vbat']

                #print("{} {} {}".
                #    format(max_x - min_x, max_y - min_y, max_z - min_z))

                if (max_x - min_x) < threshold and (
                        max_y - min_y) < threshold and (
                        max_z - min_z) < threshold:
                    break

    def _start_log_position(self):
        self.log_conf = LogConfig(name='Position', period_in_ms=LOGGING_PERIOD)
        self.log_conf.add_variable('kalman.stateX', 'float')
        self.log_conf.add_variable('kalman.stateY', 'float')
        self.log_conf.add_variable('kalman.stateZ', 'float')
        self.log_conf.add_variable('pm.vbat', 'float')
        #self.log_conf.add_variable('stabilizer.roll', 'float')
        #self.log_conf.add_variable('stabilizer.pitch', 'float')
        self.log_conf.add_variable('stabilizer.yaw', 'float')

        self.cf.log.add_config(self.log_conf)
        self.log_conf.data_received_cb.add_callback(self._position_callback)
        self.log_conf.start()

    def _position_callback(self, timestamp, data, logconf):
        self.x = data['kalman.stateX']
        self.y = data['kalman.stateY']
        self.z = data['kalman.stateZ']
        self.battery = data['pm.vbat']
        self.roll = 0#data['stabilizer.roll']
        self.pitch = 0# data['stabilizer.pitch']
        self.yaw = data['stabilizer.yaw']
        #print('[{}] Pos: ({}, {}, {}), Battery: {}'.format(self.cf.link_uri, self.x, self.y, self.z, self.battery))
        if self.battery < 3.1:
            self.log('LOW BATTERY, VOLTAGE = {}! LANDING'.format(self.battery))
            #SW.force_landing() # land


    def run(self):
        self.reset_estimator()
        while self.flying:
            time.sleep(TX_DELAY)
