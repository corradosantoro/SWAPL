# -----------------------------------------------------------------
# swapl_isa.py
# -----------------------------------------------------------------

import types

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
class Pop(Instruction):
    def execute(self, pc, runtime):
        runtime.pop()
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
class Branch(Instruction):
    UNCONDITIONAL = 0
    EQ = 1
    NEQ = 2
    REPR = { UNCONDITIONAL : "",
             EQ : "Equal",
             NEQ : "Not Equal" }

    def __repr__(self):
        ( comparison, instr_to_skip) = self.term
        return "{} {}\t{}".format(self.__class__.__name__, Branch.REPR[comparison], instr_to_skip)

    def execute(self, pc, runtime):
        ( comparison, instr_to_skip) = self.term
        if (comparison == Branch.UNCONDITIONAL):
            return pc + instr_to_skip + 1
        val = int(runtime.pop())
        if (comparison == Branch.EQ)and(val == 1):
            return pc + instr_to_skip + 1
        elif (comparison == Branch.NEQ)and(val == 0):
            return pc + instr_to_skip + 1
        else:
            return None
# -----------------------------------------------------------------
class MkInstance(Instruction):
    def execute(self, pc, runtime):
        v = runtime._get_var(self.term)
        new_instance = v.clone()
        runtime.push(new_instance)
# -----------------------------------------------------------------
class Invoke(Instruction):
    def execute(self, pc, runtime):
        values = runtime.pop()
        obj = runtime.pop()
        method = obj.get_attribute(self.term)
        args = values.items()

        from swapl_program import SWAPL_Function

        if isinstance(method, PythonLink):
            func = method.eval_as_attribute()
            ret = func(*args)
            if ret is not None:
                runtime.push(ret)
        elif isinstance(method, PythonFunction):
            ret = method.evaluate(*args)
            if ret is not None:
                runtime.push(ret)
        elif isinstance(method, SWAPL_Function):
            print("WARNING! You have to check if you're calling an instance")
            values.insert(0, obj)
            method.call(runtime, values)
        else:
            # its a normal SWAPL_Object method
            args.insert(0, runtime)
            args.insert(0, obj)
            ret = method(*args)
            if ret is not None:
                runtime.push(ret)
# -----------------------------------------------------------------
class Call(Instruction):
    def fun_call_execute(self, isfun, pc, runtime):
        if type(self.term) == tuple:
            (var, field) = self.term
            obj = runtime._get_var(var)
            f = obj.get_field(field)
            if isinstance(f, PythonLink):
                func = f.eval_as_attribute()
                values = runtime.pop()
                args = values.items()
                ret = func(*args)
                runtime.push(ret)
                return None
            else:
                raise UndefinedFunctionException()
        f = runtime.program.get_function(self.term)
        if f is None:
            proc = runtime.program.lib.get_function(self.term)
            args = StartSL.pop_list(runtime, 1)
            if isfun:
                ret = proc(*args)
                runtime.push(ret)
            else:
                proc(*args)
            return None
        else:
            values = runtime.pop()
            ret_val = f.call(runtime, values)
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
        obj = SWAPLObject()
        obj.add_attributes(self.term, StartSL.pop_list(runtime, len(self.term)))
        runtime.push(obj)
# -----------------------------------------------------------------
class GetAttribute(Instruction):
    def execute(self, pc, runtime):
        var = runtime.pop()
        field = self.term
        obj = var #runtime._get_var(var)
        f = obj.get_attribute(field)
        if isinstance(f, PythonLink):
            runtime.push(f.eval_as_attribute())
        elif isinstance(f, AttributeInterface):
            runtime.push(f.get())
        else:
            runtime.push(f)
# -----------------------------------------------------------------
class SetAttribute(Instruction):
    def execute(self, pc, runtime):
        var = runtime.pop()
        val = runtime.pop()
        field = self.term
        obj = var #runtime._get_var(var)
        f = obj.get_attribute(field)
        if isinstance(f,AttributeInterface):
            f.set(val)
        else:
            obj.set_attribute(field, val)
# -----------------------------------------------------------------
class GetSubscript(Instruction):
    def execute(self, pc, runtime):
        var = runtime.pop()
        index = runtime.pop()
        obj = var #runtime._get_var(var)
        f = obj[index]
        runtime.push(f)
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
class Neg(Instruction):
    def execute(self, pc, runtime):
        v1 = runtime.pop()
        runtime.push(- v1)
# -----------------------------------------------------------------
class CmpEQ(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 == v1)
# -----------------------------------------------------------------
class CmpNEQ(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 != v1)
# -----------------------------------------------------------------
class CmpLT(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        runtime.push(v2 < v1)
# -----------------------------------------------------------------
class CmpGT(Instruction):
    def execute(self, pc, runtime):
        (v1, v2) = runtime.pop2()
        res = v2 > v1
        runtime.push(res)
# -----------------------------------------------------------------
# Parallel Exec
# -----------------------------------------------------------------
class ParExecBegin(Instruction):

    def __init__(self, term, join = True):
        super().__init__(term)
        self.join = join

    def __repr__(self):
        (code_size, func) = self.term
        return "{}\t{} {}".format(self.__class__.__name__, code_size, func)

    def get_parexec_size(self):
        return self.term[0]

    def get_filter_code(self):
        return self.term[1]

    def execute(self, pc, runtime):
        pass
        #print(self.__class__,self.term)
        #(code_size, func) = self.term
        #agent_set = runtime._get_var('__agentset__')
        #if type(func) == tuple:
        #    (func, params) = func
        #    agent_set = func(agent_set, params)
        #else:
        #    agent_set = func(agent_set)
        #print(agent_set)

# -----------------------------------------------------------------
class ParExecEnd(Instruction):
    pass
