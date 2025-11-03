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
    'implements': 'IMPLEMENTS',
    'interface': 'INTERFACE',
    'abstract': 'ABSTRACT',
    'final': 'FINAL',
    'const': 'CONST',
    'trait': 'TRAIT',
    'use': 'USE',
    'namespace': 'NAMESPACE',
    'as': 'AS',
    'instanceof': 'INSTANCEOF',
    'throw': 'THROW',
    'try': 'TRY',
    'catch': 'CATCH',
    'finally': 'FINALLY',
    'require': 'REQUIRE',
    'include': 'INCLUDE',
    'require_once': 'REQUIRE_ONCE',
    'include_once': 'INCLUDE_ONCE',
}

#Tokens Zahid
tokens_zahid = [
    'THIS_VAR',  #Variables de instancia
    'OBJECT_OP', #Operador para objetos
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'CONCAT_ASSIGN',
    'BACKSLASH',
]

# ============================================================
# REGLAS DE TOKENS
# ============================================================

#Función de variable de instancia
def t_THIS_VAR(t):
    r'\$this->([a-zA-Z_][a-zA-Z0-9_]*)'
    return t

t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_CONCAT_ASSIGN = r'\.='
t_BACKSLASH = r'\\'
t_OBJECT_OP = r'->'

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
    'INTEGER',           # 123
    'FLOAT',             # 123.45
    'STRING',            # "texto" o 'texto'
    'NULL',              # null
    'BOOL',              # true o false

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
    r'!|\bnot\b'
    return t

def t_XOR_OP(t):
    r'\bxor\b'
    return t

def t_BOOL(t):
    r'\b(true|false)\b'
    t.value = True if t.value.lower() == 'true' else False
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
    mensaje = "Error léxico en línea {t.lineno}, columna {t.lexpos}: Caracter ilegal '{t.value[0]}'"
    print(f"Error léxico en línea {t.lineno}, columna {t.lexpos}: Caracter ilegal '{t.value[0]}'")
    errores.append(mensaje)
    t.lexer.skip(1)

# ============================================================
# CONSTRUCCIÓN DEL LEXER
# ============================================================

lexer = lex.lex()

# ============================================================
# FUNCIÓN PARA GENERAR LOGS
# ============================================================

def generar_log(codigo, integrante, tokens_encontrados, errores, usuario_git):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"lexico-{usuario_git}-{fecha_hora}.txt"
    ruta_log = os.path.join('logs', nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANÁLISIS LÉXICO - PHP\n")
        f.write(f"Integrante: {integrante}\n")
        f.write(f"Usuario GitHub: {usuario_git}\n")
        f.write(f"Fecha y Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("CÓDIGO ANALIZADO:\n")
        f.write("-" * 80 + "\n")
        f.write(codigo)
        f.write("\n" + "-" * 80 + "\n\n")
        
        f.write(f"TOKENS RECONOCIDOS: {len(tokens_encontrados)}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'#':<5} {'TIPO':<20} {'VALOR':<30} {'LÍNEA':<10}\n")
        f.write("-" * 80 + "\n")
        
        for i, tok in enumerate(tokens_encontrados, 1):
            valor_str = str(tok.value)
            if len(valor_str) > 27:
                valor_str = valor_str[:27] + "..."
            f.write(f"{i:<5} {tok.type:<20} {valor_str:<30} {tok.lineno:<10}\n")
        
        if errores:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"ERRORES ENCONTRADOS: {len(errores)}\n")
            f.write("-" * 80 + "\n")
            for error in errores:
                f.write(f"• {error}\n")
        else:
            f.write("\n" + "=" * 80 + "\n")
            f.write("✓ ANÁLISIS COMPLETADO SIN ERRORES LÉXICOS\n")
        
        f.write("=" * 80 + "\n")
        f.write("FIN DEL ANÁLISIS\n")
        f.write("=" * 80 + "\n")
    
    return nombre_log

# ============================================================
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# ============================================================

def analizar_archivo(ruta_archivo, integrante, usuario_git='LockHurb'):

    print("\n" + "=" * 80)
    print(f"ANALIZADOR LÉXICO - PHP")
    print(f"Integrante: {integrante}")
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario: {usuario_git}")
    print("=" * 80 + "\n")
    
    # Leer el archivo
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []
    
    # Analizar el código
    lexer_local = lex.lex() 
    lexer_local.input(codigo)
    tokens_encontrados = []
    errores = []
    
    print("Procesando tokens...\n")
    print(f"{'TIPO':<20} {'VALOR':<35} {'LÍNEA':<10}")
    print("-" * 80)
    
    while True:
        tok = lexer_local.token()
        if not tok:
            break
        
        # Verificar que tok sea un objeto token válido
        if hasattr(tok, 'type') and hasattr(tok, 'value'):
            tokens_encontrados.append(tok)
            
            # Mostrar el token en consola
            valor_str = str(tok.value)
            if len(valor_str) > 32:
                valor_str = valor_str[:32] + "..."
            print(f"{tok.type:<20} {valor_str:<35} {tok.lineno:<10}")
    
    print("\n" + "=" * 80)
    print(f"RESUMEN DEL ANÁLISIS")
    print("-" * 80)
    print(f"Total de tokens reconocidos: {len(tokens_encontrados)}")
    print(f"Total de errores léxicos: {len(errores)}")
    
    # Generar log
    nombre_log = generar_log(codigo, integrante, tokens_encontrados, errores, usuario_git)
    print(f"\n✓ Log generado exitosamente: logs/{nombre_log}")
    print("=" * 80 + "\n")
    
    return tokens_encontrados


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == '__main__':
    usuarios_info = [
        ('tests/algoritmo_andres.php', 'Andrés Salazar', 'AndresSalazar19'),
        ('tests/algoritmo_yadira.php', 'Yadira Suárez', 'YadiSuarez'),
        ('tests/algoritmo_zahid.php', 'Zahid Díaz', 'LockHurb')
    ]

    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        archivo = 'tests/' + archivo if not archivo.startswith('tests/') else archivo
        # Determinar el usuario según el nombre del archivo
        if 'andres' in archivo.lower():
            nombre = 'Andrés Salazar'
            usuario = 'AndresSalazar19'
        elif 'yadira' in archivo.lower():
            nombre = 'Yadira Suárez'
            usuario = 'YadiSuarez'
        elif 'zahid' in archivo.lower():
            nombre = 'Zahid Díaz'
            usuario = 'LockHurb'
        else:
            nombre = 'Desconocido'
            usuario = 'UsuarioGit'
    else:
        # Si no se pasa argumento, usar el primero por defecto
        archivo, nombre, usuario = usuarios_info[2]
        
    print("Ejecutando análisis con archivo")
    print(f"   Archivo: {archivo}")
    print(f"   Usuario: {usuario}\n")

    analizar_archivo(archivo, nombre, usuario)
