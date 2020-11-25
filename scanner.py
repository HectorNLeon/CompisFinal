import ply.lex as lex

import sys

reserved = {
    'Program': 'PROGRAM',
    'var': 'VAR',
    'module': 'MODULE',
    'main': 'MAIN',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void':'VOID',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'do': 'DO',
    'while': 'WHILE',
    'from' : 'FROM',
    'to': 'TO',
    'Line': 'LINE',
    'Point': 'POINT',
    'Circle': 'CIRCLE',
    'Arc': 'ARC',
    'Penup': 'PENUP',
    'Pendown': 'PENDOWN',
    'Color': 'COLOR',
    'Size': 'SIZE',
    'Clear': 'CLEAR'
}

tokens = [
    'ID',
    'C_INT',
    'C_FLOAT',
    'C_STRING',
    'C_CHAR',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'COMMA',
    'SEMICOLON',
    'COLON',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LSBRACKET',
    'RSBRACKET',
    'AND',
    'OR',
    'GREATER_THAN',
    'LESS_THAN',
    'IS_EQUAL',
    'NOT_EQUAL'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LSBRACKET = r'\['
t_RSBRACKET = r'\]'
t_AND = r'\&'
t_OR = r'\|'
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_IS_EQUAL = r'\=\='
t_NOT_EQUAL = r'\!\='

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_C_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_C_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_C_STRING(t):
    r'\"[^"]+\"'
    return t

def t_C_CHAR(t):
    r'\'.\''
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal characters:", t.value)
    t.lexer.skip(1)

lexer = lex.lex()



""" while True:
    try:
        s = input('')
    except EOFError:
        break """