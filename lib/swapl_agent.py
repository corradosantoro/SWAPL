# -----------------------------------------------------------------
# swapl_agent.py
# -----------------------------------------------------------------

from swapl_exceptions import *
from swapl_types import *
from swapl_isa import *
from swapl_runtime import *

import threading
import time

# -----------------------------------------------------------------
class SWAPL_Agent:

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.exported = ['role', 'name']
        self.methods = {}
        self.thread = None
        self.running = False

    def get_field(self,fname):
        if fname in self.exported:
            return getattr(self, fname)
        else:
            raise UndefinedFieldException(fname)

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

    def run_thread(self, uParams = []):
        self.thread = threading.Thread(target = self.__run, args = uParams, daemon = True)
        self.thread.start()

    def __run(self, uParams = []):
        self.run(uParams)

    def run(self, uParams = []):
        pass

    def swapl_print(self, terms):
        print(*terms.items())

    def swapl_wait(self, terms):
        time.sleep(terms[0])

