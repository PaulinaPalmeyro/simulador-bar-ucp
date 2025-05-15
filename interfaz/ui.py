import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sys
import io
import re
from generadores.cuadrados_medios import run_cuadrados_medios
from generadores.fibonacci import run_fibonacci
from generadores.congruencial_aditivo import run_congruencial_aditivo
from generadores.congruencial_mixto import run_congruencial_mixto
from generadores.congruencial_multiplicativo import run_congruencial_multiplicativo
from validacion.chi_cuadrado import chi_cuadrado, mostrar_resultado
from simulacion.bar_ucp import simular_bar_ucp

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, minvalue=None, maxvalue=None, initialvalue=None):
        self.prompt = prompt
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.initialvalue = initialvalue
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        # Configurar el tamaño mínimo de la ventana
        self.minsize(400, 150)
        
        # Crear y configurar el frame principal
        frame = ttk.Frame(master, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Agregar el texto de la promesa
        label = ttk.Label(frame, text=self.prompt, wraplength=350, justify=tk.LEFT)
        label.pack(pady=(0, 10))
        
        # Crear y configurar el campo de entrada
        self.entry = ttk.Entry(frame, width=30)
        self.entry.pack(pady=10)
        if self.initialvalue is not None:
            self.entry.insert(0, str(self.initialvalue))
        
        # Hacer que la ventana siempre esté por encima
        self.transient(self.master)
        self.grab_set()
        
        return self.entry

    def validate(self):
        try:
            value = int(self.entry.get())
            if self.minvalue is not None and value < self.minvalue:
                messagebox.showerror("Error", f"El valor debe ser mayor o igual a {self.minvalue}")
                return False
            if self.maxvalue is not None and value > self.maxvalue:
                messagebox.showerror("Error", f"El valor debe ser menor o igual a {self.maxvalue}")
                return False
            self.result = value
            return True
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número entero válido")
            return False

    def apply(self):
        self.result = int(self.entry.get())

class CustomFloatDialog(CustomDialog):
    def validate(self):
        try:
            value = float(self.entry.get())
            if self.minvalue is not None and value < self.minvalue:
                messagebox.showerror("Error", f"El valor debe ser mayor o igual a {self.minvalue}")
                return False
            if self.maxvalue is not None and value > self.maxvalue:
                messagebox.showerror("Error", f"El valor debe ser menor o igual a {self.maxvalue}")
                return False
            self.result = value
            return True
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")
            return False

    def apply(self):
        self.result = float(self.entry.get())

class StdoutRedirector(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.setup_tags()
        self.is_first_write = True
        
    def setup_tags(self):
        # Configurar tags para títulos
        self.text_widget.tag_configure('title', foreground='#2E86C1', font=('Consolas', 12, 'bold'))
        self.text_widget.tag_configure('subtitle', foreground='#2874A6', font=('Consolas', 11, 'bold'))
        self.text_widget.tag_configure('bar_title', foreground='#2E86C1', font=('Consolas', 12, 'bold'))
        
    def write(self, s):
        # Si es el primer write después de limpiar, asegurar que el scroll esté arriba
        if self.is_first_write:
            self.text_widget.yview_moveto(0)
            self.is_first_write = False
            
        # Procesar el texto para aplicar estilos
        lines = s.split('\n')
        for line in lines:
            if line.strip():
                # Detectar títulos específicos de la simulación del bar
                if any(title in line for title in [
                    "===== PARÁMETROS BASE GENERADOS =====",
                    "===== RESULTADOS DE ATENCIÓN EN LA SIMULACIÓN =====",
                    "===== MÉTRICAS ESTADÍSTICAS =====",
                    "===== USO DE NÚMEROS PSEUDOALEATORIOS ====="
                ]):
                    self.text_widget.insert(tk.END, line + '\n', 'bar_title')
                # Detectar otros títulos y subtítulos
                elif line.startswith('====='):
                    self.text_widget.insert(tk.END, line + '\n', 'title')
                elif line.startswith('---'):
                    self.text_widget.insert(tk.END, line + '\n', 'subtitle')
                else:
                    self.text_widget.insert(tk.END, line + '\n')
            else:
                self.text_widget.insert(tk.END, '\n')
        self.text_widget.see(tk.END)
        
    def flush(self):
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador TP2 - Modelos y Simulación (UI)")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.resizable(True, True)
        self.ultima_secuencia_ui = []
        self.ultima_secuencia_valida = False
        
        # Configurar el tema
        self.configure_theme()
        self.create_widgets()

    def configure_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores y estilos
        style.configure('TFrame', background='#F8F9F9')
        style.configure('TButton', 
                       background='#3498DB',
                       foreground='white',
                       padding=5,
                       font=('Segoe UI', 9))
        style.configure('Menu.TButton',
                       background='#2980B9',
                       foreground='white',
                       padding=8,
                       font=('Segoe UI', 9, 'bold'))
        style.map('TButton',
                 background=[('active', '#2980B9')],
                 foreground=[('active', 'white')])
        
        # Configurar el área de texto
        self.configure(bg='#F8F9F9')

    def create_widgets(self):
        # Frame principal con padding y estilo
        main_frame = ttk.Frame(self, padding="10", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame del menú con estilo
        frame_menu = ttk.Frame(main_frame, style='TFrame')
        frame_menu.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Frame de resultados con estilo
        frame_result = ttk.Frame(main_frame, style='TFrame')
        frame_result.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones del menú con estilo mejorado
        ttk.Button(frame_menu, text="Cuadrados Medios", width=25, command=self.cuadrados_medios_ui, style='Menu.TButton').pack(pady=5)
        ttk.Button(frame_menu, text="Fibonacci", width=25, command=self.fibonacci_ui, style='Menu.TButton').pack(pady=5)
        ttk.Button(frame_menu, text="Congruencial Aditivo", width=25, command=self.congruencial_aditivo_ui, style='Menu.TButton').pack(pady=5)
        ttk.Button(frame_menu, text="Congruencial Mixto", width=25, command=self.congruencial_mixto_ui, style='Menu.TButton').pack(pady=5)
        ttk.Button(frame_menu, text="Congruencial Multiplicativo", width=25, command=self.congruencial_multiplicativo_ui, style='Menu.TButton').pack(pady=5)
        ttk.Button(frame_menu, text="Simular Bar UCP", width=25, command=self.simular_bar_ui, style='Menu.TButton').pack(pady=5)
        ttk.Button(frame_menu, text="Salir", width=25, command=self.quit, style='Menu.TButton').pack(pady=20)

        # Área de resultados con scrollbar y estilo mejorado
        result_frame = ttk.Frame(frame_result, style='TFrame')
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_result = tk.Text(result_frame, 
                                 wrap=tk.WORD, 
                                 font=("Consolas", 11),
                                 bg='#FFFFFF',
                                 fg='#2C3E50',
                                 yscrollcommand=scrollbar.set,
                                 padx=10,
                                 pady=10)
        self.text_result.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_result.yview)

        # Redirigir print a la interfaz
        self.stdout_redirector = StdoutRedirector(self.text_result)

    def limpiar_resultado(self):
        self.text_result.delete(1.0, tk.END)
        # Resetear el flag de primer write
        self.stdout_redirector.is_first_write = True
        # Asegurar que el scroll esté en la parte superior
        self.text_result.yview_moveto(0)

    def cuadrados_medios_ui(self):
        self.limpiar_resultado()
        semilla = CustomDialog(self, "Cuadrados Medios", "🔸 Semilla inicial (entero ≥ 100)", minvalue=100).result
        if semilla is None:
            return
        digitos = CustomDialog(self, "Cuadrados Medios", "🔸 Cantidad de dígitos significativos a extraer (ej: 4)", minvalue=1).result
        if digitos is None:
            return
        cantidad = CustomDialog(self, "Cuadrados Medios", "🔸 Cantidad total de números a generar (mínimo 1)", minvalue=1).result
        if cantidad is None:
            return
        old_stdout = sys.stdout
        sys.stdout = self.stdout_redirector
        try:
            resultados, ui = run_cuadrados_medios_custom(semilla, digitos, cantidad)
            self.ultima_secuencia_ui = ui
            self.validar_secuencia(ui)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def fibonacci_ui(self):
        self.limpiar_resultado()
        x0 = CustomDialog(self, "Fibonacci", "🔸 x₀: Primera semilla (entero positivo)", minvalue=0).result
        if x0 is None:
            return
        x1 = CustomDialog(self, "Fibonacci", "🔸 x₁: Segunda semilla (entero positivo)", minvalue=0).result
        if x1 is None:
            return
        m = CustomDialog(self, "Fibonacci", "🔸 m: Módulo (entero positivo)", minvalue=1).result
        if m is None:
            return
        cantidad = CustomDialog(self, "Fibonacci", "🔸 cantidad: Total de números a generar (mínimo 1)", minvalue=1).result
        if cantidad is None:
            return
        old_stdout = sys.stdout
        sys.stdout = self.stdout_redirector
        try:
            resultados, ui = run_fibonacci_custom(x0, x1, m, cantidad)
            self.ultima_secuencia_ui = ui
            self.validar_secuencia(ui)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def congruencial_aditivo_ui(self):
        self.limpiar_resultado()
        semillas = []
        while True:
            valor = CustomDialog(self, "Congruencial Aditivo", 
                               f"Ingrese semilla #{len(semillas) + 1} (entero positivo):", 
                               minvalue=0).result
            if valor is None:
                break
            semillas.append(valor)
            if len(semillas) >= 2:
                continuar = messagebox.askyesno("Congruencial Aditivo", "¿Desea ingresar otra semilla?")
                if not continuar:
                    break
        if len(semillas) < 2:
            messagebox.showwarning("Congruencial Aditivo", "Se requieren al menos 2 semillas.")
            return
        m = CustomDialog(self, "Congruencial Aditivo", "🔸 Ingrese el módulo (m):", minvalue=1).result
        if m is None:
            return
        cantidad = CustomDialog(self, "Congruencial Aditivo", 
                              "🔸 Ingrese la cantidad total de números a generar:", 
                              minvalue=len(semillas) + 1).result
        if cantidad is None:
            return
        old_stdout = sys.stdout
        sys.stdout = self.stdout_redirector
        try:
            resultados, ui = run_congruencial_aditivo_custom(semillas, m, cantidad)
            self.ultima_secuencia_ui = ui
            self.validar_secuencia(ui)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def congruencial_mixto_ui(self):
        self.limpiar_resultado()
        x0 = CustomDialog(self, "Congruencial Mixto", "🔸 x₀: Semilla inicial (entero positivo)", minvalue=0).result
        if x0 is None:
            return
        a = CustomDialog(self, "Congruencial Mixto", "🔸 a: Multiplicador (entero positivo)", minvalue=1).result
        if a is None:
            return
        b = CustomDialog(self, "Congruencial Mixto", "🔸 b: Constante aditiva (entero positivo)", minvalue=0).result
        if b is None:
            return
        m = CustomDialog(self, "Congruencial Mixto", "🔸 m: Módulo (entero positivo)", minvalue=1).result
        if m is None:
            return
        cantidad = CustomDialog(self, "Congruencial Mixto", "🔸 cantidad: Total de números a generar (mínimo 1)", minvalue=1).result
        if cantidad is None:
            return
        old_stdout = sys.stdout
        sys.stdout = self.stdout_redirector
        try:
            resultados, ui = run_congruencial_mixto_custom(x0, a, b, m, cantidad)
            self.ultima_secuencia_ui = ui
            self.validar_secuencia(ui)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def congruencial_multiplicativo_ui(self):
        self.limpiar_resultado()
        x0 = CustomDialog(self, "Congruencial Multiplicativo", "🔸 x₀: Semilla inicial (entero positivo)", minvalue=0).result
        if x0 is None:
            return
        a = CustomDialog(self, "Congruencial Multiplicativo", "🔸 a: Multiplicador (entero positivo)", minvalue=1).result
        if a is None:
            return
        m = CustomDialog(self, "Congruencial Multiplicativo", "🔸 m: Módulo (entero positivo)", minvalue=2).result
        if m is None:
            return
        cantidad = CustomDialog(self, "Congruencial Multiplicativo", "🔸 cantidad: Total de números a generar (mínimo 1)", minvalue=1).result
        if cantidad is None:
            return
        old_stdout = sys.stdout
        sys.stdout = self.stdout_redirector
        try:
            resultados, ui = run_congruencial_multiplicativo_custom(x0, a, m, cantidad)
            self.ultima_secuencia_ui = ui
            self.validar_secuencia(ui)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def simular_bar_ui(self):
        self.limpiar_resultado()
        if not self.ultima_secuencia_ui:
            messagebox.showwarning("Simulación Bar UCP", "⚠️ No hay ninguna secuencia generada. Genere una primero con opciones 1–5.")
            return
        if not self.ultima_secuencia_valida:
            messagebox.showwarning("Simulación Bar UCP", "⚠️ La última secuencia generada no pasó el test de chi-cuadrado.\nPor favor, genere una nueva secuencia o valide la actual con la opción 6.")
            return
        lambd = CustomFloatDialog(self, "Simulación Bar UCP", "Ingrese una aproximación de la cantidad de alumnos que entran al bar por minuto:").result
        if lambd is None:
            return
        duracion = CustomDialog(self, "Simulación Bar UCP", "Ingrese la duración del recreo en segundos (ej: 600):", minvalue=1).result
        if duracion is None:
            return
        cant_cajeros = CustomDialog(self, "Simulación Bar UCP", "Ingrese la cantidad de cajeros:", minvalue=1).result
        if cant_cajeros is None:
            return
        cant_preparadores = CustomDialog(self, "Simulación Bar UCP", "Ingrese la cantidad de preparadores:", minvalue=1).result
        if cant_preparadores is None:
            return
        old_stdout = sys.stdout
        sys.stdout = self.stdout_redirector
        try:
            simular_bar_ucp(ui=self.ultima_secuencia_ui, lambd=lambd, duracion=duracion, 
                           cant_cajeros=cant_cajeros, cant_preparadores=cant_preparadores)
            # Forzar scroll arriba después de mostrar todos los resultados
            self.after_idle(lambda: self.text_result.yview_moveto(0))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def validar_secuencia(self, secuencia):
        print("\nRealizando validación automática con Test Chi-cuadrado...")
        resultado = chi_cuadrado(secuencia, k=10)
        mostrar_resultado(resultado)
        self.ultima_secuencia_valida = resultado['pasa']

def run_cuadrados_medios_custom(semilla, digitos, cantidad):
    from generadores.cuadrados_medios import cuadrados_medios, mostrar_resultados
    resultados = cuadrados_medios(semilla, digitos, cantidad)
    mostrar_resultados(resultados)
    ui = [r["U(n)"] for r in resultados]
    return resultados, ui

def run_fibonacci_custom(x0, x1, m, cantidad):
    from generadores.fibonacci import fibonacci, mostrar_resultados
    resultados = fibonacci(x0, x1, m, cantidad)
    mostrar_resultados(resultados)
    ui = [r["u_n"] for r in resultados]
    return resultados, ui

def run_congruencial_aditivo_custom(semillas, m, cantidad):
    from generadores.congruencial_aditivo import congruencial_aditivo, mostrar_resultados
    resultados = congruencial_aditivo(semillas, m, cantidad)
    mostrar_resultados(resultados)
    ui = [r["u_i"] for r in resultados]
    return resultados, ui

def run_congruencial_mixto_custom(x0, a, b, m, cantidad):
    from generadores.congruencial_mixto import congruencial_mixto, mostrar_resultados
    resultados = congruencial_mixto(x0, a, b, m, cantidad)
    mostrar_resultados(resultados)
    ui = [r["u_i"] for r in resultados]
    return resultados, ui

def run_congruencial_multiplicativo_custom(x0, a, m, cantidad):
    from generadores.congruencial_multiplicativo import congruencial_multiplicativo, mostrar_resultados
    resultados = congruencial_multiplicativo(x0, a, m, cantidad)
    mostrar_resultados(resultados)
    ui = [r["u_i"] for r in resultados]
    return resultados, ui

if __name__ == "__main__":
    app = App()
    app.mainloop() 