# ------------------------------------------------------------
# Analizador Sintáctico para PHP
# Proyecto de Lenguajes de Programación - Avance 2
# Integrantes: Andrés Salazar (AndresSalazar19), Yadira Suarez (YadiSuarez)
#              Zahid Díaz (LockHurb)
# ------------------------------------------------------------

import ply.yacc as yacc
from lexico import tokens

# ============================================================
# PRECEDENCIA DE OPERADORES
# Operadores lógicos y aritméticos
# ============================================================
precedence = (
    ('left', 'OR_OP'),
    ('left', 'XOR_OP'),
    ('left', 'AND_OP'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'IDENTICAL'),
    ('left', 'PLUS', 'MINUS', 'DOT'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'NOT_OP'),
    ('right', 'POW'),
)

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def p_programa(p):
    '''programa : programa sentencia
                | sentencia'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[2]] if p[2] else p[1]

# ============================================================
# SENTENCIAS PRINCIPALES
# ============================================================
def p_sentencia(p):
    '''sentencia : asigReferencia
                 | varBoolean
                 | expressBol SEMICOLON
                 | varArrayAsociativo
                 | arrayAsociativo SEMICOLON
                 | sentenciaForeach
                 | sentenciaWhile
                 | sentenciaFor
                 | sentenciaIf
                 | sentenciaSwitch
                 | funciones
                 | varSuperGlobal
                 | lecturaDatos
                 | impresion
                 | declaracionVariable
                 | asignacionExpresion
                 | asignacionCompuesta
                 | asignacionLambda
                 | asignacionThisVar
                 | varArrayMultidimensional
                 | definicionClase
                 | asignacionInstancia
                 | llamadaMetodo SEMICOLON
                 | accesoPropiedad SEMICOLON
                 | PHP_OPEN
                 | PHP_CLOSE
                 | define_stmt
                 | RETURN expresion SEMICOLON
                 | break_stmt
                 | continue_stmt
                 | VARIABLE INCREMENT SEMICOLON
                 | callFunction SEMICOLON
                 | constante'''
    p[0] = p[1]


def p_break_stmt(p):
    'break_stmt : BREAK SEMICOLON'
    p[0] = ('break',)


def p_continue_stmt(p):
    'continue_stmt : CONTINUE SEMICOLON'
    p[0] = ('continue',)

def p_define_stmt(p):
    'define_stmt : DEFINE LPAREN STRING COMMA valor RPAREN SEMICOLON'
    p[0] = ('define', p[3], p[5])

def p_constante(p):
    'constante : CONST ID ASSIGN valor SEMICOLON'
    p[0] = ('Const', p[2], p[4])
# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Asignación por referencia
# ============================================================
def p_asigReferencia(p):
    'asigReferencia : VARIABLE ASSIGN AMPERSAND VARIABLE SEMICOLON'
    p[0] = ('asignacion_referencia', p[1], ('referencia', p[4]))

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Variables superglobales
# ============================================================
def p_varSuperGlobal(p):
    'varSuperGlobal : SUPERGLOBALS LBRACKET STRING RBRACKET ASSIGN expresion SEMICOLON'
    p[0] = ('asignacion_superGlobal', p[1], p[3], p[6])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Variables booleanas
# ============================================================
def p_varBoolean(p):
    '''varBoolean : VARIABLE ASSIGN expressBol SEMICOLON
                  | VARIABLE ASSIGN VARIABLE SEMICOLON'''
    p[0] = ('asignacion_booleana', p[1], p[3])

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# DECLARACIÓN DE VARIABLES (SIMPLE Y MÚLTIPLE)
# ============================================================
def p_declaracionVariable(p):
    '''declaracionVariable : VARIABLE ASSIGN expresion SEMICOLON
                           | listaDeclaraciones SEMICOLON'''
    if len(p) == 5:
        p[0] = ('declaracion', p[1], p[3])
    else:
        p[0] = ('declaraciones_multiples', p[1])

def p_listaDeclaraciones(p):
    '''listaDeclaraciones : VARIABLE ASSIGN expresion COMMA listaDeclaraciones
                          | VARIABLE ASSIGN expresion'''
    if len(p) == 6:
        p[0] = [(p[1], p[3])] + p[5]
    else:
        p[0] = [(p[1], p[3])]
    
# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Asignación a $this->propiedad
# ============================================================
def p_asignacionThisVar(p):
    '''asignacionThisVar : THIS_VAR ASSIGN expresion SEMICOLON
                         | THIS_VAR ASSIGN valor SEMICOLON'''
    p[0] = ('asignacion_this', p[1], p[3])

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# ASIGNACIÓN CON EXPRESIONES O CONDICIONALES
# ============================================================
def p_asignacionExpresion(p):
    '''asignacionExpresion : VARIABLE ASSIGN expresion SEMICOLON
                           | VARIABLE ASSIGN expresionCondicional SEMICOLON'''
    p[0] = ('asignacion', p[1], p[3])

def p_expresionCondicional(p):
    '''expresionCondicional : expressBol'''
    p[0] = p[1]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# EXPRESIONES ARITMÉTICAS CON PRECEDENCIA
# ============================================================
def p_expresion(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | expresion MOD expresion
                 | expresion POW expresion
                 | expresion DOT expresion
                 | LPAREN expresion RPAREN
                 | MINUS expresion %prec UMINUS
                 | valor'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ('uminus', p[2])
    else:
        p[0] = ('valor', p[1])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Arrays asociativos
# ============================================================
def p_varArrayAsociativo(p):
    'varArrayAsociativo : VARIABLE ASSIGN arrayAsociativo SEMICOLON' 
    p[0] = ('asignacion_array', p[1], p[3])

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

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Arrays multidimensionales
# ============================================================

def p_arrayMultidimensional(p):
    '''arrayMultidimensional : LBRACKET contenidoArrayMulti RBRACKET
                             | LBRACKET RBRACKET'''
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]

def p_contenidoArrayMulti(p):
    '''contenidoArrayMulti : elementoArrayMulti
                           | elementoArrayMulti COMMA contenidoArrayMulti'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_elementoArrayMulti(p):
    '''elementoArrayMulti : valor
                          | arrayMultidimensional
                          | arrayAsociativo
                          | funcionLambda'''
    p[0] = p[1]

def p_varArrayMultidimensional(p):
    'varArrayMultidimensional : VARIABLE ASSIGN arrayMultidimensional SEMICOLON'
    p[0] = ('asignacion_array_multi', p[1], p[3])

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Estructura SWITCH-CASE
# ============================================================
def p_sentenciaSwitch(p):
    '''sentenciaSwitch : SWITCH LPAREN expresion RPAREN LBRACE listaCasos RBRACE
                       | SWITCH LPAREN expresion RPAREN LBRACE listaCasos casoDefault RBRACE
                       | SWITCH LPAREN expresion RPAREN LBRACE casoDefault RBRACE'''
    if len(p) == 8:
        if isinstance(p[6], list):
            p[0] = ('switch', p[3], p[6], None)
        else:
            p[0] = ('switch', p[3], [], p[6])
    else:
        p[0] = ('switch', p[3], p[6], p[7])

def p_listaCasos(p):
    '''listaCasos : caso
                  | caso listaCasos'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_caso(p):
    '''caso : CASE valor COLON cuerpo
            | CASE valor COLON cuerpo BREAK SEMICOLON'''
    if len(p) == 5:
        p[0] = ('case', p[2], p[4], False)
    else:
        p[0] = ('case', p[2], p[4], True)

def p_casoDefault(p):
    '''casoDefault : DEFAULT COLON cuerpo
                   | DEFAULT COLON cuerpo BREAK SEMICOLON'''
    if len(p) == 4:
        p[0] = ('default', p[3], False)
    else:
        p[0] = ('default', p[3], True)

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Asignaciones compuestas
# ============================================================
def p_asignacionCompuesta(p):
    '''asignacionCompuesta : VARIABLE PLUS_ASSIGN expresion SEMICOLON
                           | VARIABLE MINUS_ASSIGN expresion SEMICOLON
                           | VARIABLE TIMES_ASSIGN expresion SEMICOLON
                           | VARIABLE DIVIDE_ASSIGN expresion SEMICOLON
                           | VARIABLE CONCAT_ASSIGN expresion SEMICOLON'''
    p[0] = ('asignacion_compuesta', p[2], p[1], p[3])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Expresiones booleanas
# ============================================================
def p_expressBol(p):
    '''expressBol : operacionComparacion
                  | expressBol operadorLogico expressBol
                  | LPAREN expressBol RPAREN
                  | NOT_OP expressBol'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('not', p[2])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])

def p_operacionComparacion(p):
    '''operacionComparacion : valor operadorCom valor
                            | valor
                            | BOOL_TRUE
                            | BOOL_FALSE'''
    if len(p) == 2:
        p[0] = p[1]  
    else:
        p[0] = (p[2], p[1], p[3])

def p_operadorCom(p):
    '''operadorCom : EQ
                   | NE
                   | LT
                   | GE
                   | LE
                   | GT
                   | IDENTICAL'''
    p[0] = p[1]

def p_operadorLogico(p):
    '''operadorLogico : AND_OP
                      | OR_OP
                      | XOR_OP'''
    p[0] = p[1]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# ESTRUCTURA CONDICIONAL IF-ELSEIF-ELSE
# ============================================================
def p_sentenciaIf(p):
    '''sentenciaIf : IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE
                   | IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE ELSE LBRACE cuerpo RBRACE
                   | IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE cadenaElseif
                   | IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE cadenaElseif ELSE LBRACE cuerpo RBRACE'''
    if len(p) == 8:
        # if simple
        p[0] = ('if', p[3], p[6], None, None)
    elif len(p) == 9:
        # if con elseif
        p[0] = ('if', p[3], p[6], p[8], None)
    elif len(p) == 12:
        # if con else
        p[0] = ('if', p[3], p[6], None, p[10])
    else:
        # if con elseif y else
        p[0] = ('if', p[3], p[6], p[8], p[11])

def p_cadenaElseif(p):
    '''cadenaElseif : ELSEIF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE
                    | ELSEIF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE cadenaElseif'''
    if len(p) == 8:
        p[0] = [('elseif', p[3], p[6])]
    else:
        p[0] = [('elseif', p[3], p[6])] + p[8]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# BUCLE FOR
# ============================================================
def p_sentenciaFor(p):
    '''sentenciaFor : FOR LPAREN inicializacion SEMICOLON expressBol SEMICOLON incremento RPAREN LBRACE cuerpo RBRACE'''
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_inicializacion(p):
    '''inicializacion : VARIABLE ASSIGN expresion
                      | VARIABLE ASSIGN valor
                      | '''
    if len(p) > 1:
        p[0] = ('init', p[1], p[3])
    else:
        p[0] = None

def p_incremento(p):
    '''incremento : VARIABLE INCREMENT
                  | VARIABLE DECREMENT
                  | VARIABLE ASSIGN expresion
                  | VARIABLE ASSIGN valor
                  | VARIABLE PLUS_ASSIGN expresion
                  | VARIABLE MINUS_ASSIGN expresion
                  | '''
    if len(p) == 1:
        p[0] = None
    elif len(p) == 3:
        p[0] = ('inc', p[1], p[2])
    else:
        p[0] = ('asig', p[1], p[2], p[3])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Bucle While
# ============================================================
def p_sentenciaWhile(p):
    'sentenciaWhile : WHILE LPAREN expressBol RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('while', p[3], p[6])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Bucle Foreach
# ============================================================
def p_sentenciaForeach(p):
    '''sentenciaForeach : FOREACH LPAREN VARIABLE AS VARIABLE RPAREN LBRACE cuerpo RBRACE
                        | FOREACH LPAREN VARIABLE AS VARIABLE ARROW VARIABLE RPAREN LBRACE cuerpo RBRACE'''
    if len(p) == 10:
        # foreach ($array as $valor)
        p[0] = ('foreach', p[3], None, p[5], p[8])
    else:
        # foreach ($array as $clave => $valor)
        p[0] = ('foreach', p[3], p[5], p[7], p[10])

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# IMPRESIÓN POR PANTALLA (echo)
# ============================================================
def p_impresion(p):
    '''impresion : ECHO expresion SEMICOLON
                 | ECHO STRING SEMICOLON
                 | ECHO listaExpresiones SEMICOLON'''
    if len(p) == 4:
        p[0] = ('echo', p[2])

def p_listaExpresiones(p):
    '''listaExpresiones : expresion COMMA listaExpresiones
                        | expresion'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# FUNCIONES CON RETORNO Y PARÁMETROS OBLIGATORIOS
# ============================================================
def p_funciones(p):
    '''funciones : funcSinRet
                 | funcConRet
                 | funcConRetornoOpcional'''
    p[0] = ('funciones', p[1])

def p_funcSinRet(p):
    'funcSinRet : FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('funcion_sin_retorno', p[2], p[4], p[7])

def p_funcConRet(p):
    'funcConRet : FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpoConRetorno RBRACE'
    p[0] = ('funcion_con_retorno', p[2], p[4], p[7])

def p_cuerpoConRetorno(p):
    '''cuerpoConRetorno : sentencia
                        | sentencia cuerpoConRetorno
                        | RETURN expresion SEMICOLON'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [('return', p[2])]

def p_parametros(p):
    '''parametros : listaParametros
                  | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_listaParametros(p):
    '''listaParametros : parametro
                       | parametro COMMA listaParametros'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parametro(p):
    '''parametro : VARIABLE
                 | VARIABLE ASSIGN valor
                 | VARIABLE ASSIGN expresion'''
    if len(p) == 2:
        p[0] = ('param', p[1], None)
    else:
        p[0] = ('param_default', p[1], p[3])

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Funciones con parámetros opcionales
# ============================================================
def p_funcConRetornoOpcional(p):
    'funcConRetornoOpcional : FUNCTION ID LPAREN parametrosOpcionales RPAREN LBRACE cuerpoConRetorno RBRACE'
    p[0] = ('funcion_parametros_opcionales', p[2], p[4], p[7])

def p_parametrosOpcionales(p):
    '''parametrosOpcionales : listaParametrosOpcionales
                            | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_listaParametrosOpcionales(p):
    '''listaParametrosOpcionales : parametroOpcional
                                 | parametroOpcional COMMA listaParametrosOpcionales'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parametroOpcional(p):
    '''parametroOpcional : VARIABLE
                         | VARIABLE ASSIGN valor'''
    if len(p) == 2:
        p[0] = ('param', p[1], None)
    else:
        p[0] = ('param_default', p[1], p[3])

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Funciones lambda (anónimas)
# ============================================================
def p_funcionLambda(p):
    '''funcionLambda : FUNCTION LPAREN parametros RPAREN USE LPAREN listaVariables RPAREN LBRACE cuerpoConRetorno RBRACE
                     | FUNCTION LPAREN parametros RPAREN LBRACE cuerpoConRetorno RBRACE'''
    if len(p) == 12:
        # Lambda con clausura (use)
        p[0] = ('lambda', p[3], p[7], p[10])
    else:
        # Lambda sin clausura
        p[0] = ('lambda', p[3], None, p[6])

def p_listaVariables(p):
    '''listaVariables : VARIABLE
                      | VARIABLE COMMA listaVariables'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_asignacionLambda(p):
    'asignacionLambda : VARIABLE ASSIGN funcionLambda SEMICOLON'
    p[0] = ('asignacion_lambda', p[1], p[3])

# ============================================================
# APORTE: Zahid Díaz (LockHurb)
# Definición de clases con propiedades y métodos
# ============================================================
def p_definicionClase(p):
    '''definicionClase : CLASS ID LBRACE cuerpoClase RBRACE
                       | CLASS ID EXTENDS ID LBRACE cuerpoClase RBRACE'''
    if len(p) == 6:
        p[0] = ('clase', p[2], None, p[4])
    else:
        p[0] = ('clase', p[2], p[4], p[6])

def p_cuerpoClase(p):
    '''cuerpoClase : elementoClase
                   | elementoClase cuerpoClase
                   | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_elementoClase(p):
    '''elementoClase : propiedad
                     | metodo
                     | constructor'''
    p[0] = p[1]

def p_propiedad(p):
    '''propiedad : visibilidad VARIABLE SEMICOLON
                 | visibilidad VARIABLE ASSIGN valor SEMICOLON'''
    if len(p) == 4:
        p[0] = ('propiedad', p[1], p[2], None)
    else:
        p[0] = ('propiedad', p[1], p[2], p[4])

def p_metodo(p):
    '''metodo : visibilidad FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpo RBRACE
              | visibilidad FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpoConRetorno RBRACE'''
    p[0] = ('metodo', p[1], p[3], p[5], p[8])

def p_constructor(p):
    'constructor : visibilidad FUNCTION CONSTRUCT LPAREN parametros RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('constructor', p[1], p[5], p[8])

def p_visibilidad(p):
    '''visibilidad : PUBLIC
                   | PRIVATE
                   | PROTECTED
                   | '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 'public'  # Por defecto en PHP

def p_instanciaClase(p):
    '''instanciaClase : NEW ID LPAREN argumentos RPAREN
                      | NEW ID LPAREN RPAREN'''
    if len(p) == 6:
        p[0] = ('instancia', p[2], p[4])
    else:
        p[0] = ('instancia', p[2], [])

def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMMA argumentos'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_asignacionInstancia(p):
    'asignacionInstancia : VARIABLE ASSIGN instanciaClase SEMICOLON'
    p[0] = ('asignacion_instancia', p[1], p[3])

def p_accesoPropiedad(p):
    'accesoPropiedad : VARIABLE OBJECT_ARROW ID'
    p[0] = ('acceso_propiedad', p[1], p[3])

def p_llamadaMetodo(p):
    '''llamadaMetodo : VARIABLE OBJECT_ARROW ID LPAREN argumentos RPAREN
                     | VARIABLE OBJECT_ARROW ID LPAREN RPAREN'''
    if len(p) == 7:
        p[0] = ('llamada_metodo', p[1], p[3], p[5])
    else:
        p[0] = ('llamada_metodo', p[1], p[3], [])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Lectura de datos
# ============================================================
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

# ============================================================
# VALORES Y CUERPO
# ============================================================
def p_valor(p):
    '''valor : INTEGER
             | FLOAT
             | VARIABLE
             | THIS_VAR
             | SUPERGLOBALS
             | callObject
             | callFunction
             | callSuperGlobal
             | STRING
             | BOOL_TRUE
             | BOOL_FALSE
             | NULL
             | ID
             | arrayAsociativo
             | arrayMultidimensional
             | array_func'''
    p[0] = p[1]

def p_callSuperGlobal(p):
    'callSuperGlobal : SUPERGLOBALS LBRACKET STRING RBRACKET'
    p[0] = (p[1], p[3])

def p_callFunction(p):
    '''callFunction : ID LPAREN argumentos RPAREN
                    | ID LPAREN RPAREN'''
    # Genera un nodo uniforme: ('llamada_funcion', nombre, [args])
    if len(p) == 5:
        p[0] = ('llamada_funcion', p[1], p[3])
    else:
        p[0] = ('llamada_funcion', p[1], [])
def p_callObject(p):
    'callObject : VARIABLE LBRACKET valor RBRACKET'
    
def p_array_func(p):
    '''array_func : ARRAY LPAREN array_content RPAREN
                  | ARRAY LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = []


def p_array_content(p):
    '''array_content : array_element
                     | array_element COMMA array_content'''
    # array_element returns ('assoc', key, value) or ('value', v)
    if len(p) == 2:
        el = p[1]
        if el[0] == 'assoc':
            p[0] = {el[1]: el[2]}
        else:
            p[0] = [el[1]]
    else:
        first = p[1]
        rest = p[3]
        # rest may be list or dict
        if isinstance(rest, dict):
            if first[0] == 'assoc':
                rest[first[1]] = first[2]
                p[0] = rest
            else:
                # prepend value to dict values as list
                p[0] = [first[1]] + list(rest.values())
        else:
            # rest is list
            if first[0] == 'assoc':
                # convert list to dict and add assoc
                d = {i: v for i, v in enumerate(rest)}
                d[first[1]] = first[2]
                p[0] = d
            else:
                p[0] = [first[1]] + rest


def p_array_element(p):
    '''array_element : valor ARROW valor
                     | valor'''
    if len(p) == 4:
        p[0] = ('assoc', p[1], p[3])
    else:
        p[0] = ('value', p[1])
        
def p_cuerpo(p):
    '''cuerpo : sentencia
              | sentencia cuerpo
              | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = [p[1]] + p[2]

# ============================================================
# MANEJO DE ERRORES
# ============================================================
errores_sintacticos = []

def p_error(p):
    if p:
        mensaje = {
            'tipo': 'SINTÁCTICO',
            'linea': p.lineno,
            'token': p.value,
            'tipo_token': p.type,
            'mensaje': f"Token inesperado '{p.value}' de tipo {p.type}",
            'explicacion': "El token no encaja en ninguna regla gramatical válida en este contexto"
        }
        errores_sintacticos.append(mensaje)
        print(f"Error SINTÁCTICO en línea {p.lineno}:")
        print(f"  → Token inesperado: '{p.value}' (tipo: {p.type})")
        print(f"  → Explicación: {mensaje['explicacion']}")
    else:
        mensaje = {
            'tipo': 'SINTÁCTICO',
            'linea': 'EOF',
            'token': None,
            'mensaje': "Fin inesperado del archivo",
            'explicacion': "El archivo terminó antes de completar una estructura sintáctica válida"
        }
        errores_sintacticos.append(mensaje)
        print(f"Error SINTÁCTICO al final del archivo:")
        print(f"  → {mensaje['mensaje']}")
        print(f"  → Explicación: {mensaje['explicacion']}")

# ============================================================
# CONSTRUCCIÓN DEL PARSER
# ============================================================
parser = yacc.yacc()

# ============================================================
# FUNCIÓN DE ANÁLISIS
# ============================================================
def analizar_sintactico(codigo, debug=False):
    """
    Analiza sintácticamente un código PHP
    """
    global errores_sintacticos
    errores_sintacticos = []
    
    resultado = parser.parse(codigo, debug=debug)
    
    if errores_sintacticos:
        print(f"\n❌ Se encontraron {len(errores_sintacticos)} errores sintácticos:")
        for error in errores_sintacticos:
            print(f"  • {error}")
        return None
    else:
        print("\n✓ Análisis sintáctico completado sin errores")
        return resultado

if __name__ == '__main__':
    codigo_prueba = '''
    $x = 10;
    $y = 20, $z = 30;
    $resultado = $x + $y * 2;
    $condicion = $x > 5 && $y < 10;
    
    $_POST["nombre"] = "Juan";
    
    $array = ["a" => 1, "b" => 2];
    
    if ($x > 5) {
        echo "Mayor que 5";
    } elseif ($x == 5) {
        echo "Igual a 5";
    } else {
        echo "Menor que 5";
    }
    
    for ($i = 0; $i < 10; $i++) {
        echo $i;
    }
    
    while ($x > 0) {
        $x = $x - 1;
    }
    
    foreach ($array as $key => $value) {
        echo $key, $value;
    }
    
    function sumar($a, $b) {
        return $a + $b;
    }
    '''
    
    resultado = analizar_sintactico(codigo_prueba)
    if resultado:
        print("\n✓ Análisis completado exitosamente")