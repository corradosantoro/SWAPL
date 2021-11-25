# -----------------------------------------------------------------
# swapl_agent.py
# -----------------------------------------------------------------

from swapl_exceptions import *
from swapl_types import *
from swapl_isa import *
from swapl_runtime import *

# -----------------------------------------------------------------
class SWAPL_Agent:

    def __init__(self, name, role):
        self.exported = { }
        self.exported['role'] = role
        self.exported['name'] = name
        self.methods = {}

    def get_field(self,fname):
        return self.exported[fname]

    def export(self, method, name, arity):
        self.methods[name] = (method, arity)

    def get_method(self, name):
        return self.methods[name]

    def on_create(self):
        self.export(self.swapl_print, 'print', 1)

    def swapl_print(self, terms):
        print(terms)
