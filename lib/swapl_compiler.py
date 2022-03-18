# -----------------------------------------------------------------------------
# swapl_compiler.py
# -----------------------------------------------------------------------------

from swapl_program import *

class SWAPL_Compiler:

    parser = None
    include_files = [ ]
    program_parts = [ ]

    program = [ ]

    @classmethod
    def add_include_file(cls, fname):
        cls.include_files.append(fname)

    @classmethod
    def compile(cls, parser, fname):
        cls._compile(parser, fname)
        print(cls.program_parts)
        SWAPL_Compiler.program = cls.program_parts[0][1]

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
            cls._compile(parser, f)
