# -----------------------------------------------------------------
# swapl_lib.py
# -----------------------------------------------------------------

import time

# -----------------------------------------------------------------
class SWAPL_Lib:

    def __init__(self, uProgram):
        self.program = uProgram
        self.functions = {}
        self.export(self.swapl_print, 'print')
        self.export(self.swapl_wait, 'wait')
        self.export(self.swapl_role, 'role')

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


