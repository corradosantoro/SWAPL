# -----------------------------------------------------------------------------
# swapl_codelet.py
# -----------------------------------------------------------------------------

from swapl_exceptions import *
from swapl_isa import *

# -----------------------------------------------------------------------------
class SWAPL_Heap:

    def __init__(self, uParent = None):
        self.parent = uParent
        self.heap = { }

    def __repr__(self):
        return repr(self.heap)

    def get_parent(self):
        return self.parent

    def clone(self):
        cloned = SWAPL_Heap(self.parent)
        for k in self.heap:
            cloned.heap[k] = self.heap[k]
        return cloned

    def push(self):
        h = SWAPL_Heap(self)
        return h

    def pop(self):
        return self.get_parent()

    # ---------------------------------
    def make_var(self, name):
        self.heap[name] = None

    def set_var(self, name, val):
        if name in self.heap:
            self.heap[name] = val
        else:
            if self.parent is not None:
                self.parent.set_var(name, val)
            else:
                raise UndefinedVarException(name)

    def get_var(self, name):
        if name in self.heap:
            return self.heap[name]
        else:
            if self.parent is not None:
                return self.parent.get_var(name)
            else:
                raise UndefinedVarException(name)

# -----------------------------------------------------------------
class SWAPL_Runtime:

    def __init__(self, uProgram, uHeap, uCode, uParams = { 'stacksize' : 50 }):
        self.program = uProgram
        self.stacksize = uParams['stacksize']
        self.heap = uHeap
        self.clear_stack()
        self.code = uCode
        self.agent = None

    def __repr__(self):
        return "ENV: %s\nSTACK : {}\nHEAP : {}".format(self.name,
                                                       repr(self.stack[0:self.stack_pointer]),
                                                       r(self.heap))

    def run(self):
        pc = 0
        while (pc < len(self.code)):
            instr = self.code[pc]
            #print(pc, instr)
            target = instr.execute(pc, self)
            if isinstance(instr, Return):
                return target
            if target is not None:
                pc = target
            else:
                pc += 1
        return None

    def push_heap(self):
        h = SWAPL_Heap(self.heap)
        self.heap = h

    def pop_heap(self):
        self.heap = self.heap.get_parent()

    def get_heap(self):
        return self.heap

    def set_heap(self, h):
        self.heap = h

    def set_agent(self, ag):
        self.agent = ag
        self.agent_object = ag.get_attribute('object')

    def get_program(self):
        return self.program

    def get_agent(self):
        return self.agent

    #def __get_agent_object(self):
    #    return self.agent_object

    #def __set_agent_object(self, ob):
    #    self.agent_object = ob

    def _mk_var(self, uVar):
        return self.heap.make_var(uVar)

    def _get_var(self, uVar):
        if uVar == 'agent':
            return self.agent
        else:
            return self.heap.get_var(uVar)

    def _set_var(self, uVar, uVal):
        self.heap.set_var(uVar, uVal)

    def clear_stack(self):
        self.stack = [ None ] * self.stacksize
        self.stack_pointer = 0

    def status(self):
        print(self)

    def clean(self):
        self.stack_pointer = 0

    def push(self, term):
        self.stack[self.stack_pointer] = term
        self.stack_pointer += 1

    def dup(self):
        self.push(self.last())

    def last(self):
        return self.stack[self.stack_pointer - 1]

    def pop(self):
        self.stack_pointer -= 1
        return self.stack[self.stack_pointer]

    def pop2(self):
        self.stack_pointer -= 2
        return (self.stack[self.stack_pointer+1],
                self.stack[self.stack_pointer])

    def load(self, uVar):
        self.push(self._get_var(uVar))

    def store(self, uVar):
        self._set_var(uVar, self.pop())


