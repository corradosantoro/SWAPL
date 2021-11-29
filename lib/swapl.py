
# -----------------------------------------------------------------------------
# swapl.py
# -----------------------------------------------------------------------------

import sys
import os

from optparse import *

VERSION_MAJOR = 0
VERSION_MINOR = 3

from swapl_lex import *

from swapl_exceptions import *
from swapl_types import *
from swapl_isa import *
from swapl_env import *

_pgm = None

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','EEQUAL'),
    ('right','UMINUS'),
    )

# Parsing rules

def p_program(t):
    ' program : agent_model role_set agent_set agent_attr_set b_bodies '
    global _pgm
    bg = SWAPL_Behaviour( SWAPL_Program.GLOBALS, [ t[2] + t[3] + t[4] ] )
    _pgm = SWAPL_Program( t[5] + [ bg ] )
    _pgm.set_agent_model(t[1])

# ------------------------------------------------------

def p_agent_model(t):
    ' agent_model : MODEL STRING SEMICOLON '
    t[0] = t[2]

# ------------------------------------------------------
# role_set
# ------------------------------------------------------
def p_role_set(t):
    ' role_set : ROLESET LPAREN role_set_statement RPAREN SEMICOLON '
    (count, pgm) = t[3]
    t[0] = pgm + [ MkSet(count), Store(SWAPL_Program.ROLESET) ]

def p_role_set_statement_1(t):
    ' role_set_statement : role_set_statement COMMA  role_def '
    (count, pgm) = t[1]
    t[0] = (count + 1, pgm + t[3])

def p_role_set_statement_2(t):
    ' role_set_statement : role_def '
    t[0] = (1, t[1])

def p_role_def(t):
    ' role_def : BEGIN nameval_pairs END '
    (names, pgm) = t[2]
    pgm = pgm + [ MkStruct(names) ]
    t[0] = pgm

# ------------------------------------------------------
# agent_set
# ------------------------------------------------------
def p_agent_set(t):
    ' agent_set : AGENTSET LPAREN role_set_statement RPAREN SEMICOLON '
    (count, pgm) = t[3]
    t[0] = pgm + [ MkSet(count), Store(SWAPL_Program.AGENTSET) ]


# ------------------------------------------------------
# agent_attr_set
# ------------------------------------------------------
def p_agent_attr_set(t):
    ' agent_attr_set : AGENTATTRSET literal_list_set_statement SEMICOLON '
    (count, pgm) = t[2]
    t[0] = pgm + [ MkSet(count), Store(SWAPL_Program.AGENTATTRSET) ]


# ------------------------------------------------------
def p_literal_listset(t):
    'literal_list_set_statement : LPAREN literal_list RPAREN'
    t[0] = t[2]

def p_literal_list_1(t):
    'literal_list : NAME COMMA literal_list'
    (count, pgm) = t[3]
    t[0] = (count + 1, [ Push(t[1]) ] + pgm)

def p_literal_list_2(t):
    'literal_list : NAME'
    t[0] = (1,  [ Push(t[1]) ])

# ------------------------------------------------------
def p_b_bodies_1(t):
    ' b_bodies : b_bodies b_body '
    t[0] = t[1] + t[2]

def p_b_bodies_2(t):
    ' b_bodies : b_body '
    t[0] = t[1]

def p_b_body(t):
    ' b_body : BEHAVIOUR NAME BEGIN with_list END'
    t[0] = [ SWAPL_Behaviour(t[2], t[4]) ]


# ------------------------------------------------------
# assignment
# ------------------------------------------------------
def p_assing_1(t):
    ' assign : VAR NAME EQUAL expr SEMICOLON '
    t[0] = t[4] + [ MkVar(t[2]), Store(t[2]) ]

def p_assing_2(t):
    ' assign : NAME EQUAL expr SEMICOLON '
    t[0] = t[3] + [ Store(t[1]) ]

def p_assing_3(t):
    ' assign : VAR NAME SEMICOLON '
    t[0] = [ MkVar(t[2]) ]

def p_assing_4(t):
    ' assign : NAME DOT NAME EQUAL expr SEMICOLON '
    t[0] = t[5] + [ SetField( (t[1], t[3]) ) ]


# ------------------------------------------------------
# with list
# ------------------------------------------------------
def p_with_list_1(t):
    ' with_list : with_list with_block '
    t[0] = t[1] + [ t[2] ]

def p_with_list_2(t):
    ' with_list : with_block '
    t[0] = [ t[1] ]

# ------------------------------------------------------
# with block
# ------------------------------------------------------
def p_with_block(t):
    ' with_block : WITH with_set BEGIN statements END '
    t[0] = [ ParExecBegin(t[2]) ] + t[4] + [ ParExecEnd() ]

# ------------------------------------------------------
# with set
# ------------------------------------------------------
def p_with_set_1(t):
    ' with_set : ALL '
    t[0] = Set.all

def p_with_set_2(t):
    ' with_set : ONE '
    t[0] = Set.one

# ------------------------------------------------------
# statements
# ------------------------------------------------------
def p_statements_1(t):
    ' statements : statements statement '
    t[0] = t[1] + t[2]

def p_statements_2(t):
    ' statements : statement '
    t[0] = t[1]

def p_statement(t):
    ''' statement : assign
                  | funcall
                  | if_block '''
    t[0] = t[1]

# ------------------------------------------------------
# funcall
# ------------------------------------------------------
def p_funcall(t):
    ' funcall : NAME list_set_statement SEMICOLON '
    (count, pgm) = t[2]
    t[0] = pgm + [ MkOrdSet(count), Call(t[1]) ]

# ------------------------------------------------------
# if
# ------------------------------------------------------
def p_if_1(t):
    ' if_block : IF LPAREN expr RPAREN then_else_statement '
    to_skip = len(t[5])
    t[0] = t[3] + [ Skip( (Skip.NEQ, to_skip) ) ] + t[5]
# ------------------------------------------------------
def p_if_2(t):
    ' if_block : IF LPAREN expr RPAREN then_else_statement ELSE then_else_statement'
    to_skip = len(t[5])
    t[0] = t[3] + [ Skip( (Skip.NEQ, to_skip + 1) ) ] + t[5] + \
      [ Skip( (Skip.UNCONDITIONAL, len(t[7]) ) ) ] + t[7]
# ------------------------------------------------------
def p_then_else_1(t):
    ' then_else_statement : statement '
    t[0] = t[1]
# ------------------------------------------------------
def p_then_else_2(t):
    ' then_else_statement : BEGIN statements END '
    t[0] = t[2]

# ------------------------------------------------------
# expressions
# ------------------------------------------------------

def p_uminus_expr(t):
    'expr : MINUS expr %prec UMINUS'
    #t[0] = ("-", t[2])

def p_p_expr(t):
    'expr : expr PLUS expr'
    t[0] = t[1] + t[3] + [ Add() ]

def p_m_expr(t):
    'expr : expr MINUS expr'
    t[0] = t[1] + t[3] + [ Sub() ]

def p_t_expr(t):
    'expr : expr TIMES expr'
    t[0] = t[1] + t[3] + [ Mul() ]

def p_d_expr(t):
    'expr : expr DIVIDE expr'
    t[0] = t[1] + t[3] + [ Div() ]

def p_eequal(t):
    'expr : expr EEQUAL expr'
    t[0] = t[1] + t[3] + [ Sub() ]

def p_expression_group(t):
    'expr : LPAREN expr RPAREN'
    t[0] = t[2]

def p_set_expr(t):
    'expr : SET list_set_statement'
    (count, pgm) = t[2]
    t[0] = pgm + [ MkSet(count) ]

def p_list_expr(t):
    'expr : LIST list_set_statement'
    (count, pgm)
    t[0] = pgm + [ MkOrdSet(count) ]

# ------------------------------------------------------
def p_listset(t):
    'list_set_statement : LPAREN set_expr_list RPAREN'
    t[0] = t[2]

def p_set_expr_list_1(t):
    'set_expr_list : expr COMMA set_expr_list'
    (count, pgm) = t[3]
    t[0] = (count + 1, t[1] + pgm)

def p_set_expr_list_2(t):
    'set_expr_list : expr'
    t[0] = (1, t[1])
# ------------------------------------------------------

def p_struct(t):
    'expr : BEGIN nameval_pairs END'
    (names, pgm) = t[2]
    pgm = pgm + [ MkStruct(names) ]
    t[0] = pgm

def p_namevals_1(t):
    ' nameval_pairs : nameval_pairs COMMA nameval_pair '
    (names_1, pgm_1) = t[1]
    (names_2, pgm_2) = t[3]
    t[0] = ( names_1 + names_2, pgm_1 + pgm_2)

def p_namevals_2(t):
    ' nameval_pairs : nameval_pair '
    t[0] = t[1]

def p_nameval(t):
    ' nameval_pair : NAME COLON expr '
    t[0] = ( [ t[1] ], t[3] )

# ------------------------------------------------------
def p_val_expr(t):
    'expr : NAME'
    t[0] = [ Load(t[1]) ]

def p_num_expr(t):
    'expr : NUMBER'
    t[0] = [ Push(t[1]) ]

def p_string_expr(t):
    'expr : STRING'
    t[0] = [ Push(t[1]) ]

def p_field_expr(t):
    'expr : NAME DOT NAME'
    t[0] = [ GetField( (t[1], t[3]) ) ]

# ------------------------------------------------------

def p_error(t):
    print("Syntax error at '%s' line %d" % (t.value, t.lexer.lineno))
    sys.exit(1)


import ply.yacc as yacc
parser = yacc.yacc()

usage = "usage: swapl [options] infile.swapl"
opt_parser = OptionParser(usage = usage)
opt_parser.add_option("-v", "--version", action="store_true",
                      dest="version", default=False,
                      help="show version info")
opt_parser.add_option("-s", "--disasm", action="store_true",
                      dest="disasm", default=False,
                      help="show assembly info")
(options, args) = opt_parser.parse_args()
if options.version:
    print("SWAPL - SWarm Agent Programming Language\nScripting system version {}.{}".format(VERSION_MAJOR, VERSION_MINOR))
    sys.exit(0)
if len(args) != 1:
    opt_parser.error("incorrect number of arguments")
if options.disasm:
    filename = sys.argv[2]
else:
    filename = sys.argv[1]


fp = open(filename)
contents = fp.read()
result = parser.parse(contents)
fp.close()

if options.disasm:
    _pgm.disasm()
else:
    _pgm.run()

