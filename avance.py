# ------------------------------------------------------------
# Analizador Léxico para PHP
# Proyecto de Lenguajes de Programación - Avance 1
# Integrante: Andrés Salazar (AndresSazalar19)
# ------------------------------------------------------------
import ply.lex as lex
from datetime import datetime
import sys
import os

# ============================================================
# APORTE: Andrés Salazar (AndresSazalar19)
# Componentes: 
# - Variables estándar ($variable)
# - Operadores aritméticos (+, -, *, /, %, **)
# - Operadores de comparación (==, ===, !=, <, >, <=, >=)
# - Palabras reservadas básicas
# - Delimitadores básicos (;, {}, (), [], ,, =)
# - Literales (INTEGER, FLOAT, STRING)
# ============================================================

# Palabras reservadas
reserved_andres = {
    'if': 'IF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'function': 'FUNCTION',
    'class': 'CLASS',
    'new': 'NEW',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'static': 'STATIC',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'echo': 'ECHO',
    'array': 'ARRAY',
    'define': 'DEFINE',
}

# Lista de tokens
tokens_andres = [
    'VARIABLE',           # Variables estándar: $variable
    'ID',                # Identificadores
    'PLUS',              # +
    'MINUS',             # -
    'TIMES',             # *
    'DIVIDE',            # /
    'MOD',               # %
    'POW',               # **
    'EQ',                # ==
    'IDENTICAL',         # ===
    'NE',                # !=
    'LT',                # <
    'GT',                # >
    'LE',                # <=
    'GE',                # >=
    'SEMICOLON',         # ;
    'LBRACE',            # {
    'RBRACE',            # }
    'LPAREN',            # (
    'RPAREN',            # )
    'LBRACKET',          # [
    'RBRACKET',          # ]
    'COMMA',             # ,
    'ASSIGN',            # =
    'INTEGER',           # 123
    'FLOAT',             # 123.45
    'STRING',            # "texto" o 'texto'
    'PHP_OPEN',          # <?php
    'PHP_CLOSE',         # ?>
    'DOT',               # . (concatenación)
    'COLON',             # :
    'ARROW',             # =>
    'INCREMENT',         # ++
    'DECREMENT',         # --
]


# Combinar todas las palabras reservadas
reserved = {**reserved_andres}

# Combinar todos los tokens
tokens = tokens_andres + list(reserved.values())

# ============================================================
# REGLAS DE TOKENS
# ============================================================

# Etiquetas PHP
def t_PHP_OPEN(t):
    r'<\?php'
    return t

def t_PHP_CLOSE(t):
    r'\?>'
    return t

# Operadores de incremento/decremento (antes que PLUS y MINUS)
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# Operadores aritméticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POW = r'\*\*'

# Operadores de comparación (orden importante: === antes que ==)
t_IDENTICAL = r'==='
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'

# Flecha para arrays asociativos
t_ARROW = r'=>'

# Delimitadores básicos
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'
t_ASSIGN = r'='

# Variables estándar de PHP
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Identificadores (para palabras reservadas)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # Verificar si es palabra reservada
    return t

# Números de punto flotante (va antes que INTEGER)
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Números enteros
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Cadenas con comillas dobles
def t_STRING_DOUBLE(t):
    r'"([^"\\]|\\.)*"'
    t.type = 'STRING'
    t.value = t.value[1:-1]  # Remover comillas
    return t

# Cadenas con comillas simples
def t_STRING_SINGLE(t):
    r"'([^'\\]|\\.)*'"
    t.type = 'STRING'
    t.value = t.value[1:-1]  # Remover comillas
    return t


# Seguimiento de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Error léxico en línea {t.lineno}, columna {t.lexpos}: Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)
