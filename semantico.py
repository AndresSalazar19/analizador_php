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
    "constantes": {},
    "funciones": {},
    "clases": {}
}

contexto_actual = {
    "en_bucle": 0,
    "en_switch": 0,
    "funcion_actual": None,
    "tipo_retorno": None 
}

errores_semanticos = []

def agregar_error(mensaje, linea=None, contexto=None):
    error = {
        'tipo': 'SEMÁNTICO',
        'linea': linea if linea else 'desconocida',
        'mensaje': mensaje,
        'contexto': contexto
    }
    errores_semanticos.append(error)
    
    # Formatear salida
    print(f"\nError SEMÁNTICO en línea {error['linea']}:")
    print(f"  → {mensaje}")
    if contexto:
        print(f"  → Contexto: {contexto}")

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


def verificar_acceso_variable(nombre, linea=None):
    """Verifica si una variable existe y es accesible en el ámbito actual"""
    if en_ambito_local():
        if nombre in tabla_simbolos["locales"][-1]:
            return True
        if nombre in tabla_simbolos["globales"]:
            agregar_error(
                f"Variable {nombre} debe ser accedida con $GLOBALS['{nombre}']",
                linea,
                "Intento de acceder a variable global desde ámbito local"
            )
            return False
        agregar_error(
            f"Variable {nombre} no está definida (uso de variable no declarada)",
            linea,
            "La variable no existe en el ámbito actual"
        )
        return False
    else:
        if nombre in tabla_simbolos["globales"]:
            return True
        agregar_error(f"Advertencia: variable {nombre} usada antes de ser declarada; asumiendo tipo 'desconocido'.")
        tabla_simbolos['globales'][nombre] = ('desconocido', None)
        return True


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


def analizar_operacion_aritmetica(nodo, operador, linea=None):
    """Analiza operaciones aritméticas y verifica compatibilidad de tipos"""
    if len(nodo) < 3:
        return 'desconocido'
    
    operando_izq = nodo[1]
    operando_der = nodo[2]
    
    tipo_izq = analizar_valor(operando_izq, verificar_existencia=True)
    tipo_der = analizar_valor(operando_der, verificar_existencia=True)
    
    if not tipos_compatibles_aritmetica(tipo_izq, tipo_der):
        agregar_error(
            f"Operación aritmética '{operador}' con tipos incompatibles: {tipo_izq} {operador} {tipo_der}",
            linea,
            "Solo se permiten operaciones aritméticas entre int y float"
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
        if len(nodo) >= 2 and isinstance(nodo[1], str) and nodo[1].startswith('$'):
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
            # Validar existencia y argumentos de la llamada (puede estar dentro de expresiones)
            try:
                analizar_llamada_funcion(nodo)
            except Exception:
                # En caso de forma inesperada, al menos analizar los argumentos
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
                agregar_error(f"Advertencia: variable {indice} no está definida en GLOBALS.")
            return True
    return False


def declarar_variable(nodo):
    nombre = nodo[1]
    valor = nodo[2]

    if en_ambito_local():
        if nombre in tabla_simbolos['locales'][-1]:
            agregar_error(f"Redeclaración de variable {nombre} en el ámbito local.\n")


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

def registrar_funcion(nodo):
    tipo_funcion = nodo[0]
    nombre_funcion = nodo[1]
    parametros = nodo[2]
    
    if nombre_funcion in tabla_simbolos['funciones']:
        agregar_error(f"Redeclaración de función '{nombre_funcion}'. La función ya fue definida.\n")
        return False
    
    tipo_retorno = None
    if tipo_funcion in ['funcion_con_retorno', 'funcion_parametros_opcionales']:
        tipo_retorno = 'mixed'
    
    # Registrar función
    tabla_simbolos['funciones'][nombre_funcion] = {
        'tipo': tipo_funcion,
        'parametros': parametros,
        'tipo_retorno': tipo_retorno,
        'definida': True
    }
    
    return True

def analizar_funcion(nodo):
    tipo_funcion = nodo[0]
    nombre_funcion = nodo[1]
    parametros = nodo[2]
    cuerpo = nodo[3]
    
    # Registrar la función si no existe
    if nombre_funcion not in tabla_simbolos['funciones']:
        if not registrar_funcion(nodo):
            return
    
    # Establecer contexto de función actual
    contexto_actual['funcion_actual'] = nombre_funcion
    
    # Si es función con retorno, marcar que esperamos un retorno
    if tipo_funcion in ['funcion_con_retorno', 'funcion_parametros_opcionales']:
        contexto_actual['tipo_retorno'] = 'esperado'
        tiene_retorno = False
    else:
        contexto_actual['tipo_retorno'] = None

    entrar_scope_local()

    for param in parametros:
        if param[0] == 'param':
            if param[1] in tabla_simbolos['locales'][-1]:
                agregar_error(f"Redeclaración de parámetro '{param[1]}' en función '{nombre_funcion}'.\n")
            else:
                tabla_simbolos['locales'][-1][param[1]] = ('desconocido', None)
        elif param[0] == 'param_default':
            if param[1] in tabla_simbolos['locales'][-1]:
                agregar_error(f"Redeclaración de parámetro '{param[1]}' en función '{nombre_funcion}'.\n")
            else:
                tipo_param = analizar_valor(param[2], verificar_existencia=False)
                tabla_simbolos['locales'][-1][param[1]] = (tipo_param, param[2])

    def contiene_return(obj):
        """Busca recursivamente una sentencia 'return' dentro de la estructura."""
        if isinstance(obj, tuple):
            if obj and obj[0] == 'return':
                return True
            for item in obj[1:]:
                if contiene_return(item):
                    return True
            return False
        elif isinstance(obj, list):
            for item in obj:
                if contiene_return(item):
                    return True
            return False
        return False

    if isinstance(cuerpo, list):
        for sentencia in cuerpo:
            analizar(sentencia)

        if tipo_funcion in ['funcion_con_retorno', 'funcion_parametros_opcionales']:
            tiene_retorno = contiene_return(cuerpo)

    if tipo_funcion == 'funcion_con_retorno' and not tiene_retorno:
        agregar_error(f"Advertencia: La función '{nombre_funcion}' no parece contener 'return'.")

    salir_scope_local()
    
    contexto_actual['funcion_actual'] = None
    contexto_actual['tipo_retorno'] = None

def verificar_llamada_funcion(nombre_funcion):

    if nombre_funcion not in tabla_simbolos['funciones']:
        agregar_error(f"Uso de función no definida '{nombre_funcion}'.\n")
        return False
    return True


def analizar_llamada_funcion(nodo):
    # Soporta dos formas de nodo:
    # ('llamada_funcion', nombre, [args...])  -- forma producida por el parser actual
    # (nombre, [args...])                     -- forma legacy
    if not isinstance(nodo, tuple):
        return

    # Determinar nombre y argumentos según la forma
    if len(nodo) >= 1 and nodo[0] == 'llamada_funcion':
        nombre_funcion = nodo[1] if len(nodo) > 1 else None
        argumentos = nodo[2] if len(nodo) > 2 else []
    else:
        # Fallback: primer elemento como nombre
        nombre_funcion = nodo[0]
        argumentos = nodo[1] if len(nodo) > 1 else []

    if not nombre_funcion or not isinstance(nombre_funcion, str):
        return

    # Analizar argumentos (existencia/tipos básicos)
    if isinstance(argumentos, list):
        for arg in argumentos:
            analizar_valor(arg, verificar_existencia=True)
    else:
        # Si argumentos vienen como único valor
        if argumentos:
            analizar_valor(argumentos, verificar_existencia=True)

    # Verificar existencia de la función
    verificar_llamada_funcion(nombre_funcion)

    # Si la función está registrada, comprobar número de parámetros
    if nombre_funcion in tabla_simbolos['funciones']:
        funcion_info = tabla_simbolos['funciones'][nombre_funcion]
        parametros = funcion_info.get('parametros', [])

        params_obligatorios = sum(1 for p in parametros if p[0] == 'param')
        params_totales = len(parametros)

        if isinstance(argumentos, list):
            num_args = len(argumentos)
        else:
            num_args = 1 if argumentos else 0

        if num_args < params_obligatorios:
            agregar_error(f"La función '{nombre_funcion}' espera al menos {params_obligatorios} argumentos, se proporcionaron {num_args}.\n")
        elif num_args > params_totales:
            agregar_error(f"La función '{nombre_funcion}' espera máximo {params_totales} argumentos, se proporcionaron {num_args}.\n")


def analizar_break_continue(nodo):

    tipo = nodo[0]
    
    if tipo == 'break':
        if contexto_actual['en_bucle'] == 0 and contexto_actual['en_switch'] == 0:
            agregar_error("Sentencia 'break' fuera de contexto. Debe estar dentro de un bucle o switch.\n")
    elif tipo == 'continue':
        if contexto_actual['en_bucle'] == 0:
            agregar_error("Sentencia 'continue' fuera de contexto. Debe estar dentro de un bucle.\n")


def analizar_return(nodo):

    if contexto_actual['funcion_actual'] is None:
        agregar_error("Sentencia 'return' fuera de una función.\n")
        return
    
    if len(nodo) > 1:
        valor_retorno = nodo[1]
        tipo_retorno = analizar_valor(valor_retorno)
        
        if contexto_actual['funcion_actual'] in tabla_simbolos['funciones']:
            funcion_info = tabla_simbolos['funciones'][contexto_actual['funcion_actual']]
            tipo_esperado = funcion_info.get('tipo_retorno')
            
            if tipo_esperado and tipo_esperado != 'mixed':
                if tipo_retorno != tipo_esperado and tipo_retorno != 'desconocido':
                    agregar_error(f"Tipo de retorno incorrecto en función '{contexto_actual['funcion_actual']}'. "
                                  f"Se esperaba '{tipo_esperado}', se retornó '{tipo_retorno}'.\n")


def analizar_estructura_control(nodo):

    tipo = nodo[0]
    
    if tipo == 'if':
        condicion = nodo[1]
        cuerpo_if = nodo[2]
        elseifs = nodo[3] if len(nodo) > 3 else None
        cuerpo_else = nodo[4] if len(nodo) > 4 else None
        
        analizar_valor(condicion)

        if isinstance(cuerpo_if, list):
            for sentencia in cuerpo_if:
                analizar(sentencia)
        
        if elseifs:
            for elseif in elseifs:
                if elseif[0] == 'elseif':
                    analizar_valor(elseif[1]) 
                    if isinstance(elseif[2], list):
                        for sentencia in elseif[2]:
                            analizar(sentencia)
        
        if cuerpo_else and isinstance(cuerpo_else, list):
            for sentencia in cuerpo_else:
                analizar(sentencia)
    
    elif tipo in ['while', 'for', 'foreach']:
        contexto_actual['en_bucle'] += 1
        
        if tipo == 'while':
            condicion = nodo[1]
            cuerpo = nodo[2]
            analizar_valor(condicion)
        elif tipo == 'for':
            init = nodo[1]
            condicion = nodo[2]
            incremento = nodo[3]
            cuerpo = nodo[4]
            if init:
                declarar_variable(init)
            if condicion:
                analizar_valor(condicion)
            if incremento:
                analizar(incremento)
        elif tipo == 'foreach':
            array_var = nodo[1]
            key_var = nodo[2]
            value_var = nodo[3]
            cuerpo = nodo[4]
            
            verificar_acceso_variable(array_var)
            
            entrar_scope_local()
            if key_var:
                tabla_simbolos['locales'][-1][key_var] = ('mixed', None)
            tabla_simbolos['locales'][-1][value_var] = ('mixed', None)
        
        if isinstance(cuerpo, list):
            for sentencia in cuerpo:
                analizar(sentencia)
        
        if tipo == 'foreach':
            salir_scope_local()
        
        contexto_actual['en_bucle'] -= 1
    
    elif tipo == 'switch':
        contexto_actual['en_switch'] += 1
        
        expresion = nodo[1]
        casos = nodo[2] if len(nodo) > 2 else []
        default = nodo[3] if len(nodo) > 3 else None
        
        for caso in casos:
            if caso[0] == 'case':
                valor_caso = caso[1]
                cuerpo_caso = caso[2]
                analizar_valor(valor_caso, verificar_existencia=False)
                if isinstance(cuerpo_caso, list):
                    for sentencia in cuerpo_caso:
                        analizar(sentencia)
        
        if default and default[0] == 'default':
            cuerpo_default = default[1]
            if isinstance(cuerpo_default, list):
                for sentencia in cuerpo_default:
                    analizar(sentencia)
        
        contexto_actual['en_switch'] -= 1


def analizar_clase(nodo):
    nombre_clase = nodo[1]
    clase_padre = nodo[2]
    cuerpo = nodo[3]
    existing = tabla_simbolos['clases'].get(nombre_clase)
    if existing and not existing.get('__pre_registered__', False):
        agregar_error(f"Redeclaración de clase '{nombre_clase}'. La clase ya fue definida.\n")
        return
    
    if clase_padre and clase_padre not in tabla_simbolos['clases']:
        agregar_error(f"La clase '{nombre_clase}' intenta heredar de '{clase_padre}' que no está definida.\n")

    tabla_simbolos['clases'][nombre_clase] = {
        'padre': clase_padre,
        'propiedades': {},
        'metodos': {}
    }
    
    if isinstance(cuerpo, list):
        for elemento in cuerpo:
            if elemento[0] == 'propiedad':
                visibilidad = elemento[1]
                nombre_prop = elemento[2]
                valor = elemento[3] if len(elemento) > 3 else None
                
                if nombre_prop in tabla_simbolos['clases'][nombre_clase]['propiedades']:
                    agregar_error(f"Redeclaración de propiedad '{nombre_prop}' en clase '{nombre_clase}'.\n")
                else:
                    tabla_simbolos['clases'][nombre_clase]['propiedades'][nombre_prop] = {
                        'visibilidad': visibilidad,
                        'tipo': analizar_valor(valor, verificar_existencia=False) if valor else 'mixed'
                    }
            
            elif elemento[0] in ['metodo', 'constructor']:
                visibilidad = elemento[1]
                nombre_metodo = '__construct' if elemento[0] == 'constructor' else elemento[2]
                
                if nombre_metodo in tabla_simbolos['clases'][nombre_clase]['metodos']:
                    agregar_error(f"Redeclaración de método '{nombre_metodo}' en clase '{nombre_clase}'.\n")
                else:
                    tabla_simbolos['clases'][nombre_clase]['metodos'][nombre_metodo] = {
                        'visibilidad': visibilidad,
                        'tipo': elemento[0]
                    }

def extraer_variables_for(nodo):
    variables = []
    if isinstance(nodo, tuple):
        if len(nodo) >= 2 and isinstance(nodo[1], str) and nodo[1].startswith('$'):
            variables.append(nodo[1])
        elif nodo[0] in ('asignacion', 'declaracion'):
            if len(nodo) >= 2 and isinstance(nodo[1], str):
                variables.append(nodo[1])
    elif isinstance(nodo, list):
        for item in nodo:
            variables.extend(extraer_variables_for(item))
    return variables


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
    elif tipo in ['funcion_sin_retorno', 'funcion_con_retorno', 'funcion_parametros_opcionales']:
        analizar_funcion(nodo)
    elif tipo == 'echo':
        contenido = nodo[1]
        if isinstance(contenido, list):
            for expr in contenido:
                analizar_valor(expr, verificar_existencia=True)
        else:
            analizar_valor(contenido, verificar_existencia=True)
    elif tipo in ['break', 'continue']:
        analizar_break_continue(nodo)
    elif tipo == 'return':
        analizar_return(nodo)
    elif tipo in ['if', 'while', 'for', 'foreach', 'switch']:
        analizar_estructura_control(nodo)
    elif tipo == 'clase':
        analizar_clase(nodo)
    elif tipo == 'llamada_funcion':
        analizar_llamada_funcion(nodo)
    elif tipo == 'callFunction':
        # Verificar llamada a función
        if len(nodo) > 0:
            verificar_llamada_funcion(nodo[0])
    elif tipo == 'asignacion_instancia':
        nombre_var = nodo[1]
        instancia = nodo[2]
        if instancia[0] == 'instancia':
            nombre_clase = instancia[1]
            # Verificar que la clase existe
            if nombre_clase not in tabla_simbolos['clases']:
                agregar_error(f"Intento de instanciar clase no definida '{nombre_clase}'.\n")
            else:
                # Registrar la variable con el tipo de la clase
                if en_ambito_local():
                    tabla_simbolos['locales'][-1][nombre_var] = (nombre_clase, None)
                else:
                    tabla_simbolos['globales'][nombre_var] = (nombre_clase, None)
    elif tipo in ('incremento', 'decremento', 'post_incremento', 'post_decremento'):
        # Operaciones de incremento/decremento
        if len(nodo) > 1:
            variable = nodo[1]
            if isinstance(variable, str) and variable.startswith('$'):
                if not obtener_variable(variable):
                    verificar_acceso_variable(variable)
            else:
                analizar_valor(variable, verificar_existencia=True)
    elif tipo == 'asignacion':
        # Asignaciones dentro de expresiones
        if len(nodo) >= 3:
            nombre_var = nodo[1]
            valor = nodo[2]
            
            var_existe = obtener_variable(nombre_var) is not None
            tipo_valor = analizar_valor(valor, verificar_existencia=True)
            
            if not var_existe:
                if en_ambito_local():
                    tabla_simbolos['locales'][-1][nombre_var] = (tipo_valor, None)
                else:
                    tabla_simbolos['globales'][nombre_var] = (tipo_valor, None)
    elif tipo == 'asignacion_array':
        nombre = nodo[1]
        if en_ambito_local():
            tabla_simbolos['locales'][-1][nombre] = ('array', None)
        else:
            tabla_simbolos['globales'][nombre] = ('array', None)
        

def analizar_programa(ast):
    global errores_semanticos
    errores_semanticos = []
    tabla_simbolos['globales'].clear()
    tabla_simbolos['locales'].clear()
    tabla_simbolos['constantes'].clear()
    tabla_simbolos['funciones'].clear()
    tabla_simbolos['clases'].clear()

    contexto_actual['en_bucle'] = 0
    contexto_actual['en_switch'] = 0
    contexto_actual['funcion_actual'] = None
    contexto_actual['tipo_retorno'] = None

    if not ast:
        return True

    for sentencia in ast:
        if sentencia:
            if isinstance(sentencia, tuple):
                if sentencia[0] == 'funciones' and len(sentencia) > 1:
                    funcion = sentencia[1]
                    if isinstance(funcion, tuple) and len(funcion) >= 4:
                        registrar_funcion(funcion)
                elif sentencia[0] in ['funcion_sin_retorno', 'funcion_con_retorno', 'funcion_parametros_opcionales']:
                    registrar_funcion(sentencia)
                elif sentencia[0] == 'clase':
                    # Pre-registrar clase para permitir referencias circulares
                    nombre_clase = sentencia[1]
                    if nombre_clase not in tabla_simbolos['clases']:
                        tabla_simbolos['clases'][nombre_clase] = {
                            '__pre_registered__': True,
                            'padre': None,
                            'propiedades': {},
                            'metodos': {}
                        }

    for sentencia in ast:
        if sentencia:
            analizar(sentencia)

    if errores_semanticos:
        print(f"\n{'='*50}")
        print(f"Se encontraron {len(errores_semanticos)} errores semánticos")
        print(f"{'='*50}\n")
        for i, error in enumerate(errores_semanticos, 1):
            print(f"{i}. {error}")
        return False

    print(f"\n{'='*50}")
    print("Análisis semántico completado sin errores")
    print(f"{'='*50}")
    print(f"Variables globales: {len(tabla_simbolos['globales'])}")
    print(f"Funciones definidas: {len(tabla_simbolos['funciones'])}")
    print(f"Clases definidas: {len(tabla_simbolos['clases'])}")
    print(f"Constantes definidas: {len(tabla_simbolos['constantes'])}")
    print(f"{'='*50}\n")
    return True