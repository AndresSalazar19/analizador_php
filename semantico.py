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
    """Verifica si una variable existe y es accesible en el ámbito actual"""
    if en_ambito_local():
        if nombre in tabla_simbolos["locales"][-1]:
            return True
        if nombre in tabla_simbolos["globales"]:
            agregar_error(f"variable {nombre} debe ser accedida con $GLOBALS['{nombre}'].")
            return False
        agregar_error(f"variable {nombre} no está definida (uso de variable no declarada).")
        return False
    else:
        if nombre in tabla_simbolos["globales"]:
            return True
        agregar_error(f"variable {nombre} no está definida en el ámbito global (uso de variable no declarada).")
        return False


def tipos_compatibles_aritmetica(tipo1, tipo2):
    """Verifica si dos tipos son compatibles para operaciones aritméticas"""
    tipos_numericos = {'int', 'float'}
    
    # Ambos deben ser numéricos
    if tipo1 in tipos_numericos and tipo2 in tipos_numericos:
        return True
    
    # Tipos incompatibles para aritmética
    return False


def obtener_tipo_resultado_aritmetico(tipo1, tipo2):
    """Determina el tipo resultante de una operación aritmética"""
    if tipo1 == 'float' or tipo2 == 'float':
        return 'float'
    if tipo1 == 'int' and tipo2 == 'int':
        return 'int'
    return 'desconocido'


def analizar_operacion_aritmetica(nodo, operador):
    """Analiza operaciones aritméticas y verifica compatibilidad de tipos"""
    if len(nodo) < 3:
        return 'desconocido'
    
    operando_izq = nodo[1]
    operando_der = nodo[2]
    
    tipo_izq = analizar_valor(operando_izq, verificar_existencia=True)
    tipo_der = analizar_valor(operando_der, verificar_existencia=True)
    
    # Verificar compatibilidad de tipos
    if not tipos_compatibles_aritmetica(tipo_izq, tipo_der):
        agregar_error(
            f"operación aritmética '{operador}' con tipos incompatibles: "
            f"{tipo_izq} {operador} {tipo_der}. "
            f"Solo se permiten operaciones entre int y float."
        )
        return 'desconocido'
    
    return obtener_tipo_resultado_aritmetico(tipo_izq, tipo_der)


def analizar_operacion_comparacion(nodo, operador):
    """Analiza operaciones de comparación"""
    if len(nodo) < 3:
        return 'bool'
    
    operando_izq = nodo[1]
    operando_der = nodo[2]
    
    # Verificar que las variables existen
    analizar_valor(operando_izq, verificar_existencia=True)
    analizar_valor(operando_der, verificar_existencia=True)
    
    return 'bool'


def analizar_valor(nodo, verificar_existencia=True):
    """Analiza y retorna el tipo de un valor o expresión"""
    if isinstance(nodo, tuple):
        tipo_nodo = nodo[0]
        
        # Variable
        if len(nodo) >= 2 and isinstance(nodo[1], str) and nodo[1].startswith('


def verificar_globales(valor):
    if isinstance(valor, tuple) and valor[0] == 'valor' and isinstance(valor[1], tuple):
        superglobal, indice = valor[1][0], "$" + valor[1][1]
        if superglobal == 'GLOBALS':
            if indice not in tabla_simbolos['globales']:
                agregar_error(f"variable {indice} no está definida en GLOBALS.")
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
    else:
        # Analizar expresiones complejas
        tipo_valor = analizar_valor(valor, verificar_existencia=True)
        if en_ambito_local():
            tabla_simbolos['locales'][-1][nombre] = (tipo_valor, None)
        else:
            tabla_simbolos['globales'][nombre] = (tipo_valor, None)


def declaracion_superglobal(nodo):
    nombre = nodo[1]
    indice = "$" + nodo[2]
    valor = nodo[3]

    if nombre == 'GLOBALS':
        if isinstance(valor, tuple) and valor[0] == 'valor':
            dato = valor[1]
            tipo_valor = detectar_tipo(dato)
            tabla_simbolos["globales"][indice] = (tipo_valor, dato)
        else:
            tipo_valor = analizar_valor(valor, verificar_existencia=True)
            tabla_simbolos["globales"][indice] = (tipo_valor, None)


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
            tabla_simbolos['locales'][-1][param[1]] = ('desconocido', None)
        elif param[0] == 'param_default':
            tipo_param = analizar_valor(param[2], verificar_existencia=False)
            tabla_simbolos['locales'][-1][param[1]] = (tipo_param, param[2])

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
    elif tipo in ('if', 'elseif'):
        # Analizar condición
        analizar_valor(nodo[1], verificar_existencia=True)
        # Analizar cuerpo
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for sentencia in nodo[2]:
                analizar(sentencia)
        # Si hay else, analizarlo
        if len(nodo) > 3 and nodo[3]:
            analizar(nodo[3])
    elif tipo == 'else':
        # Analizar cuerpo del else
        if len(nodo) > 1 and isinstance(nodo[1], list):
            for sentencia in nodo[1]:
                analizar(sentencia)
    elif tipo == 'while':
        analizar_valor(nodo[1], verificar_existencia=True)
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for sentencia in nodo[2]:
                analizar(sentencia)
    elif tipo == 'switch':
        # Analizar expresión del switch
        if len(nodo) > 1:
            analizar_valor(nodo[1], verificar_existencia=True)
        # Analizar casos
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for caso in nodo[2]:
                analizar(caso)
    elif tipo == 'case':
        # Analizar valor del caso
        if len(nodo) > 1:
            analizar_valor(nodo[1], verificar_existencia=True)
        # Analizar cuerpo del caso
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for sentencia in nodo[2]:
                analizar(sentencia)
    elif tipo == 'default':
        # Analizar cuerpo del default
        if len(nodo) > 1 and isinstance(nodo[1], list):
            for sentencia in nodo[1]:
                analizar(sentencia)
    elif tipo in ('break', 'continue'):
        # break y continue no requieren análisis adicional
        pass
    elif tipo == 'class':
        # Analizar definición de clase
        # Las clases se manejan de forma básica
        pass
    elif tipo == 'new':
        # Instanciación de objetos
        # new Clase(args)
        pass
    elif tipo == 'return':
        # Analizar valor de retorno
        if len(nodo) > 1 and nodo[1]:
            analizar_valor(nodo[1], verificar_existencia=True)
    elif tipo == 'for':
        # Analizar inicialización, condición, incremento y cuerpo
        # La inicialización del for declara la variable
        if len(nodo) > 1 and nodo[1]:
            analizar(nodo[1])  # inicialización (ej: $i = 1)
        if len(nodo) > 2 and nodo[2]:
            analizar_valor(nodo[2], verificar_existencia=True)  # condición
        if len(nodo) > 3 and nodo[3]:
            analizar(nodo[3])  # incremento
        if len(nodo) > 4 and isinstance(nodo[4], list):
            for sentencia in nodo[4]:
                analizar(sentencia)
    elif tipo in ('incremento', 'decremento', 'post_incremento', 'post_decremento'):
        # Operaciones de incremento/decremento (++, --)
        if len(nodo) > 1:
            analizar_valor(nodo[1], verificar_existencia=True)
    elif tipo == 'asignacion':
        # Asignaciones dentro de expresiones (ej: $i = $i + 1)
        if len(nodo) >= 3:
            nombre_var = nodo[1]
            valor = nodo[2]
            # Si la variable no existe, la creamos
            if not obtener_variable(nombre_var):
                tipo_valor = analizar_valor(valor, verificar_existencia=True)
                if en_ambito_local():
                    tabla_simbolos['locales'][-1][nombre_var] = (tipo_valor, None)
                else:
                    tabla_simbolos['globales'][nombre_var] = (tipo_valor, None)
            else:
                # Si existe, solo verificamos el valor
                analizar_valor(valor, verificar_existencia=True)


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
    return True):
            nombre_var = nodo[1]
            if verificar_existencia:
                if not verificar_acceso_variable(nombre_var):
                    return 'desconocido'
            var_info = obtener_variable(nombre_var)
            return var_info[0] if var_info else 'desconocido'
        
        # Acceso a GLOBALS
        elif len(nodo) >= 2 and isinstance(nodo[1], tuple):
            verificar_globales(nodo)
            if nodo[1][0] == 'GLOBALS':
                indice = "$" + nodo[1][1]
                var_info = tabla_simbolos['globales'].get(indice)
                return var_info[0] if var_info else 'desconocido'
        
        # Operaciones aritméticas
        elif tipo_nodo in ('suma', 'resta', 'multiplicacion', 'division', 'modulo', 'potencia'):
            return analizar_operacion_aritmetica(nodo, tipo_nodo)
        
        # Operaciones de comparación
        elif tipo_nodo in ('mayor_que', 'menor_que', 'mayor_igual', 'menor_igual', 
                          'igual', 'diferente', 'identico', 'no_identico'):
            return analizar_operacion_comparacion(nodo, tipo_nodo)
        
        # Operaciones lógicas
        elif tipo_nodo in ('and', 'or', 'not'):
            return 'bool'
        
        # Concatenación de strings
        elif tipo_nodo == 'concatenacion':
            return 'string'
        
        # Operaciones de incremento/decremento
        elif tipo_nodo in ('incremento', 'decremento', 'post_incremento', 'post_decremento'):
            if len(nodo) > 1:
                return analizar_valor(nodo[1], verificar_existencia)
            return 'int'
        
        # Llamadas a funciones
        elif tipo_nodo == 'llamada_funcion':
            # Por ahora retornamos tipo desconocido
            # Los argumentos se verifican
            if len(nodo) > 2 and isinstance(nodo[2], list):
                for arg in nodo[2]:
                    analizar_valor(arg, verificar_existencia=True)
            return 'desconocido'
        
        # Constantes
        elif tipo_nodo == 'constante':
            nombre_const = nodo[1] if len(nodo) > 1 else None
            if nombre_const and nombre_const in tabla_simbolos['constantes']:
                return tabla_simbolos['constantes'][nombre_const][0]
            return 'desconocido'
    
    return detectar_tipo(nodo)


def verificar_globales(valor):
    if isinstance(valor, tuple) and valor[0] == 'valor' and isinstance(valor[1], tuple):
        superglobal, indice = valor[1][0], "$" + valor[1][1]
        if superglobal == 'GLOBALS':
            if indice not in tabla_simbolos['globales']:
                agregar_error(f"variable {indice} no está definida en GLOBALS.")
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
    else:
        # Analizar expresiones complejas
        tipo_valor = analizar_valor(valor, verificar_existencia=True)
        if en_ambito_local():
            tabla_simbolos['locales'][-1][nombre] = (tipo_valor, None)
        else:
            tabla_simbolos['globales'][nombre] = (tipo_valor, None)


def declaracion_superglobal(nodo):
    nombre = nodo[1]
    indice = "$" + nodo[2]
    valor = nodo[3]

    if nombre == 'GLOBALS':
        if isinstance(valor, tuple) and valor[0] == 'valor':
            dato = valor[1]
            tipo_valor = detectar_tipo(dato)
            tabla_simbolos["globales"][indice] = (tipo_valor, dato)
        else:
            tipo_valor = analizar_valor(valor, verificar_existencia=True)
            tabla_simbolos["globales"][indice] = (tipo_valor, None)


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
            tabla_simbolos['locales'][-1][param[1]] = ('desconocido', None)
        elif param[0] == 'param_default':
            tipo_param = analizar_valor(param[2], verificar_existencia=False)
            tabla_simbolos['locales'][-1][param[1]] = (tipo_param, param[2])

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
    elif tipo in ('if', 'elseif'):
        # Analizar condición
        analizar_valor(nodo[1], verificar_existencia=True)
        # Analizar cuerpo
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for sentencia in nodo[2]:
                analizar(sentencia)
        # Si hay else, analizarlo
        if len(nodo) > 3 and nodo[3]:
            analizar(nodo[3])
    elif tipo == 'else':
        # Analizar cuerpo del else
        if len(nodo) > 1 and isinstance(nodo[1], list):
            for sentencia in nodo[1]:
                analizar(sentencia)
    elif tipo == 'while':
        analizar_valor(nodo[1], verificar_existencia=True)
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for sentencia in nodo[2]:
                analizar(sentencia)
    elif tipo == 'switch':
        # Analizar expresión del switch
        if len(nodo) > 1:
            analizar_valor(nodo[1], verificar_existencia=True)
        # Analizar casos
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for caso in nodo[2]:
                analizar(caso)
    elif tipo == 'case':
        # Analizar valor del caso
        if len(nodo) > 1:
            analizar_valor(nodo[1], verificar_existencia=True)
        # Analizar cuerpo del caso
        if len(nodo) > 2 and isinstance(nodo[2], list):
            for sentencia in nodo[2]:
                analizar(sentencia)
    elif tipo == 'default':
        # Analizar cuerpo del default
        if len(nodo) > 1 and isinstance(nodo[1], list):
            for sentencia in nodo[1]:
                analizar(sentencia)
    elif tipo in ('break', 'continue'):
        # break y continue no requieren análisis adicional
        pass
    elif tipo == 'class':
        # Analizar definición de clase
        # Las clases se manejan de forma básica
        pass
    elif tipo == 'new':
        # Instanciación de objetos
        # new Clase(args)
        pass
    elif tipo == 'return':
        # Analizar valor de retorno
        if len(nodo) > 1 and nodo[1]:
            analizar_valor(nodo[1], verificar_existencia=True)
    elif tipo == 'for':
        # Analizar inicialización, condición, incremento y cuerpo
        # La inicialización del for declara la variable
        if len(nodo) > 1 and nodo[1]:
            analizar(nodo[1])  # inicialización (ej: $i = 1)
        if len(nodo) > 2 and nodo[2]:
            analizar_valor(nodo[2], verificar_existencia=True)  # condición
        if len(nodo) > 3 and nodo[3]:
            analizar(nodo[3])  # incremento
        if len(nodo) > 4 and isinstance(nodo[4], list):
            for sentencia in nodo[4]:
                analizar(sentencia)
    elif tipo in ('incremento', 'decremento', 'post_incremento', 'post_decremento'):
        # Operaciones de incremento/decremento (++, --)
        if len(nodo) > 1:
            analizar_valor(nodo[1], verificar_existencia=True)
    elif tipo == 'asignacion':
        # Asignaciones dentro de expresiones (ej: $i = $i + 1)
        if len(nodo) >= 3:
            nombre_var = nodo[1]
            valor = nodo[2]
            # Si la variable no existe, la creamos
            if not obtener_variable(nombre_var):
                tipo_valor = analizar_valor(valor, verificar_existencia=True)
                if en_ambito_local():
                    tabla_simbolos['locales'][-1][nombre_var] = (tipo_valor, None)
                else:
                    tabla_simbolos['globales'][nombre_var] = (tipo_valor, None)
            else:
                # Si existe, solo verificamos el valor
                analizar_valor(valor, verificar_existencia=True)


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