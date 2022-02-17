# -----------------------------------------------------------------
# swapl_lib.py
# -----------------------------------------------------------------

import time

from swapl_types import *

# -----------------------------------------------------------------
class SWAPL_Lib:

    def __init__(self, uProgram):
        self.program = uProgram
        self.functions = { }
        self.export(self.swapl_print, 'print')
        self.export(self.swapl_wait, 'wait')
        self.export(self.swapl_role, 'role')
        self.export(self.swapl_all, 'all')
        #self.export(self.swapl_roles, 'roles')

        Random = SWAPLObject()
        Random.from_dict(
            { "uniform" : PythonLink("random.uniform") }
        )
        self.program.globals_heap.make_var("Random")
        self.program.globals_heap.set_var("Random", Random)

        Math = SWAPLObject()
        Math.from_dict(
            { "pi" : PythonLink("math.pi"),
              "fabs" : PythonLink("math.fabs"),
              "sqrt" : PythonLink("math.sqrt"),
              "sin" : PythonLink("math.sin"),
              "cos" : PythonLink("math.cos"),
              "atan2" : PythonLink("math.atan2") }
        )
        self.program.globals_heap.make_var("Math")
        self.program.globals_heap.set_var("Math", Math)

    def export(self, method, name):
        self.functions[name] = method

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        else:
            return None

    def swapl_print(self, terms):
        print(*terms.items())

    def swapl_wait(self, terms):
        time.sleep(terms[0])

    def swapl_role(self, terms):
        from swapl_program import SWAPL_Program
        ag_set = self.program.globals_heap.get_var(SWAPL_Program.AGENTSET)
        return ag_set.roles(terms).one().data[0]['object']

    def swapl_all(self, terms):
        from swapl_program import SWAPL_Program
        ag_set = self.program.globals_heap.get_var(SWAPL_Program.AGENTSET)
        return ag_set


