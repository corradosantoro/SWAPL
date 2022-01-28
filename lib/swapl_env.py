# -----------------------------------------------------------------------------
# swapl_env.py
# -----------------------------------------------------------------------------

import importlib
import pathlib
import sys
import threading

from swapl_isa import *
from swapl_runtime import *
from swapl_concurrency import *

# -----------------------------------------------------------------------------
class SWAPL_Program:

    GLOBALS = '__globals__'
    AGENTSET = '__agentset__'
    ROLESET = '__roleset__'
    AGENTATTRSET = '__agentattributes__'
    ENVIRONMENT = '__environment__'

    def __init__(self, uBList):
        self.behaviours = { }
        self.agent_file = None
        self.agents = { }
        for b in uBList:
            self.behaviours[b.get_name()] = b

    def disasm(self):
        for b in self.behaviours.values():
            print(b)

    def set_agent_model(self, m):
        self.agent_file = m

    def run(self):
        self.globals_environment = SWAPL_Heap()
        self.globals_environment.make_var(SWAPL_Program.ROLESET)
        self.globals_environment.make_var(SWAPL_Program.AGENTSET)
        self.globals_environment.make_var(SWAPL_Program.AGENTATTRSET)
        self.globals_environment.make_var(SWAPL_Program.ENVIRONMENT)
        self.globals_runtime = SWAPL_Runtime(self, self.globals_environment, self.behaviours[SWAPL_Program.GLOBALS])
        self.globals_runtime.run_no_parallel()
        #print(self.globals_environment)
        self.create_agents()
        self.main = SWAPL_Runtime(self, self.globals_environment, self.behaviours['main'])
        self.main.run()

    def create_agents(self):
        ag_set = self.globals_environment.get_var(SWAPL_Program.AGENTSET)
        ag_attr_set = self.globals_environment.get_var(SWAPL_Program.AGENTATTRSET)

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
        self.globals_environment.set_var(SWAPL_Program.AGENTSET, Set(list(self.agents.values())))

    def get_agents(self):
        return self.agents

    def get_agent(self, name):
        return self.agents[name]

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

    def __init__(self, uName, uWithList):
        self.name = uName
        self.with_blocks = uWithList

    def __repr__(self):
        s = "----------------------------------------------------------------------\n"
        s += "Behaviour {}\n".format(self.name)
        s += "----------------------------------------------------------------------\n"
        for p in self.with_blocks:
            s += disasm(p)
            s += "\n"
        s += "----------------------------------------------------------------------\n\n"
        return s

    def get_name(self):
        return self.name

    def run_no_parallel(self, runtime):
        for w in self.with_blocks:
            #
            runtime.push_heap()

            pc = 0
            while (pc < len(w)):
                target = w[pc].execute(pc, runtime)
                if target is not None:
                    pc = target
                else:
                    pc += 1
            runtime.pop_heap()

    def run(self, runtime):
        for w in self.with_blocks:
            #
            runtime.push_heap()
            opening = w[0]
            if not(isinstance(opening,ParExecBegin)):
                raise InvalidOpeningInstructionException()

            agent_set = runtime._get_var(SWAPL_Program.AGENTSET)
            func = opening.term
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
                new_runtime = SWAPL_Runtime(runtime.program, runtime.get_heap().clone(), self)
                new_runtime.set_agent(ag)
                th = SWAPL_Thread(ag, new_runtime, w[1:], entering_point, exiting_point)
                th.start()
                thread_list.append(th)

            if opening.join:
                for th in thread_list:
                    th.join()

            runtime.pop_heap()


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

    def __init__(self, agent, runtime, program, entering_point, exiting_point):
        super().__init__()
        self.agent = agent
        self.runtime = runtime
        self.program = program
        self.entering_point = entering_point
        self.exiting_point = exiting_point
        #self.set_daemon(False)

    def run(self):
        self.entering_point.meet()
        pc = 0
        code_stack = [ ]
        current_code = self.program
        while (pc < len(self.program)):
            target = current_code[pc].execute(pc, self.runtime)
            if target is not None:
                pc = target
            else:
                pc += 1
        self.exiting_point.meet()

