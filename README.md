# Analizador Léxico, Sintáctico y Semántico para PHP

## 📋 Descripción del Proyecto

Este proyecto implementa un analizador completo para el lenguaje PHP que incluye análisis léxico, sintáctico y semántico. Cuenta con una interfaz gráfica moderna desarrollada con Tkinter que permite escribir, analizar y exportar código PHP con detección de errores en tiempo real.

## 👥 Integrantes del Equipo

- **Andrés Salazar** (@AndresSalazar19)
- **Yadira Suarez** (@YadiSuarez)
- **Zahid Díaz** (@LockHurb)

## 🚀 Características Principales

### Análisis Léxico
- Reconocimiento de tokens PHP (variables, operadores, palabras reservadas, literales)
- Detección de errores léxicos con reporte detallado
- Soporte para:
  - Variables estándar (`$variable`)
  - Variables de instancia (`$this->propiedad`)
  - Superglobales (`$_GET`, `$_POST`, `$GLOBALS`, etc.)
  - Operadores aritméticos, lógicos y de comparación
  - Cadenas de texto, números enteros y flotantes
  - Comentarios de línea y multilínea

### Análisis Sintáctico
- Parser completo basado en PLY (Python Lex-Yacc)
- Estructuras soportadas:
  - Condicionales (`if`, `else`, `elseif`, `switch`)
  - Bucles (`for`, `while`, `foreach`)
  - Funciones con parámetros opcionales y obligatorios
  - Funciones lambda (anónimas)
  - Clases con herencia, propiedades y métodos
  - Arrays asociativos y multidimensionales
- Detección de errores sintácticos con mensaje explicativo

### Análisis Semántico
- Tabla de símbolos con ámbitos global y local
- Reglas semánticas implementadas:
  1. Verificación de declaración de variables antes de uso
  2. Detección de redeclaración de variables, funciones y clases
  3. Verificación de tipos en operaciones aritméticas
  4. Control de acceso a variables globales desde ámbito local
  5. Validación de parámetros en llamadas a funciones
  6. Detección de `break`/`continue` fuera de contexto
  7. Validación de `return` dentro de funciones
  8. Verificación de existencia de clases en instanciación
  9. Control de modificación de constantes
  10. Validación de herencia de clases

### Interfaz Gráfica
- Editor de código con numeración de líneas sincronizada
- Resaltado de sintaxis
- Tema claro/oscuro
- Pestañas para visualizar:
  - Tokens identificados
  - Árbol sintáctico
  - Errores (léxicos, sintácticos y semánticos)
  - Estadísticas del análisis
- Exportación de reportes completos a archivos `.txt`
- Gestión de archivos (nuevo, abrir, guardar)

## 📦 Requisitos e Instalación

### Requisitos del Sistema
- Python 3.7 o superior
- Sistema operativo: Windows, Linux o macOS

### Instalación de Dependencias

1. **Instalar PLY (Python Lex-Yacc)**
```bash
   pip install ply
```

2. **Verificar Tkinter** (incluido con Python en la mayoría de instalaciones)
```bash
   python -m tkinter
```
   Si no está instalado:
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **Fedora**: `sudo dnf install python3-tkinter`
   - **macOS**: Incluido con Python desde python.org
   - **Windows**: Incluido con Python

### Librerías Utilizadas
```
ply==3.11           # Parser generator (lex y yacc)
tkinter             # Interfaz gráfica (incluida en Python estándar)
datetime            # Manejo de fechas (incluida en Python estándar)
os                  # Operaciones del sistema (incluida en Python estándar)
sys                 # Sistema (incluida en Python estándar)
```

### Método 1: Desde un IDE
1. Abrir `interfaz.py` en tu IDE favorito (PyCharm, VS Code, etc.)
2. Ejecutar el archivo directamente

### Uso de la Interfaz

1. **Escribir Código**:
   - Escribir o pegar código PHP en el editor
   - O usar "📂 Abrir" para cargar un archivo `.php`

2. **Ejecutar Análisis**:
   - **🔍 Análisis Léxico**: Identifica tokens y errores léxicos
   - **📊 Análisis Sintáctico**: Genera árbol sintáctico y detecta errores
   - **🎯 Análisis Semántico**: Valida reglas semánticas
   - **⚡ Análisis Completo**: Ejecuta los tres análisis en secuencia

3. **Ver Resultados**:
   - Pestaña **Tokens**: Lista de tokens identificados
   - Pestaña **Árbol Sintáctico**: Estructura del programa
   - Pestaña **Errores**: Errores detectados con línea y explicación
   - Pestaña **Estadísticas**: Resumen del análisis

4. **Exportar Reporte**:
   - Clic en "📋 Exportar Reporte"
   - El archivo se guarda en `logs/` con timestamp

## 🧪 Algoritmos de Prueba

Cada integrante ha desarrollado algoritmos de prueba específicos ubicados en `algoritmos_prueba/`:

### Andrés Salazar (`prueba_andres.php`)
- Declaración de variables múltiples
- Estructuras condicionales (`if`, `elseif`, `else`)
- Bucles `for` con diferentes inicializaciones
- Funciones con retorno y parámetros
- Operaciones aritméticas complejas

### Yadira Suarez (`prueba_yadira.php`)
- Variables booleanas y expresiones lógicas
- Bucles `while` y `foreach`
- Arrays asociativos
- Superglobales (`$_GET`, `$_POST`, `$GLOBALS`)
- Asignaciones por referencia

### Zahid Díaz (`prueba_zahid.php`)
- Estructura `switch-case`
- Asignaciones compuestas (`+=`, `-=`, etc.)
- Funciones lambda con clausuras
- Clases con herencia
- Arrays multidimensionales

## 📊 Reglas Semánticas Implementadas

### Por Andrés Salazar
1. **Declaración antes de uso**: Variables deben ser declaradas antes de usarse
2. **Tipos compatibles en aritmética**: Operaciones aritméticas solo entre `int` y `float`
3. **Validación de parámetros de funciones**: Número correcto de argumentos en llamadas
4. **Return en funciones con retorno**: Funciones declaradas con retorno deben tener `return`

### Por Yadira Suarez
1. **Variables superglobales**: Validación de acceso a `$GLOBALS` y otras superglobales
2. **Scope de variables**: Variables globales no accesibles directamente desde ámbito local
3. **Expresiones booleanas**: Validación de operadores lógicos y comparaciones
4. **Bucle foreach**: Validación de estructura y variables en `foreach`

### Por Zahid Díaz
1. **Break/Continue en contexto**: Solo dentro de bucles o switch
2. **Clases y herencia**: Validación de clases padre antes de heredar
3. **Constantes inmutables**: Detección de modificación de constantes
4. **Métodos y propiedades de clase**: Validación de redeclaración en clases

## 📝 Logs Generados

Los logs se generan automáticamente en la carpeta `logs/` con el formato:
```
analisis-completo-usuario-DD-MM-YYYY-HHhMM.txt
```

### Contenido de los Logs
- Código analizado
- Resumen de errores (léxicos, sintácticos, semánticos)
- Lista completa de tokens
- Árbol sintáctico formateado
- Errores detallados con línea y explicación
- Tabla de símbolos

## 🎨 Características de la Interfaz

### Temas
- **Tema Oscuro** (predeterminado): Ideal para trabajo prolongado
- **Tema Claro**: Mayor contraste para presentaciones

### Editor
- Numeración de líneas sincronizada con scroll
- Fuente monoespaciada (Consolas)
- Deshacer/Rehacer (`Ctrl+Z`, `Ctrl+Y`)
- Código de ejemplo al iniciar


## 📞 Contacto y Soporte

Para consultas o problemas con el proyecto, contactar a cualquiera de los integrantes:
- Andrés Salazar: @AndresSalazar19
- Yadira Suarez: @YadiSuarez
- Zahid Díaz: @LockHurb

## 📄 Licencia

Este proyecto es de uso académico para el curso de Lenguajes de Programación.

---

**Desarrollado con ❤️ por el Equipo de Análisis PHP**