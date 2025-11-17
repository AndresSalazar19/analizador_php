# ============================================================
# ANALIZADOR UNIFICADO (LÉXICO o SINTÁCTICO) - PHP
# ============================================================

import os
import sys
import ply.lex as lex
import ply.yacc as yacc
from datetime import datetime
from lexico import tokens   # tu archivo de tokens
from sintactico import parser   # tu analizador sintáctico
from semantico import analizar_programa, errores_semanticos

# ============================================================
# FUNCIÓN PARA GENERAR LOGS
# ============================================================

def generar_log(codigo, integrante, tokens_encontrados, errores_lexicos, errores_sintacticos, errores_semanticos, resultado, usuario_git, modo):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"{modo}-{usuario_git}-{fecha_hora}.txt"
    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("=" * 90 + "\n")
        f.write(f"ANÁLISIS {modo.upper()} - PHP\n")
        f.write(f"Integrante: {integrante}\n")
        f.write(f"Usuario GitHub: {usuario_git}\n")
        f.write(f"Fecha y Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 90 + "\n\n")

        f.write("CÓDIGO ANALIZADO:\n")
        f.write("-" * 90 + "\n")
        f.write(codigo)
        f.write("\n" + "-" * 90 + "\n\n")

        # ---- LÉXICO ----
        if modo in ["lexico", "sintactico"]:
            f.write("═" * 90 + "\n")
            f.write("RESULTADOS DEL ANÁLISIS LÉXICO\n")
            f.write("═" * 90 + "\n")
            f.write(f"Tokens reconocidos: {len(tokens_encontrados)}\n")
            f.write(f"Errores léxicos: {len(errores_lexicos)}\n")
            f.write("-" * 90 + "\n")
            f.write(f"{'#':<5} {'TIPO':<20} {'VALOR':<30} {'LÍNEA':<10}\n")
            f.write("-" * 90 + "\n")

            for i, tok in enumerate(tokens_encontrados, 1):
                valor_str = str(tok.value)
                if len(valor_str) > 27:
                    valor_str = valor_str[:27] + "..."
                f.write(f"{i:<5} {tok.type:<20} {valor_str:<30} {tok.lineno:<10}\n")

            if errores_lexicos:
                f.write("\n" + "-" * 90 + "\n")
                f.write("ERRORES LÉXICOS ENCONTRADOS:\n")
                f.write("-" * 90 + "\n")
                for e in errores_lexicos:
                    f.write(f"• {e}\n")
            else:
                f.write("\n✓ Análisis léxico completado sin errores\n")
            
            f.write("\n")

        # ---- SINTÁCTICO ----
        if modo == "sintactico":
            f.write("═" * 90 + "\n")
            f.write("RESULTADOS DEL ANÁLISIS SINTÁCTICO\n")
            f.write("═" * 90 + "\n")
            
            if errores_sintacticos:
                f.write(f"✗ Se detectaron {len(errores_sintacticos)} errores sintácticos:\n")
                f.write("-" * 90 + "\n")
                for i, e in enumerate(errores_sintacticos, 1):
                    f.write(f"{i}. {e}\n")
                f.write("-" * 90 + "\n")
            else:
                f.write("✓ Análisis sintáctico completado sin errores\n")
                f.write("-" * 90 + "\n")
                f.write("\nÁRBOL SINTÁCTICO GENERADO:\n")
                f.write("-" * 90 + "\n")
                f.write(formatear_arbol(resultado))
                f.write("\n" + "-" * 90 + "\n")

        f.write("\n" + "=" * 90 + "\n")
        f.write("FIN DEL ANÁLISIS\n")
        f.write("=" * 90 + "\n")

                # ---- SEMÁNTICO ----
        if modo == "semantico":
            f.write("═" * 90 + "\n")
            f.write("RESULTADOS DEL ANÁLISIS SEMÁNTICO\n")
            f.write("═" * 90 + "\n")

            if errores_sintacticos:
                f.write("✗ No se realizó análisis semántico porque el AST tiene errores.\n")
            else:
                if errores_semanticos:
                    f.write(f"✗ Se detectaron {len(errores_semanticos)} errores semánticos:\n")
                    f.write("-" * 90 + "\n")
                    for i, e in enumerate(errores_semanticos, 1):
                        f.write(f"{i}. {e}\n")
                    f.write("-" * 90 + "\n")
                else:
                    f.write("✓ Análisis semántico completado sin errores\n")

            f.write("\n")

    return nombre_log

# ============================================================
# FUNCIÓN PARA FORMATEAR EL ÁRBOL SINTÁCTICO
# ============================================================

def formatear_arbol(nodo, nivel=0, prefijo=""):
    """
    Formatea el árbol sintáctico de forma legible
    """
    if nodo is None:
        return ""
    
    indent = "  " * nivel
    resultado = ""
    
    if isinstance(nodo, tuple):
        # Es un nodo con estructura
        if len(nodo) > 0:
            resultado += f"{indent}{prefijo}({nodo[0]}\n"
            for i, hijo in enumerate(nodo[1:], 1):
                es_ultimo = (i == len(nodo) - 1)
                nuevo_prefijo = "└─ " if es_ultimo else "├─ "
                resultado += formatear_arbol(hijo, nivel + 1, nuevo_prefijo)
            resultado += f"{indent})\n"
    elif isinstance(nodo, list):
        # Es una lista de nodos
        resultado += f"{indent}{prefijo}[\n"
        for i, hijo in enumerate(nodo):
            es_ultimo = (i == len(nodo) - 1)
            nuevo_prefijo = "└─ " if es_ultimo else "├─ "
            resultado += formatear_arbol(hijo, nivel + 1, nuevo_prefijo)
        resultado += f"{indent}]\n"
    elif isinstance(nodo, dict):
        # Es un diccionario (para arrays asociativos)
        resultado += f"{indent}{prefijo}{{\n"
        items = list(nodo.items())
        for i, (clave, valor) in enumerate(items):
            es_ultimo = (i == len(items) - 1)
            nuevo_prefijo = "└─ " if es_ultimo else "├─ "
            resultado += f"{indent}  {nuevo_prefijo}{clave} => "
            if isinstance(valor, (dict, list, tuple)):
                resultado += "\n" + formatear_arbol(valor, nivel + 2, "")
            else:
                resultado += f"{valor}\n"
        resultado += f"{indent}}}\n"
    else:
        # Es un valor primitivo
        resultado += f"{indent}{prefijo}{repr(nodo)}\n"
    
    return resultado

# ============================================================
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# ============================================================

def analizar_php(ruta_archivo, integrante, usuario_git='LockHurb', modo='lexico'):
    print("\n" + "=" * 80)
    print(f"ANALIZADOR {modo.upper()} - PHP")
    print(f"Integrante: {integrante}")
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario: {usuario_git}")
    print("=" * 80 + "\n")

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # ====== FASE LÉXICA ======
    print("Iniciando análisis léxico...\n")
    import lexico
    # Reiniciar la lista de errores del módulo léxico (si existe) antes de tokenizar
    if hasattr(lexico, 'errores'):
        try:
            lexico.errores.clear()
        except Exception:
            lexico.errores = []

    lexer_local = lex.lex(module=lexico)
    lexer_local.input(codigo)
    tokens_encontrados = []

    print(f"{'TIPO':<20} {'VALOR':<35} {'LÍNEA':<10}")
    print("-" * 80)
    
    while True:
        tok = lexer_local.token()
        if not tok:
            break
        tokens_encontrados.append(tok)
        
        # Mostrar token en consola
        valor_str = str(tok.value)
        if len(valor_str) > 32:
            valor_str = valor_str[:32] + "..."
        print(f"{tok.type:<20} {valor_str:<35} {tok.lineno:<10}")

    # Obtener errores léxicos generados durante la tokenización
    errores_lexicos = list(lexico.errores) if hasattr(lexico, 'errores') else []

    print("\n" + "-" * 80)
    print(f"✓ Tokens reconocidos: {len(tokens_encontrados)}")
    print(f"✓ Errores léxicos: {len(errores_lexicos)}")

    # Si solo se pide léxico, se termina aquí
    if modo == "lexico":
        nombre_log = generar_log(
            codigo, integrante, tokens_encontrados, errores_lexicos, [], None, usuario_git, modo
        )
        print(f"\n✓ Log léxico generado: logs/{nombre_log}")
        print("=" * 80 + "\n")
        return tokens_encontrados

    # ====== FASE SINTÁCTICA ======
    print("\n" + "=" * 80)
    print("Iniciando análisis sintáctico...\n")
    
    import sintactico
    sintactico.errores_sintacticos.clear()

    # Reiniciar el lexer para el parser
    lexer_local = lex.lex(module=lexico)
    resultado = sintactico.parser.parse(codigo, lexer=lexer_local)
    
    print("\n" + "-" * 80)
    if sintactico.errores_sintacticos:
        print(f"✗ Errores sintácticos encontrados: {len(sintactico.errores_sintacticos)}")
        for i, error in enumerate(sintactico.errores_sintacticos, 1):
            print(f"  {i}. {error}")
    else:
        print("✓ Análisis sintáctico completado sin errores")
        if resultado:
            print("\n✓ Árbol sintáctico generado correctamente")

        # ====== FASE SEMÁNTICA ======
    if modo == "semantico":
        print("\n" + "=" * 80)
        print("Iniciando análisis semántico...\n")

        import semantico
        semantico.errores_semanticos.clear()

        # Ejecutar el analizador semántico usando el AST generado
        if resultado is None:
            print("✗ No se pudo realizar análisis semántico porque el árbol sintáctico es inválido.")
        else:
            print("Procesando AST para análisis semántico...\n")
            semantico.analizar_programa(resultado)

        # Mostrar lista de errores
        if semantico.errores_semanticos:
            print("-" * 80)
            print(f"✗ Errores semánticos encontrados: {len(semantico.errores_semanticos)}")
            for i, e in enumerate(semantico.errores_semanticos, 1):
                print(f"  {i}. {e}")
        else:
            print("✓ Análisis semántico completado sin errores")

    # ====== LOG FINAL ======
    nombre_log = generar_log(
        codigo,
        integrante,
        tokens_encontrados,
        errores_lexicos,
        sintactico.errores_sintacticos,
        semantico.errores_semanticos,
        resultado,
        usuario_git,
         modo
    )

    print(f"\n✓ Log semántico generado: logs/{nombre_log}")
    print("=" * 80 + "\n")
    return resultado

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == '__main__':
    usuarios_info = [
        ('tests/algoritmo_andres.php', 'Andrés Salazar', 'AndresSalazar19'),
        ('tests/algoritmo_yadira.php', 'Yadira Suárez', 'YadiSuarez'),
        ('tests/algoritmo_zahid.php', 'Zahid Díaz', 'LockHurb')
    ]

    # Determinar archivo y modo
    if len(sys.argv) > 2:
        archivo = sys.argv[1]
        archivo = 'tests/' + archivo if not archivo.startswith('tests/') else archivo
        modo = sys.argv[2].lower()  # lexico, sintactico, semantico
    elif len(sys.argv) > 1:
        archivo = sys.argv[1]
        archivo = 'tests/' + archivo if not archivo.startswith('tests/') else archivo
        modo = 'sintactico'  # Por defecto sintáctico si solo se pasa el archivo
    else:
        archivo, nombre, usuario = usuarios_info[0]
        modo = 'semantico'

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

    print(f"\nEjecutando análisis {modo}...")
    print(f"   Archivo: {archivo}")
    print(f"   Usuario: {usuario}")
    
    analizar_php(archivo, nombre, usuario, modo)