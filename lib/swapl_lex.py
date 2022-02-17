# -----------------------------------------------------------------------------
# swapl_lex.py
# -----------------------------------------------------------------------------

from swapl_exceptions import *
from swapl_types import *
from swapl_isa import *

reserved = {
    'var' : 'VAR',
    'set' : 'SET',
    'list' : 'LIST',
    'model' : 'MODEL',
    'behaviour' : 'BEHAVIOUR',
    'with' : 'WITH',
    'all' : 'ALL',
    'one' : 'ONE',
    'roles' : 'ROLES',
    'roleset' : 'ROLESET',
    'agentset' : 'AGENTSET',
    'attributes' : 'AGENTATTRSET',
    'environment' : 'ENVIRONMENT',
    'while' : 'WHILE',
    'if' : 'IF',
    'else' : 'ELSE',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    '@pythonlink' : 'PYTHONLINK',
    # 'uavset' : 'UAVSET',
    # 'fun' : 'FUN',
    # 'roles' : 'ROLES',
    # 'this' : 'THIS',
    # 'index' : 'INDEX',
    # 'sync' : 'SYNC',
    }

tokens = list(reserved.values()) + ['SEMICOLON',
                                    'COLON',
                                    'COMMA',
                                    'DOT',
                                    'EQUAL',
                                    'EEQUAL',
                                    'LT',
                                    'GT',
                                    'PLUS',
                                    'MINUS',
                                    'TIMES',
                                    'DIVIDE',
                                    'LPAREN',
                                    'RPAREN',
                                    'NAME',
                                    'NUMBER',
                                    'STRING',
                                    'BEGIN',
                                    'END',
                                    'SUBL',
                                    'SUBR',
                                    'PIPE' ]

# Tokens

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUAL      = r'='
t_EEQUAL     = r'=='
t_LT         = r'<'
t_GT         = r'>'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_COLON      = r':'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_DOT        = r'\.'
t_BEGIN      = r'{'
t_END        = r'}'
t_PIPE       = r'\|'
t_SUBL       = r'\['
t_SUBR       = r'\]'

#def t_BEHAVIOUR(t):
#    r'behaviour'
#    #print('START BEHAVIOUR')
#    SWAPL_Program.start_behaviour()
#    return t

#def t_WITH(t):
#    r'with'
#    #print('START WITH')
#    SWAPL_Program.start_with()
#    return t

def t_STRING(t):
     r'"([^"\n]|(\\"))*"'
     t.value = t.value[1:-1]
     return t

def t_NUMBER(t):
   r'[+-]?([0-9]*[.])?[0-9]+'
   try:
       if t.value.find('.') < 0:
           t.value = int(t.value)
       else:
           t.value = float(t.value)
   except ValueError:
       print("Number value too large %d", t.value)
       t.value = 0
   return t


def t_NAME(t):
    r'@?[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t


# Ignored characters
t_ignore = " \t"

def t_comment(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#def t_eof(t):
#    print("EOF of file")
#    return t

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Give the lexer some input
#lexer.input('fun ffdsfsd ;')

# Tokenize
#while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)
