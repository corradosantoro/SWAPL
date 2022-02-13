
# -----------------------------------------------------------------------------
# swapl.py
# -----------------------------------------------------------------------------

import sys
import os

import math
import random

from optparse import *

VERSION_MAJOR = 0
VERSION_MINOR = 3

from swapl_lex import *

from swapl_exceptions import *
from swapl_types import *
from swapl_isa import *
from swapl_program import *
from swapl_www import *

_pgm = SWAPL_Program()


precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','EEQUAL'),
    ('right','UMINUS'),
    )

# Parsing rules

def p_program_0(t):
    ' program : headers b_bodies '
    global _pgm
    bg = SWAPL_Behaviour( SWAPL_Program.GLOBALS, t[1] )
    _pgm.add_behaviours( t[2] + [ bg ] )

# ------------------------------------------------------

def p_headers_1(t):
    ' headers : header '
    t[0] = t[1]

def p_headers_2(t):
    ' headers : header headers '
    t[0] = t[1] + t[2]

# ------------------------------------------------------

def p_header_agent_model(t):
    ' header : agent_model '
    global _pgm
    _pgm.set_agent_model(t[1])
    t[0] = []

# ------------------------------------------------------
def p_header_role_set(t):
    ' header : role_set '
    t[0] = t[1]
def p_header_agent_set(t):
    ' header : agent_set '
    t[0] = t[1]
def p_header_agent_attributes(t):
    ' header : agent_attr_set '
    t[0] = t[1]
def p_header_environment(t):
    ' header : environment_def '
    t[0] = t[1]
def p_header_assign(t):
    ' header : assign '
    t[0] = t[1]
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
# environment_def
# ------------------------------------------------------
def p_environment_def(t):
    ' environment_def : ENVIRONMENT LPAREN role_def RPAREN SEMICOLON '
    t[0] = t[3] + [ Store(SWAPL_Program.ENVIRONMENT) ]


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

def p_b_body_1(t):
    ' b_body : BEHAVIOUR NAME BEGIN with_list END'
    t[0] = [ SWAPL_Behaviour(t[2], t[4]) ]


def p_b_body_2(t):
    ' b_body : FUNCTION NAME LPAREN names_list RPAREN BEGIN statements END'
    #print('Function', t[2], t[4])
    t[0] = [ SWAPL_Function(t[2], t[4], t[7]) ]


# ------------------------------------------------------
# names list
# ------------------------------------------------------
def p_names_list_1(t):
    ' names_list : NAME COMMA names_list '
    t[0] = [ t[1] ] + t[3]

def p_name_list_2(t):
    ' names_list : NAME '
    t[0] = [ t[1] ]

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
    t[0] = t[1] + t[2]

def p_with_list_2(t):
    ' with_list : with_block '
    t[0] = t[1]

# ------------------------------------------------------
# with block
# ------------------------------------------------------
def p_with_block_1(t):
    ' with_block : WITH with_set BEGIN statements END '
    t[0] = [ ParExecBegin( (len(t[4]) + 1, t[2]) ) ] + t[4] + [ ParExecEnd() ]

def p_with_block_2(t):
    ' with_block : WITH with_set BEGIN statements END PIPE '
    t[0] = [ ParExecBegin( (len(t[4]) + 1, t[2]), False) ] + t[4] + [ ParExecEnd() ]

# ------------------------------------------------------
# with set
# ------------------------------------------------------
def p_with_set_1(t):
    ' with_set : ALL '
    t[0] = Set.all

def p_with_set_2(t):
    ' with_set : ONE '
    t[0] = Set.one

def p_with_set_3(t):
    ' with_set : ROLES LPAREN string_list RPAREN '
    t[0] = (Set.roles, t[3])

# ------------------------------------------------------
def p_string_list_1(t):
    ' string_list : STRING '
    t[0] = [ t[1] ]

def p_string_list_2(t):
    ' string_list : string_list COMMA STRING '
    t[0] = t[1] + [ t[2] ]

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
                  | proccall
                  | returnstmt
                  | if_block
                  | while_block'''
    t[0] = t[1]

# ------------------------------------------------------
# proccall
# ------------------------------------------------------
def p_proc_call(t):
    ' proccall : NAME list_set_statement SEMICOLON '
    (count, pgm) = t[2]
    t[0] = pgm + [ MkOrdSet(count), Call(t[1]) ]

# ------------------------------------------------------
# funcall
# ------------------------------------------------------
def p_fun_call_1(t):
    ' funcall : NAME list_set_statement '
    (count, pgm) = t[2]
    t[0] = pgm + [ MkOrdSet(count), FunCall(t[1]) ]
# ------------------------------------------------------
def p_fun_call_all(t):
    ' funcall : ALL list_set_statement '
    (count, pgm) = t[2]
    t[0] = pgm + [ MkOrdSet(count), FunCall(t[1]) ]

# ------------------------------------------------------
def p_fun_call_2(t):
    ' funcall : NAME DOT NAME list_set_statement '
    (count, pgm) = t[4]
    t[0] = pgm + [ MkOrdSet(count), FunCall( (t[1], t[3]) ) ]

# ------------------------------------------------------
# returnstmt
# ------------------------------------------------------
def p_returnstmt(t):
    ' returnstmt : RETURN expr SEMICOLON '
    t[0] = t[2] + [ Return() ]

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
# while
# ------------------------------------------------------
def p_while(t):
    ' while_block : WHILE LPAREN expr RPAREN then_else_statement '
    to_skip = len(t[5])
    jump_target = to_skip + 1 + len(t[3]) + 1
    t[0] = t[3] + [ Skip( (Skip.NEQ, to_skip + 1) ) ] + t[5] + \
      [ Skip( (Skip.UNCONDITIONAL, -jump_target) ) ]
# ------------------------------------------------------
# expressions
# ------------------------------------------------------

def p_uminus_expr(t):
    'expr : MINUS expr %prec UMINUS'
    t[0] = t[2] + [ Neg() ]

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

def p_lt(t):
    'expr : expr LT expr'
    t[0] = t[1] + t[3] + [ CmpLT() ]

def p_gt(t):
    'expr : expr GT expr'
    t[0] = t[1] + t[3] + [ CmpGT() ]

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
def p_listset_0(t):
    'list_set_statement : LPAREN RPAREN'
    t[0] = (0, [])

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
def p_fun_expr(t):
    'expr : funcall'
    t[0] = t[1]

def p_pythonlink(t):
    'expr : PYTHONLINK STRING'
    t[0] = [ Push(PythonLink(t[2])) ]

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

def p_true_expr(t):
    'expr : TRUE'
    t[0] = [ Push(1) ]

def p_false_expr(t):
    'expr : FALSE'
    t[0] = [ Push(0) ]

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
opt_parser.add_option("-p", "--port",
                      dest="server_port",
                      default = None,
                      help="show assembly info")
(options, args) = opt_parser.parse_args()
if options.version:
    print("SWAPL - SWarm Agent Programming Language\nScripting system version {}.{}".format(VERSION_MAJOR, VERSION_MINOR))
    sys.exit(0)
if len(args) != 1:
    opt_parser.error("incorrect number of arguments")
filename = 1
if options.disasm:
    filename += 1
if options.server_port is not None:
    filename += 2


#current_path = pathlib.Path(__file__).parent.resolve()
#lib_file = str(current_path) + '/swapllib/all.swapl'
#fp = open(lib_file)
#contents = fp.read()
#fp.close()

fp = open(sys.argv[filename])
contents = fp.read()
result = parser.parse(contents)
fp.close()

if options.disasm:
    _pgm.disasm()
else:
    if options.server_port is not None:
        SWAPLHttpRequestHandler.program = _pgm
        SWAPLHttpServer(int(options.server_port)).start()
    _pgm.run()
    if options.server_port is not None:
        while True:
            import time
            time.sleep(100)

