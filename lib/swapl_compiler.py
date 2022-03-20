# -----------------------------------------------------------------------------
# swapl_compiler.py
# -----------------------------------------------------------------------------

import os.path
import pathlib

from swapl_program import *

class SWAPL_Compiler:

    parser = None
    include_files = [ ]
    program_parts = [ ]

    program = [ ]

    paths = [ ]

    @classmethod
    def init(cls):
        current_path = pathlib.Path(__file__).parent.resolve()
        cls.paths = [ '.', str(current_path) + '/swapllib' ]


    @classmethod
    def add_include_file(cls, fname):
        cls.include_files.append(fname)

    @classmethod
    def compile(cls, parser, fname):
        cls._compile(parser, fname)
        #print(cls.program_parts)
        cls._merge()
        #SWAPL_Compiler.program = cls.program_parts[0][1]
        #print(cls.program)

    @classmethod
    def _compile(cls, parser, fname):
        fp = open(fname)
        contents = fp.read()
        result = parser.parse(contents)
        fp.close()

        cls.program_parts.append([ fname, SWAPL_Compiler.program ])
        SWAPL_Compiler.program = SWAPL_Program()

        if len(cls.include_files) > 0:
            f = cls.include_files.pop(0)

            for path in cls.paths:
                fullname = path + '/' + f
                if os.path.exists(fullname):
                    cls._compile(parser, fullname)
                    return
            raise SourceFileNotFoundException(f)

    @classmethod
    def _merge(cls):
        final_program = SWAPL_Program()
        # merge globals
        glb = [ ]
        for (fname, p) in cls.program_parts:
            b = p.get_behaviour(SWAPL_Program.GLOBALS)
            glb = glb + b.get_code() + [ Clean() ] # at the end ensure that the stack is clean
            p.del_behaviour(SWAPL_Program.GLOBALS)

        final_program.add_behaviour( SWAPL_Behaviour (SWAPL_Program.GLOBALS, glb) )

        # merge behaviours
        for (fname, p) in cls.program_parts:
            for b in p.get_behaviours():
                if final_program.has_behaviour(b.get_name()):
                    raise RedefinedBehaviourException("Behaviour {} redefined in {}".format(b.get_name(), fname))
                final_program.add_behaviour(b)

        cls.program = final_program
