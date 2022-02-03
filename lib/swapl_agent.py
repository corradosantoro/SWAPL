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
        self.name = swapl_agent.get_field('name')
        self.role = swapl_agent.get_field('role')
        self.exported = ['role', 'name']
        self.methods = {}
        self.thread = None
        self.running = False

    def __repr__(self):
        return repr( (self.exported, self.methods) )

    def get_field(self,fname):
        if fname in self.exported:
            return getattr(self, fname)
        else:
            raise UndefinedFieldException(fname)

    def set_field(self,fname,fval):
        if fname in self.exported:
            setattr(self, fname, fval)
        else:
            raise UndefinedFieldException(fname)

    def fields(self):
        flds = { }
        for f in self.exported:
            flds[f] = self.get_field(f)
        return flds

    def export(self, method, name, arity):
        self.methods[name] = (method, arity)

    def export_field(self, field):
        if type(field) == list:
            [ self.exported.append(x) for x in field ]
        else:
            self.exported.append(field)

    def get_method(self, name):
        return self.methods[name]

    def on_create(self):
        self.export(self.swapl_print, 'print', 1)
        self.export(self.swapl_wait, 'wait', 1)
        self.export(self.swapl_rand, 'rand', 1)
        self.export(self.swapl_role, 'role', 1)

    def run_thread(self, uParams = []):
        self.thread = threading.Thread(target = self.__run, args = uParams, daemon = True)
        self.running = True
        self.thread.start()

    def __run(self, uParams = []):
        self.run(uParams)

    def run(self, uParams = []):
        pass

    def swapl_print(self, terms):
        print(*terms.items())

    def swapl_wait(self, terms):
        time.sleep(terms[0])

    def swapl_rand(self, terms):
        return random.uniform(terms[0], terms[1])

    def swapl_role(self, terms):
        from swapl_program import SWAPL_Program
        ag_set = self.program.globals_heap.get_var(SWAPL_Program.AGENTSET)
        return ag_set.roles(terms).one().data[0]['object']

