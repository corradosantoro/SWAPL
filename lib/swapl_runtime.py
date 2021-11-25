# -----------------------------------------------------------------------------
# swapl_runtime.py
# -----------------------------------------------------------------------------

from swapl_exceptions import *

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

    def __init__(self, uHeap, uBehaviour, uParams = { 'stacksize' : 50 }):
        self.stacksize = uParams['stacksize']
        self.heap = uHeap
        self.clear_stack()
        self.behaviour = uBehaviour
        #self.bifs = { 'swapl_print' : swapl_print }
        self.agent = None

    def __repr__(self):
        return "ENV: %s\nSTACK : {}\nHEAP : {}".format(self.name,
                                                       repr(self.stack[0:self.stack_pointer]),
                                                       r(self.heap))

    def run(self):
        self.behaviour.run(self)

    def run_no_parallel(self):
        self.behaviour.run_no_parallel(self)

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
        self.agent_object = ag.get_field('object')

    def get_agent(self):
        return self.agent

    def get_agent_object(self):
        return self.agent_object

    def _mk_var(self, uVar):
        return self.heap.make_var(uVar)

    def _get_var(self, uVar):
        if uVar == 'this':
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


