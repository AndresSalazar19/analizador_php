# ------------------------------------------------------------
# Analizador Semántico para PHP
# Proyecto de Lenguajes de Programación - Avance 2
# Integrantes: Andrés Salazar (AndresSalazar19), Yadira Suarez (YadiSuarez)
#              Zahid Díaz (LockHurb)
# ------------------------------------------------------------

# TABLA DE SÍMBOLOS GENERAL
tabla_simbolos = {
    "globales": {},
    "locales": [],
    "constantes": {}
}

errores_semanticos = []

def agregar_error(mensaje):
    errores_semanticos.append(mensaje)
    print(f"Error semántico: {mensaje}")

def en_ambito_local():
    return len(tabla_simbolos["locales"]) > 0

def entrar_scope_local():
    tabla_simbolos["locales"].append({})

def salir_scope_local():
    tabla_simbolos["locales"].pop()

def detectar_tipo(dato):
    if isinstance(dato, tuple):
        if dato and dato[0] == 'valor':
            return detectar_tipo(dato[1])
        return 'desconocido'

    tipo_map = {
        int: 'int', float: 'float', str: 'string', bool: 'bool',
        type(None): 'null', list: 'array', dict: 'array'
    }
    return tipo_map.get(type(dato), 'desconocido')


def obtener_variable(nombre):
    if en_ambito_local() and nombre in tabla_simbolos["locales"][-1]:
        return tabla_simbolos["locales"][-1][nombre]
    return tabla_simbolos["globales"].get(nombre)


def verificar_acceso_variable(nombre):
    if en_ambito_local():
        if nombre in tabla_simbolos["locales"][-1]:
            return True
        if nombre in tabla_simbolos["globales"]:
            agregar_error(f"variable {nombre} debe ser accedida con $GLOBALS['{nombre}'].\n")
            return False
        agregar_error(f"variable {nombre} no está definida.\n")
        return False
    else:
        if nombre in tabla_simbolos["globales"]:
            return True
        agregar_error(f"variable {nombre} no está definida en el ámbito global.\n")
        return False


def analizar_valor(nodo, verificar_existencia=True):
    if isinstance(nodo, tuple):
        if len(nodo) >= 2 and isinstance(nodo[1], str) and nodo[1].startswith('$'):
            nombre_var = nodo[1]
            if verificar_existencia:
                verificar_acceso_variable(nombre_var)
            var_info = obtener_variable(nombre_var)
            return var_info[0] if var_info else 'desconocido'
        elif len(nodo) >= 2 and isinstance(nodo[1], tuple):
            return verificar_globales(nodo)
    return detectar_tipo(nodo)


def verificar_globales(valor):
    if isinstance(valor, tuple) and valor[0] == 'valor' and isinstance(valor[1], tuple):
        superglobal, indice = valor[1][0], "$" + valor[1][1]
        if superglobal == 'GLOBALS':
            if indice not in tabla_simbolos['globales']:
                agregar_error(f"variable {indice} no está definida en GLOBALS.\n")
            return True
    return False


def declarar_variable(nodo):
    nombre = nodo[1]
    valor = nodo[2]

    if verificar_globales(valor):
        return

    if isinstance(valor, tuple) and valor[0] == 'valor' and not isinstance(valor[1], tuple):
        dato = valor[1]
        tipo_valor = detectar_tipo(dato)
        if en_ambito_local():
            tabla_simbolos['locales'][-1][nombre] = (tipo_valor, dato)
        else:
            tabla_simbolos['globales'][nombre] = (tipo_valor, dato)


def declaracion_superglobal(nodo):
    nombre = nodo[1]
    indice = "$" + nodo[2]
    valor = nodo[3]

    if nombre == 'GLOBALS':
        if isinstance(valor, tuple) and valor[0] == 'valor':
            dato = valor[1]
            tipo_valor = detectar_tipo(dato)
            tabla_simbolos["globales"][indice] = (tipo_valor, dato)


def analizar_define(nodo):
    nombre_constante = nodo[1]
    valor = nodo[2]

    if nombre_constante in tabla_simbolos['constantes']:
        agregar_error(f"Intento de modificar constante '{nombre_constante}'. Las constantes no pueden ser redefinidas.")
        return

    tipo_valor = analizar_valor(valor, verificar_existencia=False)
    tabla_simbolos['constantes'][nombre_constante] = (tipo_valor, valor)


def analizar_funcion(nodo):
    parametros = nodo[2]
    cuerpo = nodo[3]

    entrar_scope_local()

    for param in parametros:
        if param[0] == 'param':
            declarar_variable((param[1], 'desconocido', None))
        elif param[0] == 'param_default':
            tipo_param = analizar_valor(param[2], verificar_existencia=False)
            declarar_variable((param[1], tipo_param, param[2]))

    if isinstance(cuerpo, list):
        for sentencia in cuerpo:
            analizar(sentencia)

    salir_scope_local()


def analizar(nodo):
    if not nodo or not isinstance(nodo, tuple):
        return

    tipo = nodo[0]

    if tipo == 'declaracion':
        declarar_variable(nodo)
    elif tipo == 'declaraciones_multiples':
        for var_name, var_expr in nodo[1]:
            analizar(('declaracion', var_name, var_expr))
    elif tipo == 'asignacion_superGlobal':
        declaracion_superglobal(nodo)
    elif tipo in ('define', 'Const'):
        analizar_define(nodo)
    elif tipo == 'funciones':
        analizar_funcion(nodo[1])
    elif tipo == 'echo':
        contenido = nodo[1]
        if isinstance(contenido, list):
            for expr in contenido:
                analizar_valor(expr, verificar_existencia=True)
        else:
            analizar_valor(contenido, verificar_existencia=True)


def analizar_programa(ast):
    global errores_semanticos
    errores_semanticos = []
    tabla_simbolos['globales'].clear()
    tabla_simbolos['locales'].clear()
    tabla_simbolos['constantes'].clear()

    if not ast:
        return True

    for sentencia in ast:
        if sentencia:
            analizar(sentencia)

    if errores_semanticos:
        print(f"\n{'='*50}")
        print(f"Se encontraron {len(errores_semanticos)} errores semánticos")
        print(f"{'='*50}\n")
        return False

    print(f"\n{'='*50}")
    print("Análisis semántico completado sin errores")
    print(f"{'='*50}\n")
    return True