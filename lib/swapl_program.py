# -----------------------------------------------------------------------------
# swapl_program.py
# -----------------------------------------------------------------------------

import importlib
import pathlib
import sys
import threading

from swapl_isa import *
from swapl_codelet import *
from swapl_concurrency import *
from swapl_lib import *

# -----------------------------------------------------------------------------
class SWAPL_Program:

    GLOBALS = '__globals__'
    MAIN = 'main'
    AGENTSET = '__agentset__'
    ROLESET = '__roleset__'
    AGENTATTRSET = '__agentattributes__'
    ENVIRONMENT = '__environment__'

    def __init__(self, uBList = []):
        self.behaviours = { }
        self.agent_file = None
        self.agents = { }
        self.add_behaviours(uBList)
        self.globals_heap = SWAPL_Heap()
        self.lib = SWAPL_Lib(self)

    def add_behaviours(self, uBList):
        for b in uBList:
            self.behaviours[b.get_name()] = b

    def disasm(self):
        for b in self.behaviours.values():
            print(b)

    def set_agent_model(self, m):
        self.agent_file = m

    def run(self):
        self.globals_heap.make_var(SWAPL_Program.ROLESET)
        self.globals_heap.make_var(SWAPL_Program.AGENTSET)
        self.globals_heap.make_var(SWAPL_Program.AGENTATTRSET)
        self.globals_heap.make_var(SWAPL_Program.ENVIRONMENT)

        self.behaviours[SWAPL_Program.GLOBALS].run_simple(self, self.globals_heap, True)

        #print(self.globals_heap)
        #sys.exit(1)

        self.create_agents()

        self.behaviours[SWAPL_Program.MAIN].run(self, self.globals_heap)

        #self.globals_runtime = SWAPL_Runtime(self, self.globals_heap, self.behaviours[SWAPL_Program.GLOBALS])
        #self.globals_runtime.run_simple()
        #self.main = SWAPL_Runtime(self, self.globals_heap, self.behaviours['main'])
        #self.main.run()


    def create_agents(self):
        ag_set = self.globals_heap.get_var(SWAPL_Program.AGENTSET)
        ag_attr_set = self.globals_heap.get_var(SWAPL_Program.AGENTATTRSET)

        current_path = pathlib.Path(__file__).parent.resolve()
        sys.path.insert(0, str(current_path) + '/agentlib/')

        self.agent_module = importlib.import_module(self.agent_file)
        for agent in ag_set.items():
            a_name = agent.get_field('name')
            a_role = agent.get_field('role')
            if a_name is None:
                a_spawn = agent.get_field('spawn')
                for i in range(0, a_spawn):
                    new_agent = agent.clone()
                    a_name = 'dynamic-' + str(i)
                    new_agent.set_field('name', a_name)
                    a_obj = self.agent_module.Agent(self, new_agent)
                    new_agent.set_field('object', a_obj)
                    if ag_attr_set is not None:
                        for attribute in ag_attr_set.items():
                            a_obj.export_field(attribute)
                            a_obj.set_field(attribute, None)
                    a_obj.on_create()
                    self.agents[a_name] = new_agent
            else:
                a_obj = self.agent_module.Agent(self, agent)
                agent.set_field('object', a_obj)
                if ag_attr_set is not None:
                    for attribute in ag_attr_set.items():
                        a_obj.export_field(attribute)
                        a_obj.set_field(attribute, None)
                a_obj.on_create()
                self.agents[a_name] = agent
        self.globals_heap.set_var(SWAPL_Program.AGENTSET, Set(list(self.agents.values())))

    def get_agents(self):
        return self.agents

    def get_agent(self, name):
        return self.agents[name]

    def get_environment(self):
        return self.globals_heap.get_var(SWAPL_Program.ENVIRONMENT)

    def get_function(self, name):
        try:
            f = self.behaviours[name]
            if isinstance(f, SWAPL_Function):
                return f
            else:
                return None
        except KeyError:
            return None


# -----------------------------------------------------------------------------
class SWAPL_Behaviour:

    def __init__(self, uName, uCode):
        self.name = uName
        self.code = uCode

    def __repr__(self):
        s = "----------------------------------------------------------------------\n"
        s += "Behaviour {}\n".format(self.name)
        s += "----------------------------------------------------------------------\n"
        s += disasm(self.code)
        s += "----------------------------------------------------------------------\n\n"
        return s

    def get_name(self):
        return self.name

    def run_simple(self, program, heap, do_not_push):
        #
        if do_not_push:
            new_heap = heap
        else:
            new_heap = heap.push()
        runtime = SWAPL_Runtime(program, new_heap, self.code)
        runtime.run()
        if not(do_not_push):
            new_heap.pop()
        return heap

    def run(self, program, heap):
        pc = 0
        while pc < len(self.code):
            #
            heap = heap.push()
            opening = self.code[pc]
            if not(isinstance(opening,ParExecBegin)):
                raise InvalidOpeningInstructionException()

            code_len = opening.get_parexec_size()
            closing = self.code[pc+code_len]
            if not(isinstance(closing,ParExecEnd)):
                raise InvalidClosingInstructionException()

            w = self.code[pc:pc+code_len+1]

            pc = pc + code_len + 1

            agent_set = heap.get_var(SWAPL_Program.AGENTSET)
            func = opening.get_func()
            if type(func) == tuple:
                (func, params) = func
                agent_set = func(agent_set, params)
            else:
                agent_set = func(agent_set)
            #print(agent_set)

            entering_point = MeetingPoint(agent_set.size())
            exiting_point = MeetingPoint(agent_set.size())

            thread_list = [ ]
            for ag in agent_set.items():
                new_runtime = SWAPL_Runtime(program, heap.clone(), w)
                new_runtime.set_agent(ag)
                th = SWAPL_Thread(ag, new_runtime, entering_point, exiting_point)
                th.start()
                thread_list.append(th)

            if opening.join:
                for th in thread_list:
                    th.join()

            heap = heap.pop()


# -----------------------------------------------------------------------------
class SWAPL_Function:

    def __init__(self, uName, uParams, uCode):
        self.name = uName
        self.params = uParams
        self.code = uCode

    def __repr__(self):
        s = "----------------------------------------------------------------------\n"
        s += "Function {}\n".format(self.name)
        s += "----------------------------------------------------------------------\n"
        s += disasm(self.code)
        s += "\n"
        s += "----------------------------------------------------------------------\n\n"
        return s

    def get_name(self):
        return self.name

    def get_params(self):
        return self.params

    def get_code(self):
        return self.code


# -----------------------------------------------------------------------------
class SWAPL_Thread(threading.Thread):

    def __init__(self, agent, runtime, entering_point, exiting_point):
        super().__init__()
        self.agent = agent
        self.runtime = runtime
        self.entering_point = entering_point
        self.exiting_point = exiting_point
        #self.set_daemon(False)

    def run(self):
        self.entering_point.meet()
        self.runtime.run()
        self.exiting_point.meet()

