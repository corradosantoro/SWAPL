# -----------------------------------------------------------------
# swapl_isa.py
# -----------------------------------------------------------------

from swapl_types import *

def disasm(pgm):
    listing = ""
    line = 1
    for i in pgm:
        listing += "%3d : %s\n" % (line,i)
        line += 1
    return listing

class Instruction:

    def __init__(self, uTerm = None):
        self.term = uTerm

    def __repr__(self):
        if self.term is None:
            t = ""
        else:
            t = self.term
        return "{}\t{}".format(self.__class__.__name__, t)

    def execute(self, pc, runtime):
        pass

# -----------------------------------------------------------------
class Status(Instruction):
    def execute(self, pc, runtime):
        runtime.status()
# -----------------------------------------------------------------
# Stack Manipulation
# -----------------------------------------------------------------
class Push(Instruction):
    def execute(self, pc, runtime):
        runtime.push(self.term)
# -----------------------------------------------------------------
class Dup(Instruction):
    def execute(self, pc, runtime):
        runtime.dup()
# -----------------------------------------------------------------
class Clean(Instruction):
    def execute(self, pc, runtime):
        runtime.clean()
# -----------------------------------------------------------------
# Stack/Heap
# -----------------------------------------------------------------
class Load(Instruction):
    def execute(self, pc, runtime):
        runtime.load(self.term)
# -----------------------------------------------------------------
class Store(Instruction):
    def execute(self, pc, runtime):
        runtime.store(self.term)
# -----------------------------------------------------------------
# Vars
# -----------------------------------------------------------------
class MkVar(Instruction):
    def execute(self, pc, runtime):
        runtime._mk_var(self.term)
# -----------------------------------------------------------------
# Transfer
# -----------------------------------------------------------------
class Skip(Instruction):
    UNCONDITIONAL = 0
    EQ = 1
    NEQ = 2
    def execute(self, pc, runtime):
        ( comparison, instr_to_skip) = self.term
        if (comparison == Skip.UNCONDITIONAL):
            return pc + instr_to_skip + 1
        val = runtime.pop()
        if (comparison == Skip.EQ)and(val == 0):
            return pc + instr_to_skip + 1
        elif (comparison == Skip.NEQ)and(val != 0):
            return pc + instr_to_skip + 1
        else:
            return None
# -----------------------------------------------------------------
class Call(Instruction):
    def fun_call_execute(self, isfun, pc, runtime):
        f = runtime.program.get_function(self.term)
        if f is None:
            ( proc, arity ) = runtime.get_agent_object().get_method(self.term)
            args = StartSL.pop_list(runtime, arity)
            if isfun:
                ret = proc(*args)
                runtime.push(ret)
            else:
                proc(*args)
            return None
        else:
            from swapl_codelet import SWAPL_Runtime, SWAPL_Heap
            heap = runtime.get_heap().push()
            params = f.get_params()
            i = len(params) - 1
            values = runtime.pop()
            while i >= 0:
                heap.make_var(params[i])
                heap.set_var(params[i], values[i])
                i -= 1
            new_runtime = SWAPL_Runtime(runtime.get_program(), heap, f.get_code())
            ret_val = new_runtime.run()
            heap = heap.pop()
            if ret_val is not None:
                runtime.push(ret_val)

    def execute(self, pc, runtime):
        self.fun_call_execute(False, pc, runtime)
# -----------------------------------------------------------------
class FunCall(Call):
    def execute(self, pc, runtime):
        return self.fun_call_execute(True, pc, runtime)
# -----------------------------------------------------------------
class Return(Instruction):
    def execute(self, pc, runtime):
        ret_val = runtime.pop()
        return ret_val
# -----------------------------------------------------------------
# Sets/Lists
# -----------------------------------------------------------------
class StartSL:
    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def pop_list(cls, runtime, items):
        terms = [ ]
        while items > 0:
            t = runtime.pop()
            terms.insert(0,t)
            items -= 1
        return terms
# -----------------------------------------------------------------
class MkSet(Instruction):
    def execute(self, pc, runtime):
        runtime.push(Set(StartSL.pop_list(runtime, self.term)))
# -----------------------------------------------------------------
class MkOrdSet(Instruction):
    def execute(self, pc, runtime):
        runtime.push(OrderedSet(StartSL.pop_list(runtime, self.term)))
# -----------------------------------------------------------------
# Structs
# -----------------------------------------------------------------
class MkStruct(Instruction):
    def execute(self, pc, runtime):
        runtime.push(StructData(self.term, StartSL.pop_list(runtime, len(self.term))))
# -----------------------------------------------------------------
class GetField(Instruction):
    def execute(self, pc, runtime):
        ( var, field ) = self.term
        obj = runtime._get_var(var)
        runtime.push(obj.get_field(field))
# -----------------------------------------------------------------
class SetField(Instruction):
    def execute(self, pc, runtime):
        ( var, field ) = self.term
        obj = runtime._get_var(var)
        val = runtime.pop()
        obj.set_field(field, val)
# -----------------------------------------------------------------
# Arithmetic/Logic
# -----------------------------------------------------------------
class Add(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 + v1)
# -----------------------------------------------------------------
class Sub(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 - v1)
# -----------------------------------------------------------------
class Mul(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 * v1)
# -----------------------------------------------------------------
class Div(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 / v1)
# -----------------------------------------------------------------
class CmpLT(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 < v1)
# -----------------------------------------------------------------
class CmpGT(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 > v1)
# -----------------------------------------------------------------
# Parallel Exec
# -----------------------------------------------------------------
class ParExecBegin(Instruction):

    def __init__(self, term, join = True):
        super().__init__(term)
        self.join = join

    def __repr__(self):
        return "{}\t{}".format(self.__class__.__name__, self.term)

    def execute(self, pc, runtime):
        #print(self.__class__,self.term)
        func = self.term
        agent_set = runtime._get_var('__agentset__')
        if type(func) == tuple:
            (func, params) = func
            agent_set = func(agent_set, params)
        else:
            agent_set = func(agent_set)
        print(agent_set)

# -----------------------------------------------------------------
class ParExecEnd(Instruction):
    pass
