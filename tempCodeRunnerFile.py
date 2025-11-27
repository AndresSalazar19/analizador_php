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
