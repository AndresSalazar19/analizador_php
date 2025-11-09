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

# ============================================================
# FUNCIÓN PARA GENERAR LOGS
# ============================================================

def generar_log(codigo, integrante, tokens_encontrados, errores_lexicos, errores_sintacticos, resultado, usuario_git, modo):
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
            f.write("RESULTADOS DEL ANÁLISIS LÉXICO\n")
            f.write("-" * 90 + "\n")
            f.write(f"Tokens reconocidos: {len(tokens_encontrados)}\n")
            f.write(f"Errores léxicos: {len(errores_lexicos)}\n")
            f.write("-" * 90 + "\n")

            for i, tok in enumerate(tokens_encontrados, 1):
                valor_str = str(tok.value)
                if len(valor_str) > 25:
                    valor_str = valor_str[:25] + "..."
                f.write(f"{i:<4} {tok.type:<15} {valor_str:<28} Línea: {tok.lineno}\n")

            if errores_lexicos:
                f.write("\nERRORES LÉXICOS:\n")
                for e in errores_lexicos:
                    f.write(f"• {e}\n")
            f.write("\n")

        # ---- SINTÁCTICO ----
        if modo == "sintactico":
            f.write("RESULTADOS DEL ANÁLISIS SINTÁCTICO\n")
            f.write("-" * 90 + "\n")
            if errores_sintacticos:
                f.write(f"✗ Se detectaron {len(errores_sintacticos)} errores sintácticos:\n")
                for e in errores_sintacticos:
                    f.write(f"• {e}\n")
            else:
                f.write("✓ Análisis sintáctico completado sin errores\n")
                f.write(f"\nÁrbol sintáctico generado:\n{resultado}\n")

        f.write("=" * 90 + "\nFIN DEL ANÁLISIS\n" + "=" * 90 + "\n")

    return nombre_log

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
    import lexico
    lexer_local = lex.lex(module=lexico)
    lexer_local.input(codigo)
    tokens_encontrados = []
    errores_lexicos = []

    while True:
        tok = lexer_local.token()
        if not tok:
            break
        tokens_encontrados.append(tok)

    print(f"✓ Tokens reconocidos: {len(tokens_encontrados)}")

    # Si solo se pide léxico, se termina aquí
    if modo == "lexico":
        nombre_log = generar_log(
            codigo, integrante, tokens_encontrados, errores_lexicos, [], None, usuario_git, modo
        )
        print(f"\n✓ Log léxico generado: logs/{nombre_log}")
        return tokens_encontrados

    # ====== FASE SINTÁCTICA ======
    print("\nIniciando análisis sintáctico...\n")
    import  sintactico
    sintactico.errores_sintacticos.clear()

    resultado = sintactico.parser.parse(codigo, lexer=lexer_local)
    if sintactico.errores_sintacticos:
        print(f"✗ Errores sintácticos encontrados: {len(sintactico.errores_sintacticos)}")
    else:
        print("✓ Análisis sintáctico completado sin errores")

    # ====== LOG FINAL ======
    nombre_log = generar_log(
        codigo, integrante, tokens_encontrados, errores_lexicos,
        sintactico.errores_sintacticos, resultado, usuario_git, modo
    )
    print(f"\n✓ Log generado: logs/{nombre_log}")
    print("=" * 80 + "\n")

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == '__main__':
    usuarios_info = [
        ('tests/algoritmo_andres.php', 'Andrés Salazar', 'AndresSalazar19'),
        ('tests/algoritmo_yadira.php', 'Yadira Suárez', 'YadiSuarez'),
        ('tests/algoritmo_zahid.php', 'Zahid Díaz', 'LockHurb')
    ]

    if len(sys.argv) > 2:
        archivo = sys.argv[1]
        archivo = 'tests/' + archivo if not archivo.startswith('tests/') else archivo
        modo = sys.argv[2].lower()  # lexico o sintactico
    else:
        archivo, nombre, usuario = usuarios_info[1]
        modo = 'lexico'

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

    analizar_php(archivo, nombre, usuario, modo)
