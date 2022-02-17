# -----------------------------------------------------------------
# swapl_agent.py
# -----------------------------------------------------------------

from swapl_exceptions import *
from swapl_types import *
from swapl_isa import *
from swapl_codelet import *

import threading
import time
import random
import math

# -----------------------------------------------------------------
class SWAPL_Agent:

    def __init__(self, program, swapl_agent):
        self.program = program
        self.swapl_agent = swapl_agent
        self.name = swapl_agent.get_attribute('name')
        self.role = swapl_agent.get_attribute('role')
        self.thread = None
        self.running = False

    def __repr__(self):
        return repr( self.__class__.__name__ )

    def add_attributes(self, field_list):
        for x in field_list:
            self.swapl_agent.add_attribute(x, AttributeInterface(self, x))

    def add_attribute(self, field):
        self.swapl_agent.add_attribute(field, AttributeInterface(self, field))

    def get_attribute(self, aname):
        return getattr(self, aname)

    def set_attribute(self,fname,fval):
        setattr(self, fname, fval)

    def export(self, method, name):
        self.methods[name] = method

    def get_method(self, name):
        return self.methods[name]

    def on_create(self):
        pass

    def run_thread(self, uParams = []):
        self.thread = threading.Thread(target = self.__run, args = uParams, daemon = True)
        self.running = True
        self.thread.start()

    def __run(self, uParams = []):
        self.run(uParams)

    def run(self, uParams = []):
        pass

