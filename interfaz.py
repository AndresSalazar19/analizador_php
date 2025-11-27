import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
from datetime import datetime
import time

# Importar módulos
try:
    from lexico import tokens
    import ply.lex as lex
    import lexico
    from sintactico import parser, errores_sintacticos
    from semantico import analizar_programa, errores_semanticos, tabla_simbolos
except ImportError as e:
    print(f"Error al importar módulos: {e}")

class PHPAnalyzerIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico, Sintáctico y Semántico - PHP")
        self.root.geometry("1400x900")
        
        # Variables
        self.current_file = None
        self.codigo_actual = ""
        self.tokens_encontrados = []
        self.errores_lexicos = []
        self.resultado_sintactico = None
        self.dark_mode = True
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear la interfaz
        self.create_header()
        self.create_main_container()
        self.create_status_bar()
        
        # Aplicar tema oscuro por defecto
        self.apply_theme()
        
    def setup_styles(self):
        """Configura los estilos para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores tema oscuro
        self.colors_dark = {
            'bg': '#1e1e1e',
            'fg': '#d4d4d4',
            'editor_bg': '#1e1e1e',
            'editor_fg': '#d4d4d4',
            'sidebar_bg': '#252526',
            'header_bg': '#6366f1',
            'button_bg': '#4b5563',
            'button_hover': '#6b7280',
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6',
            'line_number_bg': '#252526',
            'line_number_fg': '#858585'
        }
        
        # Colores tema claro
        self.colors_light = {
            'bg': '#ffffff',
            'fg': '#1e1e1e',
            'editor_bg': '#ffffff',
            'editor_fg': '#1e1e1e',
            'sidebar_bg': '#f3f4f6',
            'header_bg': '#6366f1',
            'button_bg': '#e5e7eb',
            'button_hover': '#d1d5db',
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6',
            'line_number_bg': '#f3f4f6',
            'line_number_fg': '#6b7280'
        }
        
        self.colors = self.colors_dark
        
    def apply_theme(self):
        """Aplica el tema actual a toda la interfaz"""
        colors = self.colors
        
        # Aplicar al root
        self.root.configure(bg=colors['bg'])
        
        # Actualizar editor
        self.editor.configure(
            bg=colors['editor_bg'],
            fg=colors['editor_fg'],
            insertbackground=colors['fg']
        )
        
        # Actualizar números de línea
        self.line_numbers.configure(
            bg=colors['line_number_bg'],
            fg=colors['line_number_fg']
        )
        
        # Actualizar paneles de resultados
        for widget in [self.tokens_text, self.tree_text, self.errors_text]:
            widget.configure(
                bg=colors['editor_bg'],
                fg=colors['editor_fg']
            )
    
    def toggle_theme(self):
        """Alterna entre tema oscuro y claro"""
        self.dark_mode = not self.dark_mode
        self.colors = self.colors_dark if self.dark_mode else self.colors_light
        self.apply_theme()
        tema = "Oscuro" if self.dark_mode else "Claro"
        self.theme_button.configure(text=f"🌙 Tema {tema}")
        
    def create_header(self):
        """Crea la barra de herramientas superior"""
        header = tk.Frame(self.root, bg=self.colors['header_bg'], height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header, bg=self.colors['header_bg'])
        title_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            title_frame,
            text="PHP",
            font=('Consolas', 14, 'bold'),
            bg=self.colors['header_bg'],
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            title_frame,
            text="Analizador Léxico, Sintáctico y Semántico",
            font=('Segoe UI', 12),
            bg=self.colors['header_bg'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Botón de tema
        self.theme_button = tk.Button(
            header,
            text="🌙 Tema Oscuro",
            command=self.toggle_theme,
            bg='#4b5563',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.theme_button.pack(side=tk.RIGHT, padx=20)
        
    def create_main_container(self):
        """Crea el contenedor principal con el editor y los paneles"""
        # Toolbar
        self.create_toolbar()
        
        # Contenedor principal
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel izquierdo (Editor)
        left_panel = self.create_editor_panel()
        main_paned.add(left_panel, weight=1)
        
        # Panel derecho (Resultados)
        right_panel = self.create_results_panel()
        main_paned.add(right_panel, weight=1)
        
    def create_toolbar(self):
        """Crea la barra de herramientas con botones de acción"""
        toolbar = tk.Frame(self.root, bg=self.colors['bg'], pady=10)
        toolbar.pack(fill=tk.X, padx=10)
        
        # Botones de archivo
        file_frame = tk.Frame(toolbar, bg=self.colors['bg'])
        file_frame.pack(side=tk.LEFT)
        
        buttons_file = [
            ("📄 Nuevo", self.nuevo_archivo),
            ("📂 Abrir", self.abrir_archivo),
            ("💾 Guardar", self.guardar_archivo),
        ]
        
        for text, command in buttons_file:
            btn = tk.Button(
                file_frame,
                text=text,
                command=command,
                bg=self.colors['button_bg'],
                fg=self.colors['fg'],
                relief=tk.FLAT,
                padx=12,
                pady=6,
                cursor='hand2',
                font=('Segoe UI', 9)
            )
            btn.pack(side=tk.LEFT, padx=2)
            
        # Separador
        tk.Frame(toolbar, width=2, bg='#4b5563').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de análisis
        analysis_frame = tk.Frame(toolbar, bg=self.colors['bg'])
        analysis_frame.pack(side=tk.LEFT)
        
        self.btn_lexico = tk.Button(
            analysis_frame,
            text="🔍 Análisis Léxico",
            command=self.ejecutar_lexico,
            bg='#6366f1',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor='hand2',
            font=('Segoe UI', 9, 'bold')
        )
        self.btn_lexico.pack(side=tk.LEFT, padx=2)
        
        self.btn_sintactico = tk.Button(
            analysis_frame,
            text="📊 Análisis Sintáctico",
            command=self.ejecutar_sintactico,
            bg='#10b981',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor='hand2',
            font=('Segoe UI', 9, 'bold')
        )
        self.btn_sintactico.pack(side=tk.LEFT, padx=2)
        
        self.btn_semantico = tk.Button(
            analysis_frame,
            text="🎯 Análisis Semántico",
            command=self.ejecutar_semantico,
            bg='#ec4899',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor='hand2',
            font=('Segoe UI', 9, 'bold')
        )
        self.btn_semantico.pack(side=tk.LEFT, padx=2)
        
        self.btn_completo = tk.Button(
            analysis_frame,
            text="⚡ Análisis Completo",
            command=self.ejecutar_completo,
            bg='#f59e0b',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor='hand2',
            font=('Segoe UI', 9, 'bold')
        )
        self.btn_completo.pack(side=tk.LEFT, padx=2)
        
        # Botón de exportar
        self.btn_export = tk.Button(
            toolbar,
            text="📋 Exportar Reporte",
            command=self.exportar_reporte,
            bg=self.colors['button_bg'],
            fg=self.colors['fg'],
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor='hand2',
            font=('Segoe UI', 9)
        )
        self.btn_export.pack(side=tk.RIGHT, padx=2)
        
    def create_editor_panel(self):
        """Crea el panel del editor de código"""
        panel = tk.Frame(self.root, bg=self.colors['bg'])
        
        # Título del panel
        title_frame = tk.Frame(panel, bg=self.colors['sidebar_bg'], height=35)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📝 Editor de Código PHP",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Frame para editor con números de línea
        editor_frame = tk.Frame(panel, bg=self.colors['editor_bg'])
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Números de línea
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=5,
            takefocus=0,
            border=0,
            background=self.colors['line_number_bg'],
            foreground=self.colors['line_number_fg'],
            state='disabled',
            font=('Consolas', 10)
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor de código
        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg=self.colors['editor_bg'],
            fg=self.colors['editor_fg'],
            insertbackground=self.colors['fg'],
            selectbackground='#264f78',
            relief=tk.FLAT,
            undo=True
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Vincular eventos
        self.editor.bind('<KeyRelease>', self.update_line_numbers)
        self.editor.bind('<MouseWheel>', self.update_line_numbers)
        
        # Código inicial
        codigo_ejemplo = '''<?php
// Ejemplo de código PHP
$nombre = "Juan";
$edad = 25;

if ($edad >= 18) {
    echo "Hola " . $nombre;
    echo "Eres mayor de edad";
} else {
    echo "Eres menor de edad";
}

for ($i = 0; $i < 5; $i++) {
    echo $i;
}
?>'''
        self.editor.insert('1.0', codigo_ejemplo)
        self.update_line_numbers()
        
        return panel
    
    def update_line_numbers(self, event=None):
        """Actualiza los números de línea"""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        line_count = self.editor.get('1.0', tk.END).count('\n')
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')
        
    def create_results_panel(self):
        """Crea el panel de resultados con pestañas"""
        panel = tk.Frame(self.root, bg=self.colors['bg'])
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Tokens
        self.create_tokens_tab()
        
        # Pestaña de Árbol Sintáctico
        self.create_tree_tab()
        
        # Pestaña de Errores
        self.create_errors_tab()
        
        # Pestaña de Estadísticas
        self.create_stats_tab()
        
        return panel
    
    def create_tokens_tab(self):
        """Crea la pestaña de tokens"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="🔤 Tokens")
        
        # Título
        title_frame = tk.Frame(tab, bg=self.colors['sidebar_bg'], height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🎯 Tokens Identificados",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Área de tokens
        self.tokens_text = scrolledtext.ScrolledText(
            tab,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=self.colors['editor_bg'],
            fg=self.colors['editor_fg'],
            relief=tk.FLAT
        )
        self.tokens_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_tree_tab(self):
        """Crea la pestaña del árbol sintáctico"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="🌳 Árbol Sintáctico")
        
        # Título
        title_frame = tk.Frame(tab, bg=self.colors['sidebar_bg'], height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📊 Árbol Sintáctico Generado",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Área del árbol
        self.tree_text = scrolledtext.ScrolledText(
            tab,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=self.colors['editor_bg'],
            fg=self.colors['editor_fg'],
            relief=tk.FLAT
        )
        self.tree_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_errors_tab(self):
        """Crea la pestaña de errores"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="⚠️ Errores")
        
        # Título
        title_frame = tk.Frame(tab, bg=self.colors['sidebar_bg'], height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🚨 Errores Encontrados",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Área de errores
        self.errors_text = scrolledtext.ScrolledText(
            tab,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=self.colors['editor_bg'],
            fg=self.colors['editor_fg'],
            relief=tk.FLAT
        )
        self.errors_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_stats_tab(self):
        """Crea la pestaña de estadísticas"""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="📈 Estadísticas")
        
        # Título
        title_frame = tk.Frame(tab, bg=self.colors['sidebar_bg'], height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📊 Estadísticas del Análisis",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Frame de estadísticas
        stats_container = tk.Frame(tab, bg=self.colors['bg'])
        stats_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Estado del análisis
        status_frame = tk.Frame(stats_container, bg=self.colors['sidebar_bg'], relief=tk.FLAT, bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            status_frame,
            text="✅ Estado del Análisis",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        ).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        self.status_lexico_label = tk.Label(
            status_frame,
            text="○ Análisis léxico no ejecutado",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg'],
            anchor=tk.W
        )
        self.status_lexico_label.pack(fill=tk.X, padx=15, pady=2)
        
        self.status_sintactico_label = tk.Label(
            status_frame,
            text="○ Análisis sintáctico no ejecutado",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg'],
            anchor=tk.W
        )
        self.status_sintactico_label.pack(fill=tk.X, padx=15, pady=2)
        
        self.status_semantico_label = tk.Label(
            status_frame,
            text="○ Análisis semántico no ejecutado",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg'],
            anchor=tk.W
        )
        self.status_semantico_label.pack(fill=tk.X, padx=15, pady=(2, 15))
        
        # Grid de estadísticas
        grid_frame = tk.Frame(stats_container, bg=self.colors['bg'])
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid
        for i in range(2):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(3):
            grid_frame.rowconfigure(i, weight=1)
        
        # Crear tarjetas de estadísticas
        self.stat_cards = {}
        stats_config = [
            ('tokens', '0', 'TOKENS', '#6366f1'),
            ('lineas', '0', 'LÍNEAS', '#3b82f6'),
            ('errores', '0', 'ERRORES', '#ef4444'),
            ('variables', '0', 'VARIABLES', '#8b5cf6'),
            ('palabras_reservadas', '0', 'PALABRAS RESERV.', '#10b981'),
            ('tiempo', '0.000s', 'TIEMPO', '#f59e0b')
        ]
        
        for idx, (key, value, label, color) in enumerate(stats_config):
            row = idx // 2
            col = idx % 2
            
            card = tk.Frame(
                grid_frame,
                bg=self.colors['sidebar_bg'],
                relief=tk.FLAT,
                bd=1
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            value_label = tk.Label(
                card,
                text=value,
                font=('Segoe UI', 28, 'bold'),
                bg=self.colors['sidebar_bg'],
                fg=color
            )
            value_label.pack(pady=(20, 5))
            
            text_label = tk.Label(
                card,
                text=label,
                font=('Segoe UI', 9),
                bg=self.colors['sidebar_bg'],
                fg=self.colors['fg']
            )
            text_label.pack(pady=(0, 20))
            
            self.stat_cards[key] = value_label
        
    def create_status_bar(self):
        """Crea la barra de estado inferior"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['sidebar_bg'], height=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="● Listo",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['success'],
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.file_label = tk.Label(
            self.status_bar,
            text="Sin archivo",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        )
        self.file_label.pack(side=tk.LEFT, padx=20)
        
        self.version_label = tk.Label(
            self.status_bar,
            text="PHP 8.x",
            font=('Segoe UI', 9),
            bg=self.colors['sidebar_bg'],
            fg=self.colors['fg']
        )
        self.version_label.pack(side=tk.RIGHT, padx=10)
        
    # ==================== FUNCIONES DE ARCHIVO ====================
    
    def nuevo_archivo(self):
        """Crea un nuevo archivo"""
        if messagebox.askyesno("Nuevo archivo", "¿Desea crear un nuevo archivo? Se perderá el contenido actual."):
            self.editor.delete('1.0', tk.END)
            self.editor.insert('1.0', '<?php\n\n?>')
            self.current_file = None
            self.file_label.config(text="Sin archivo")
            self.update_status("Nuevo archivo creado", "success")
            
    def abrir_archivo(self):
        """Abre un archivo PHP"""
        file_path = filedialog.askopenfilename(
            title="Abrir archivo PHP",
            filetypes=[("PHP files", "*.php"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.delete('1.0', tk.END)
                    self.editor.insert('1.0', content)
                    self.current_file = file_path
                    self.file_label.config(text=os.path.basename(file_path))
                    self.update_status(f"Archivo abierto: {os.path.basename(file_path)}", "success")
                    self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
                
    def guardar_archivo(self):
        """Guarda el archivo actual"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    content = self.editor.get('1.0', tk.END)
                    file.write(content)
                self.update_status(f"Archivo guardado: {os.path.basename(self.current_file)}", "success")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
        else:
            self.guardar_como()
            
    def guardar_como(self):
        """Guarda el archivo con un nuevo nombre"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo PHP",
            defaultextension=".php",
            filetypes=[("PHP files", "*.php"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    content = self.editor.get('1.0', tk.END)
                    file.write(content)
                self.current_file = file_path
                self.file_label.config(text=os.path.basename(file_path))
                self.update_status(f"Archivo guardado: {os.path.basename(file_path)}", "success")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    # ==================== FUNCIONES DE ANÁLISIS ====================
    
    def ejecutar_lexico(self):
        """Ejecuta el análisis léxico"""
        self.update_status("Ejecutando análisis léxico...", "info")
        start_time = time.time()
        
        try:
            # Obtener código
            codigo = self.editor.get('1.0', tk.END)
            self.codigo_actual = codigo
            
            # Reiniciar errores
            if hasattr(lexico, 'errores'):
                lexico.errores.clear()
            
            # Crear lexer y tokenizar
            lexer_local = lex.lex(module=lexico)
            lexer_local.input(codigo)
            
            self.tokens_encontrados = []
            while True:
                tok = lexer_local.token()
                if not tok:
                    break
                self.tokens_encontrados.append(tok)
            
            # Obtener errores
            self.errores_lexicos = list(lexico.errores) if hasattr(lexico, 'errores') else []
            
            # Calcular tiempo
            elapsed = time.time() - start_time
            
            # Mostrar resultados
            self.mostrar_tokens()
            self.actualizar_estadisticas_lexico(elapsed)
            
            # Actualizar estado
            if self.errores_lexicos:
                self.status_lexico_label.config(
                    text=f"✗ Análisis léxico completado con {len(self.errores_lexicos)} errores",
                    fg=self.colors['error']
                )
                self.update_status(f"Análisis léxico completado con {len(self.errores_lexicos)} errores", "warning")
            else:
                self.status_lexico_label.config(
                    text="✓ Análisis léxico completado sin errores",
                    fg=self.colors['success']
                )
                self.update_status("Análisis léxico completado exitosamente", "success")
                
            self.notebook.select(0)  # Mostrar pestaña de tokens
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis léxico:\n{str(e)}")
            self.update_status("Error en análisis léxico", "error")
    
    def ejecutar_sintactico(self):
        """Ejecuta el análisis sintáctico"""
        self.update_status("Ejecutando análisis sintáctico...", "info")
        start_time = time.time()
        
        try:
            import sintactico
            
            codigo = self.editor.get('1.0', tk.END)
            self.codigo_actual = codigo
            
            # Limpiar errores previos
            sintactico.errores_sintacticos.clear()
            
            # Crear lexer y parser
            lexer_local = lex.lex(module=lexico)
            self.resultado_sintactico = sintactico.parser.parse(codigo, lexer=lexer_local)
            
            # Calcular tiempo
            elapsed = time.time() - start_time
            
            # Mostrar resultados
            self.mostrar_arbol_sintactico()
            self.mostrar_errores_sintacticos()
            self.actualizar_estadisticas_sintactico(elapsed)
            
            # Actualizar estado
            if sintactico.errores_sintacticos:
                self.status_sintactico_label.config(
                    text=f"✗ Análisis sintáctico completado con {len(sintactico.errores_sintacticos)} errores",
                    fg=self.colors['error']
                )
                self.update_status(f"Análisis sintáctico completado con {len(sintactico.errores_sintacticos)} errores", "warning")
            else:
                self.status_sintactico_label.config(
                    text="✓ Análisis sintáctico completado sin errores",
                    fg=self.colors['success']
                )
                self.update_status("Análisis sintáctico completado exitosamente", "success")
                
            self.notebook.select(1)  # Mostrar pestaña de árbol
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis sintáctico:\n{str(e)}")
            self.update_status("Error en análisis sintáctico", "error")
    
    def ejecutar_semantico(self):
        """Ejecuta el análisis semántico"""
        self.update_status("Ejecutando análisis semántico...", "info")
        start_time = time.time()
        
        try:
            import semantico
            
            # Primero ejecutar sintáctico si no se ha hecho
            if not self.resultado_sintactico:
                self.ejecutar_sintactico()
                if not self.resultado_sintactico:
                    messagebox.showwarning("Advertencia", "No se pudo generar el árbol sintáctico")
                    return
            
            # Limpiar errores previos
            semantico.errores_semanticos.clear()
            
            # Ejecutar análisis semántico
            analizar_programa(self.resultado_sintactico)
            
            # Calcular tiempo
            elapsed = time.time() - start_time
            
            # Mostrar resultados
            self.mostrar_errores_semanticos()
            self.actualizar_estadisticas_semantico(elapsed)
            
            # Actualizar estado
            if semantico.errores_semanticos:
                self.status_semantico_label.config(
                    text=f"✗ Análisis semántico completado con {len(semantico.errores_semanticos)} errores",
                    fg=self.colors['error']
                )
                self.update_status(f"Análisis semántico completado con {len(semantico.errores_semanticos)} errores", "warning")
            else:
                self.status_semantico_label.config(
                    text="✓ Análisis semántico completado sin errores",
                    fg=self.colors['success']
                )
                self.update_status("Análisis semántico completado exitosamente", "success")
                
            self.notebook.select(2)  # Mostrar pestaña de errores
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis semántico:\n{str(e)}")
            self.update_status("Error en análisis semántico", "error")
    
    def ejecutar_completo(self):
        """Ejecuta los tres análisis en secuencia"""
        self.update_status("Ejecutando análisis completo...", "info")
        
        try:
            # Ejecutar en orden
            self.ejecutar_lexico()
            self.ejecutar_sintactico()
            self.ejecutar_semantico()
            
            self.update_status("Análisis completo finalizado", "success")
            self.notebook.select(3)  # Mostrar pestaña de estadísticas
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis completo:\n{str(e)}")
            self.update_status("Error en análisis completo", "error")
    
    # ==================== FUNCIONES DE VISUALIZACIÓN ====================
    
    def mostrar_tokens(self):
            """Muestra los tokens encontrados y errores léxicos"""
            self.tokens_text.delete('1.0', tk.END)
            
            # Mostrar errores léxicos primero si existen
            if self.errores_lexicos:
                self.tokens_text.insert(tk.END, "═" * 90 + "\n")
                self.tokens_text.insert(tk.END, "ERRORES LÉXICOS ENCONTRADOS\n")
                self.tokens_text.insert(tk.END, "═" * 90 + "\n\n")
                
                for i, error in enumerate(self.errores_lexicos, 1):
                    if isinstance(error, dict):
                        self.tokens_text.insert(tk.END, f"{i}. ❌ Error LÉXICO en línea {error['linea']}, columna {error['columna']}:\n")
                        self.tokens_text.insert(tk.END, f"   → {error['mensaje']}\n")
                        self.tokens_text.insert(tk.END, f"   → Explicación: {error['explicacion']}\n\n")
                    else:
                        # Formato antiguo de errores
                        self.tokens_text.insert(tk.END, f"{i}. ❌ {error}\n\n")
                
                self.tokens_text.insert(tk.END, "\n" + "═" * 90 + "\n\n")
            
            if not self.tokens_encontrados:
                self.tokens_text.insert(tk.END, "No se encontraron tokens.\n")
                return
            
            # Encabezado
            header = f"{'#':<6} {'TIPO':<25} {'VALOR':<35} {'LÍNEA':<10}\n"
            header += "=" * 90 + "\n"
            self.tokens_text.insert(tk.END, header)
            
            # Tokens
            for i, tok in enumerate(self.tokens_encontrados, 1):
                valor_str = str(tok.value)
                if len(valor_str) > 32:
                    valor_str = valor_str[:32] + "..."
                
                linea = f"{i:<6} {tok.type:<25} {valor_str:<35} {tok.lineno:<10}\n"
                self.tokens_text.insert(tk.END, linea)
            
            # Resumen
            self.tokens_text.insert(tk.END, "\n" + "=" * 90 + "\n")
            self.tokens_text.insert(tk.END, f"Total de tokens: {len(self.tokens_encontrados)}\n")
            self.tokens_text.insert(tk.END, f"Total de errores léxicos: {len(self.errores_lexicos)}\n")

    
    def mostrar_arbol_sintactico(self):
        """Muestra el árbol sintáctico"""
        self.tree_text.delete('1.0', tk.END)
        
        if not self.resultado_sintactico:
            self.tree_text.insert(tk.END, "No se generó árbol sintáctico.\n")
            return
        
        # Mostrar árbol formateado
        arbol = self.formatear_arbol(self.resultado_sintactico)
        self.tree_text.insert(tk.END, arbol)
    
    def formatear_arbol(self, nodo, nivel=0, prefijo=""):
        """Formatea el árbol sintáctico de forma legible"""
        if nodo is None:
            return ""
        
        indent = "  " * nivel
        resultado = ""
        
        if isinstance(nodo, tuple):
            if len(nodo) > 0:
                resultado += f"{indent}{prefijo}({nodo[0]}\n"
                for i, hijo in enumerate(nodo[1:], 1):
                    es_ultimo = (i == len(nodo) - 1)
                    nuevo_prefijo = "└─ " if es_ultimo else "├─ "
                    resultado += self.formatear_arbol(hijo, nivel + 1, nuevo_prefijo)
                resultado += f"{indent})\n"
        elif isinstance(nodo, list):
            resultado += f"{indent}{prefijo}[\n"
            for i, hijo in enumerate(nodo):
                es_ultimo = (i == len(nodo) - 1)
                nuevo_prefijo = "└─ " if es_ultimo else "├─ "
                resultado += self.formatear_arbol(hijo, nivel + 1, nuevo_prefijo)
            resultado += f"{indent}]\n"
        elif isinstance(nodo, dict):
            resultado += f"{indent}{prefijo}{{\n"
            items = list(nodo.items())
            for i, (clave, valor) in enumerate(items):
                es_ultimo = (i == len(items) - 1)
                nuevo_prefijo = "└─ " if es_ultimo else "├─ "
                resultado += f"{indent}  {nuevo_prefijo}{clave} => "
                if isinstance(valor, (dict, list, tuple)):
                    resultado += "\n" + self.formatear_arbol(valor, nivel + 2, "")
                else:
                    resultado += f"{valor}\n"
            resultado += f"{indent}}}\n"
        else:
            resultado += f"{indent}{prefijo}{repr(nodo)}\n"
        
        return resultado
    
    def mostrar_errores_sintacticos(self):
        """Muestra los errores sintácticos con formato mejorado"""
        import sintactico
        
        self.errors_text.delete('1.0', tk.END)
        
        # Título
        self.errors_text.insert(tk.END, "═" * 90 + "\n")
        self.errors_text.insert(tk.END, "ERRORES SINTÁCTICOS\n")
        self.errors_text.insert(tk.END, "═" * 90 + "\n\n")
        
        if sintactico.errores_sintacticos:
            for i, error in enumerate(sintactico.errores_sintacticos, 1):
                self.errors_text.insert(tk.END, f"{i}. ❌ Error SINTÁCTICO en línea {error['linea']}:\n")
                self.errors_text.insert(tk.END, f"   → {error['mensaje']}\n")
                self.errors_text.insert(tk.END, f"   → Explicación: {error['explicacion']}\n\n")
        else:
            self.errors_text.insert(tk.END, "✓ No se encontraron errores sintácticos.\n")

    
    def mostrar_errores_semanticos(self):
            """Muestra los errores semánticos con formato mejorado"""
            import semantico
            from semantico import tabla_simbolos
            
            self.errors_text.delete('1.0', tk.END)
            
            # Título
            self.errors_text.insert(tk.END, "═" * 90 + "\n")
            self.errors_text.insert(tk.END, "ERRORES SEMÁNTICOS\n")
            self.errors_text.insert(tk.END, "═" * 90 + "\n\n")
            
            if semantico.errores_semanticos:
                for i, error in enumerate(semantico.errores_semanticos, 1):
                    if isinstance(error, dict):
                        self.errors_text.insert(tk.END, f"{i}. ⚠️ Error SEMÁNTICO en línea {error['linea']}:\n")
                        self.errors_text.insert(tk.END, f"   → {error['mensaje']}\n")
                        if error.get('contexto'):
                            self.errors_text.insert(tk.END, f"   → Contexto: {error['contexto']}\n")
                        self.errors_text.insert(tk.END, "\n")
                    else:
                        # Formato antiguo de errores
                        self.errors_text.insert(tk.END, f"{i}. ⚠️ {error}\n\n")
            else:
                self.errors_text.insert(tk.END, "✓ No se encontraron errores semánticos.\n")
            
            # Mostrar tabla de símbolos
            self.errors_text.insert(tk.END, "\n" + "═" * 90 + "\n")
            self.errors_text.insert(tk.END, "TABLA DE SÍMBOLOS\n")
            self.errors_text.insert(tk.END, "═" * 90 + "\n\n")
            
            self.errors_text.insert(tk.END, f"Variables globales: {len(tabla_simbolos['globales'])}\n")
            self.errors_text.insert(tk.END, f"Funciones: {len(tabla_simbolos['funciones'])}\n")
            self.errors_text.insert(tk.END, f"Clases: {len(tabla_simbolos['clases'])}\n")
            self.errors_text.insert(tk.END, f"Constantes: {len(tabla_simbolos['constantes'])}\n")

    def actualizar_estadisticas_lexico(self, tiempo):
        """Actualiza las estadísticas después del análisis léxico"""
        lineas = self.editor.get('1.0', tk.END).count('\n')
        palabras_reserv = sum(1 for tok in self.tokens_encontrados if tok.type in ['IF', 'ELSE', 'WHILE', 'FOR', 'FUNCTION', 'CLASS'])
        
        self.stat_cards['tokens'].config(text=str(len(self.tokens_encontrados)))
        self.stat_cards['lineas'].config(text=str(lineas))
        self.stat_cards['errores'].config(text=str(len(self.errores_lexicos)))
        self.stat_cards['palabras_reservadas'].config(text=str(palabras_reserv))
        self.stat_cards['tiempo'].config(text=f"{tiempo:.3f}s")
    
    def actualizar_estadisticas_sintactico(self, tiempo):
        """Actualiza las estadísticas después del análisis sintáctico"""
        import sintactico
        errores_totales = len(self.errores_lexicos) + len(sintactico.errores_sintacticos)
        self.stat_cards['errores'].config(text=str(errores_totales))
        self.stat_cards['tiempo'].config(text=f"{tiempo:.3f}s")
    
    def actualizar_estadisticas_semantico(self, tiempo):
        """Actualiza las estadísticas después del análisis semántico"""
        import sintactico
        import semantico
        
        errores_totales = (len(self.errores_lexicos) + 
                          len(sintactico.errores_sintacticos) + 
                          len(semantico.errores_semanticos))
        
        self.stat_cards['errores'].config(text=str(errores_totales))
        self.stat_cards['variables'].config(text=str(len(tabla_simbolos['globales'])))
        self.stat_cards['tiempo'].config(text=f"{tiempo:.3f}s")
    
    # ==================== EXPORTAR REPORTE ====================
    
    def exportar_reporte(self):
        """Exporta un reporte completo del análisis con errores mejorados"""
        if not self.tokens_encontrados:
            messagebox.showwarning("Advertencia", "No hay análisis para exportar")
            return
        
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
            usuario = "usuario"
            nombre_log = f"analisis-completo-{usuario}-{fecha_hora}.txt"
            ruta_log = os.path.join('logs', nombre_log)
            
            with open(ruta_log, 'w', encoding='utf-8') as f:
                f.write("=" * 90 + "\n")
                f.write("ANÁLISIS COMPLETO - PHP\n")
                f.write(f"Fecha y Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 90 + "\n\n")
                
                # Resumen de errores
                import sintactico
                import semantico
                
                total_errores = (len(self.errores_lexicos) + 
                               len(sintactico.errores_sintacticos) + 
                               len(semantico.errores_semanticos))
                
                f.write("RESUMEN DE ERRORES:\n")
                f.write(f"  • Errores léxicos: {len(self.errores_lexicos)}\n")
                f.write(f"  • Errores sintácticos: {len(sintactico.errores_sintacticos)}\n")
                f.write(f"  • Errores semánticos: {len(semantico.errores_semanticos)}\n")
                f.write(f"  • TOTAL: {total_errores}\n\n")
                
                # Código analizado
                f.write("CÓDIGO ANALIZADO:\n")
                f.write("-" * 90 + "\n")
                f.write(self.codigo_actual)
                f.write("\n" + "-" * 90 + "\n\n")
                
                # Errores léxicos
                if self.errores_lexicos:
                    f.write("═" * 90 + "\n")
                    f.write("ERRORES LÉXICOS\n")
                    f.write("═" * 90 + "\n")
                    for i, error in enumerate(self.errores_lexicos, 1):
                        if isinstance(error, dict):
                            f.write(f"\n{i}. Error LÉXICO en línea {error['linea']}, columna {error['columna']}:\n")
                            f.write(f"   → {error['mensaje']}\n")
                            f.write(f"   → Explicación: {error['explicacion']}\n")
                        else:
                            f.write(f"\n{i}. {error}\n")
                
                # Tokens
                f.write("\n" + "═" * 90 + "\n")
                f.write("ANÁLISIS LÉXICO - TOKENS\n")
                f.write("═" * 90 + "\n")
                f.write(f"Tokens encontrados: {len(self.tokens_encontrados)}\n")
                f.write("-" * 90 + "\n")
                
                for i, tok in enumerate(self.tokens_encontrados, 1):
                    f.write(f"{i:<6} {tok.type:<25} {str(tok.value):<35} {tok.lineno:<10}\n")
                
                # Errores sintácticos
                if sintactico.errores_sintacticos:
                    f.write("\n" + "═" * 90 + "\n")
                    f.write("ERRORES SINTÁCTICOS\n")
                    f.write("═" * 90 + "\n")
                    for i, error in enumerate(sintactico.errores_sintacticos, 1):
                        if isinstance(error, dict):
                            f.write(f"\n{i}. Error SINTÁCTICO en línea {error['linea']}:\n")
                            f.write(f"   → {error['mensaje']}\n")
                            f.write(f"   → Explicación: {error['explicacion']}\n")
                        else:
                            f.write(f"\n{i}. {error}\n")
                
                # Árbol sintáctico
                f.write("\n" + "═" * 90 + "\n")
                f.write("ANÁLISIS SINTÁCTICO\n")
                f.write("═" * 90 + "\n")
                if self.resultado_sintactico:
                    f.write("\nÁRBOL SINTÁCTICO:\n")
                    f.write(self.formatear_arbol(self.resultado_sintactico))
                else:
                    f.write("\nNo se generó árbol sintáctico debido a errores.\n")
                
                # Errores semánticos
                if semantico.errores_semanticos:
                    f.write("\n" + "═" * 90 + "\n")
                    f.write("ERRORES SEMÁNTICOS\n")
                    f.write("═" * 90 + "\n")
                    for i, error in enumerate(semantico.errores_semanticos, 1):
                        if isinstance(error, dict):
                            f.write(f"\n{i}. Error SEMÁNTICO en línea {error['linea']}:\n")
                            f.write(f"   → {error['mensaje']}\n")
                            if error.get('contexto'):
                                f.write(f"   → Contexto: {error['contexto']}\n")
                        else:
                            f.write(f"\n{i}. {error}\n")
                
                # Tabla de símbolos
                f.write("\n" + "═" * 90 + "\n")
                f.write("TABLA DE SÍMBOLOS\n")
                f.write("═" * 90 + "\n")
                from semantico import tabla_simbolos
                f.write(f"Variables globales: {len(tabla_simbolos['globales'])}\n")
                f.write(f"Funciones: {len(tabla_simbolos['funciones'])}\n")
                f.write(f"Clases: {len(tabla_simbolos['clases'])}\n")
                f.write(f"Constantes: {len(tabla_simbolos['constantes'])}\n")
                
                f.write("\n" + "=" * 90 + "\n")
                f.write("FIN DEL ANÁLISIS\n")
                f.write("=" * 90 + "\n")
            
            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente:\n{ruta_log}")
            self.update_status(f"Reporte exportado: {nombre_log}", "success")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el reporte:\n{str(e)}")


    # ==================== UTILIDADES ====================
    
    def update_status(self, message, status_type="info"):
        """Actualiza la barra de estado"""
        colors = {
            'success': self.colors['success'],
            'error': self.colors['error'],
            'warning': self.colors['warning'],
            'info': self.colors['info']
        }
        
        self.status_label.config(
            text=f"● {message}",
            fg=colors.get(status_type, self.colors['fg'])
        )
        self.root.update_idletasks()


# ==================== INICIALIZACIÓN ====================

def main():
    root = tk.Tk()
    app = PHPAnalyzerIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()