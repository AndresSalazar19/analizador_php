# variables superglobales, tipos de datos primitivos, operadores, comentarios.
import ply.lex as lex

# Lista de tokens
tokens = [
    'SUPERGLOBAL',
    'INT',
    'FLOAT',
    'STRING',
    'BOOL',
    'NULL',

    # Operadores lógicos
    'AND_OP',
    'OR_OP',
    'NOT_OP',
    'XOR_OP',
]

# Expresiones regulares para los tokens
t_SUPERGLOBAL = r'\$(GLOBALS|\_(GET|POST|SESSION|COOKIE|SERVER|FILES|REQUEST|ENV))'
t_AND_OP = r'&&|\band\b'
t_OR_OP = r'\|\||\bor\b'
t_NOT_OP = r'!|\bnot\b'
t_XOR_OP = r'\bxor\b'

# Reglas para los tokens
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'\b(true|false)\b'
    t.value = True if t.value == 'true' else False
    return t

def t_NULL(t):
    r'\bnull\b'
    t.value = None
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]  # quitamos las comillas
    return t



def t_COMMENT_MULTI(t):
    r'/\*([^*]|\*(?!/))*\*/'
    # Ignorar comentarios multilínea
    pass

def t_COMMENT_LINE(t):
    r'(//|\#)[^\n]*'
    # Ignorar comentarios de línea
    pass

# regla para nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Regla de handling error
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

