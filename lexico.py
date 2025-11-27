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
    'null': 'NULL',
    'echo': 'ECHO',
    'array': 'ARRAY',
    'define': 'DEFINE',
    '__construct': 'CONSTRUCT',
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
    'STRING',            # "texto" o 'texto'
    'PHP_OPEN',          # <?php
    'PHP_CLOSE',         # ?>
    'DOT',               # . (concatenación)
    'COLON',             # :
    'ARROW',             # =>
    'INCREMENT',         # ++
    'DECREMENT',         # --
]

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Componentes: 
# - Variables de instancia ($this->variable)
# - Operadores de asignación compuesta (+=, -=, *=, /=, .=)
# - Palabras reservadas
# - Delimitadores de objetos (->)
# ============================================================

reserved_zahid = {
    'extends': 'EXTENDS',
    'const': 'CONST',
    'use': 'USE',
    'as': 'AS',
    'readline': 'READLINE'
}

#Tokens Zahid
tokens_zahid = [
    'THIS_VAR',  #Variables de instancia
    'OBJECT_ARROW', #Operador para objetos
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'CONCAT_ASSIGN',
]

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Componentes: 
# - Variables superglobales ($GLOBALS, $_GET, $_POST, $_SESSION, $_COOKIE, $_SERVER, $_FILES, $_REQUEST, $_ENV)
# - Tipos de datos primitivos (INTEGER, FLOAT, STRING, NULL, BOOL)
# - Operadores lógicos (AND, OR, NOT, XOR) 
# - Commentarios (//, #, /* */)
# ============================================================

tokens_yadira = [
    'SUPERGLOBALS',  # $GLOBALS, $_GET, $_POST, $_SESSION, $_COOKIE, $_SERVER, $_FILES, $_REQUEST, $_ENV
    'BOOL_TRUE',         # true
    'BOOL_FALSE',         # false
    'INTEGER',           # 123
    'FLOAT',             # 123.45
    'AMPERSAND',        # &

    # Operadores lógicos
    'AND_OP',             # && or 'and'
    'OR_OP',              # || or 'or'
    'NOT_OP',             # '!' or 'not'    
    'XOR_OP',             # 'xor'                # Identificadores
]

# Combinar todas las palabras reservadas
reserved = {**reserved_andres, **reserved_zahid}

# Combinar todos los tokens
tokens = tokens_andres + tokens_yadira + tokens_zahid + list(reserved.values())

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

#Función de variable de instancia
def t_THIS_VAR(t):
    r'\$this->([a-zA-Z_][a-zA-Z0-9_]*)'
    return t

# Operadores de asignación compuesta
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_CONCAT_ASSIGN = r'\.='

# Operadores de incremento/decremento
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# Operador de objetos
t_OBJECT_ARROW = r'->'

# Flecha para arrays asociativos
t_ARROW = r'=>'

# Operadores de comparación (orden importante: === antes que ==)
t_IDENTICAL = r'==='
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'

# Operadores aritméticos
t_POW = r'\*\*'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'

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
t_AMPERSAND = r'&'


# Primero verificar superglobales
def t_SUPERGLOBALS(t):
    r'\$(GLOBALS|_GET|_POST|_SESSION|_COOKIE|_SERVER|_FILES|_REQUEST|_ENV)'
    t.value = t.value[1:]  # quita el símbolo $
    return t

# Variables estándar de PHP
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_AND_OP(t):
    r'&&|\band\b'
    return t

def t_OR_OP(t):
    r'\|\||\bor\b'
    return t

def t_NOT_OP(t):
    r'!(?!=)|\bnot\b'
    return t

def t_XOR_OP(t):
    r'\bxor\b'
    return t

def t_BOOL_TRUE(t):
    r'\btrue\b'
    t.value = True
    return t

def t_BOOL_FALSE(t):
    r'\bfalse\b'
    t.value = False
    return t

# Identificadores (para palabras reservadas)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # Verificar si es palabra reservada
    if t.type == 'BOOL':
        t.value = True if t.value.lower() == 'true' else False
    elif t.type == 'NULL':
        t.value = None
    return t

# Números de punto flotante (va antes que INTEGER)
def t_FLOAT(t):
    r'(\+|-)?\d+\.\d+'
    t.value = float(t.value)
    return t

# Números enteros
def t_INTEGER(t):
    r'(\+|-)?\d+'
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

# Comentarios multilínea
def t_COMMENT_MULTI(t):
    r'/\*([^*]|\*(?!/))*\*/'
    pass # Ignorar

# Comentarios de línea
def t_COMMENT_LINE(t):
    r'(//|\#)[^\n]*'
    # Ignorar comentarios de línea
    pass

# Seguimiento de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Manejo de errores
errores = []
def t_error(t):
    mensaje = (
        f"Error LÉXICO en línea {t.lineno}, columna {t.lexpos}:\n"
        f"  → Caracter ilegal '{t.value[0]}' (código ASCII: {ord(t.value[0])})\n"
        f"  → Explicación: Caracter no reconocido por el analizador léxico"
    )
    print(mensaje)
    errores.append({
        'tipo': 'LÉXICO',
        'linea': t.lineno,
        'columna': t.lexpos,
        'mensaje': f"Caracter ilegal '{t.value[0]}'",
        'explicacion': "Caracter no reconocido por el analizador léxico"
    })
    t.lexer.skip(1)

