# ------------------------------------------------------------
# Analizador Sintáctico para PHP
# Proyecto de Lenguajes de Programación - Avance 2
# Integrantes: Andrés Salazar (AndresSazalar19, Yadira Suarez (YadiSuarez)
#  Zahid Díaz (LockHurb)
# ------------------------------------------------------------

import ply.yacc as yacc
from lexico import tokens

precedence = (
    ('left', 'OR_OP'),
    ('left', 'XOR_OP'),
    ('left', 'AND_OP'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
)  

def p_programa(p):
    '''programa : programa sentencia
                | sentencia'''

def p_sentencia(p):
    '''sentencia : asigReferencia
                 | varBoolean
                 | expressBol SEMICOLON
                 | varArrayAsociativo
                 | arrayAsociativo SEMICOLON
                 | sentenciaForeach
                 | sentenciaWhile
                 | funcSinRet
                 | varSuperGlobal'''
    
# Asignación por referencia
def p_asigReferencia(p):
    'asigReferencia : VARIABLE ASSIGN AMPERSAND VARIABLE SEMICOLON'
    p[0] = ('asignacion_referencia', p[1], ('referencia', p[4]))

def p_varSuperGlobal(p):
    'varSuperGlobal :  SUPERGLOBALS LBRACKET STRING RBRACKET ASSIGN valor SEMICOLON'
    p[0] = ('asignacion_superGlobal', p[1], p[3], p[6])

def p_varBoolean(p):
    '''varBoolean : VARIABLE ASSIGN expressBol SEMICOLON
                  | VARIABLE ASSIGN VARIABLE SEMICOLON'''
    p[0] = ('asignacion_booleana', p[1], p[3])
    
def p_varArrayAsociativo(p):
    'varArrayAsociativo : VARIABLE ASSIGN arrayAsociativo SEMICOLON' 
    p[0] = ('asignacion_array', p[1], p[3])  

# expresiones booleanas
def p_expressBol(p):
    '''expressBol : operacionComparacion
                  | operacionComparacion operadorLogico expressBol
                  | LPAREN expressBol RPAREN
                  | LPAREN expressBol RPAREN operadorLogico expressBol
                  | NOT_OP expressBol'''
    if len(p) == 2:
        if p[1] == '!':
            p[0] = ('not', p[2])
        else:
            p[0] = p[1]
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    elif len(p) == 4:
        p[0] = (p[2], p[1], p[3]) # Caso: expr operador expr
    elif len(p) == 6:
        p[0] = (p[4], p[2], p[5]) # Caso: (expr) operador expr

def p_operacionComparacion(p):
    '''operacionComparacion : valor operadorCom valor
                            | BOOL_TRUE
                            | BOOL_FALSE'''
    if len(p) == 2:
        p[0] = p[1]  
    else:
        p[0] = (p[2], p[1], p[3])  # ('>', 5, 3)
    
def p_valor(p):
    '''valor : INTEGER
            | FLOAT
            | VARIABLE
            | SUPERGLOBALS
            | STRING'''   
    p[0] = p[1]

def p_operadorCom(p):
    '''operadorCom : EQ
                 | NE
                 | LT
                 | GE
                 | LE
                 | GT'''
    p[0] = p[1]
    
def p_operadorLogico(p):
    '''operadorLogico : AND_OP
                       | OR_OP
                       | XOR_OP'''
    p[0] = p[1]
    
# Array Asociativos
def p_arrayAsociativo(p):
    '''arrayAsociativo : LBRACKET contenidoArray RBRACKET
                        | LBRACKET RBRACKET'''   
    if len(p) == 3:
        p[0] = {} 
    else:
        p[0] = p[2] 

def p_contenidoArray(p):
    '''contenidoArray : valor ARROW valorArray
                        | valor ARROW valorArray COMMA contenidoArray'''    
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    else:
        p[5][p[1]] = p[3]
        p[0] = p[5]

def p_valorArray(p):
    '''valorArray : valor
                | arrayAsociativo'''
    p[0] = p[1]

# Bucle While
def p_sentenciaWhile(p):
    'sentenciaWhile : WHILE LPAREN expressBol RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('while', p[3], p[6])


# Bucle For
def p_sentenciaForeach(p):
    '''sentenciaForeach : FOREACH LPAREN VARIABLE AS VARIABLE RPAREN LBRACE cuerpo RBRACE
                     | FOREACH LPAREN VARIABLE AS VARIABLE ARROW VARIABLE RPAREN LBRACE cuerpo RBRACE
    '''
    if len(p) == 10:
        # foreach ($array as $valor)
        p[0] = ('foreach', p[3], None, p[5], p[8])  # (foreach, array, clave=None, valor, cuerpo)
    else:
        # foreach ($array as $clave => $valor)
        p[0] = ('foreach', p[3], p[5], p[7], p[10])  # (foreach, array, clave, valor, cuerpo)


def p_inicializacion(p):
    '''inicializacion : VARIABLE ASSIGN valor
                      | NULL'''
    p[0] = ('init', p[1], p[3]) if len(p) > 2 else None

def p_incremento(p):
    '''incremento : VARIABLE INCREMENT
                  | VARIABLE DECREMENT
                  | VARIABLE ASSIGN valor
                  | NULL'''
    p[0] = ('inc', p[1], p[2]) if len(p) > 2 else None

def p_cuerpo(p):
    '''cuerpo : sentencia
              | sentencia cuerpo
              | NULL'''
    # Permite múltiples sentencias dentro del bloque
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = [p[1]] + p[2]

def p_funcSinRet(p):
    'funcSinRet : FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('funcion', p[2], p[4], p[7])

def p_parametros(p):
    '''parametros :  VARIABLE
                  | VARIABLE COMMA parametros
                  | NULL'''
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]    

def p_lecturaDatos(p):
    '''lecturaDatos : VARIABLE ASSIGN funcionLectura SEMICOLON'''
    p[0] = ('lectura_datos', p[1], p[3])

def p_funcionLectura(p):
    '''funcionLectura : READLINE LPAREN STRING RPAREN
                      | FGETS LPAREN STDIN RPAREN'''
    if p[1].lower() == 'readline':
        p[0] = ('readline', p[3])   # Ej: readline("Ingresa tu nombre: ")
    else:
        p[0] = ('fgets', 'STDIN')   # Ej: fgets(STDIN)

errores_sintacticos = []
def p_error(p):
    if p:
        mensaje= f"Error de sintaxis en '{p.value}' (tipo {p.type})"
        errores_sintacticos.append(mensaje)
    else:
        print("Error de sintaxis: fin inesperado del archivo")      

# BConstrucción del parser
parser = yacc.yacc()