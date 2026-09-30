import tkinter as tk
import math
import re


class CalculadoraCientifica:
    def __init__(self):
        # =====================
        #    VENTANA PRINCIPAL
        # =====================
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora Científica")
        self.ventana.resizable(False, False)
        
        # =====================
        #    TEMAS
        # =====================
        self.tema_actual = "oscuro"
        self.temas = {
            "oscuro": {
                "fondo": "#2b2b2b",
                "pantalla_bg": "#1e1e1e",
                "pantalla_fg": "white",
                "historial_bg": "#1e1e1e",
                "historial_fg": "#aaa",
                "boton_num": "#505050",
                "boton_num_fg": "white",
                "boton_op": "#ff9500",
                "boton_eq": "#4CAF50",
                "boton_clear": "#f44336",
                "boton_sci": "#6a5acd",
                "texto": "white"
            },
            "claro": {
                "fondo": "#f5f5f5",
                "pantalla_bg": "white",
                "pantalla_fg": "black",
                "historial_bg": "white",
                "historial_fg": "#555",
                "boton_num": "#e0e0e0",
                "boton_num_fg": "black",
                "boton_op": "#ff9500",
                "boton_eq": "#4CAF50",
                "boton_clear": "#f44336",
                "boton_sci": "#6a5acd",
                "texto": "black"
            }
        }
        
        # Lista para guardar el historial internamente
        self.historial_datos = []
        
        # Lista para guardar referencias a los botones (para cambiar tema)
        self.botones = {}
        
        # =====================
        #    CREAR WIDGETS
        # =====================
        self.crear_historial()
        self.crear_pantalla()
        self.crear_botones()
        self.configurar_eventos()
        self.aplicar_tema()
        
        # Ajustar tamaño
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_reqwidth()
        alto = self.ventana.winfo_reqheight()
        self.ventana.geometry(f"{ancho}x{alto}")
        
        self.ventana.focus_force()
    
    # =====================
    #    HISTORIAL
    # =====================
    def crear_historial(self):
        self.historial = tk.Listbox(
            self.ventana,
            font=("Consolas", 10),
            height=4,
            selectbackground="#4CAF50",
            bd=0,
            highlightthickness=0
        )
        self.historial.pack(fill="x", padx=10, pady=(10, 5))
        self.historial.bind("<Double-Button-1>", self.usar_historial)
    
    def agregar_historial(self, operacion, resultado):
        """Agrega una operación al historial"""
        entrada = f"{operacion} = {resultado}"
        self.historial_datos.insert(0, (operacion, str(resultado)))
        self.historial.insert(0, entrada)
        # Limitar a 20 entradas
        if self.historial.size() > 20:
            self.historial.delete(20)
            self.historial_datos.pop()
    
    def usar_historial(self, event):
        """Al hacer doble clic en el historial, carga la operación"""
        seleccion = self.historial.curselection()
        if seleccion:
            operacion, _ = self.historial_datos[seleccion[0]]
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, operacion)
    
    # =====================
    #    PANTALLA
    # =====================
    def crear_pantalla(self):
        self.pantalla = tk.Entry(
            self.ventana,
            font=("Arial", 28, "bold"),
            justify="right",
            bd=0,
            insertbackground="white"
        )
        self.pantalla.pack(fill="x", padx=10, pady=5, ipady=15)
    
    # =====================
    #    BOTONES
    # =====================
    def crear_botones(self):
        # Frame para los botones (usamos grid aquí)
        self.frame_botones = tk.Frame(self.ventana, bd=0)
        self.frame_botones.pack(padx=10, pady=10)
        
        # Definición de botones: (texto, fila, columna, tipo)
        # Tipos: 'num', 'op', 'eq', 'clear', 'sci', 'especial'
        layout = [
            # Fila 0: Científicas
            ("sin", 0, 0, "sci"), ("cos", 0, 1, "sci"), ("tan", 0, 2, "sci"),
            ("√", 0, 3, "sci"), ("x²", 0, 4, "sci"), ("log", 0, 5, "sci"),
            # Fila 1: Números + paréntesis + backspace
            ("7", 1, 0, "num"), ("8", 1, 1, "num"), ("9", 1, 2, "num"),
            ("(", 1, 3, "op"), (")", 1, 4, "op"), ("←", 1, 5, "clear"),
            # Fila 2
            ("4", 2, 0, "num"), ("5", 2, 1, "num"), ("6", 2, 2, "num"),
            ("*", 2, 3, "op"), ("/", 2, 4, "op"), ("C", 2, 5, "clear"),
            # Fila 3
            ("1", 3, 0, "num"), ("2", 3, 1, "num"), ("3", 3, 2, "num"),
            ("+", 3, 3, "op"), ("-", 3, 4, "op"), ("", 3, 5, ""),
            # Fila 4
            ("π", 4, 0, "sci"), ("0", 4, 1, "num"), (".", 4, 2, "num"),
            ("=", 4, 3, "eq"), ("e", 4, 4, "sci"), ("🌓", 4, 5, "tema"),
        ]
        
        for texto, fila, columna, tipo in layout:
            if texto == "":
                continue
            
            if tipo == "num":
                comando = lambda t=texto: self.escribir(t)
            elif tipo == "op":
                comando = lambda t=texto: self.escribir(t)
            elif tipo == "sci":
                comando = lambda t=texto: self.escribir_funcion(t)
            elif tipo == "clear":
                if texto == "C":
                    comando = self.borrar
                else:
                    comando = self.borrar_ultimo
            elif tipo == "eq":
                comando = self.calcular
            elif tipo == "tema":
                comando = self.cambiar_tema
            else:
                comando = None
            
            boton = tk.Button(
                self.frame_botones,
                text=texto,
                font=("Arial", 14, "bold"),
                width=4,
                height=2,
                bd=0,
                relief="flat",
                command=comando
            )
            boton.grid(row=fila, column=columna, padx=2, pady=2, sticky="nswe")
            
            # Guardar referencia con su tipo
            self.botones[boton] = tipo
        
        # Configurar columnas para que se expandan
        for i in range(6):
            self.frame_botones.columnconfigure(i, weight=1)
    
    # =====================
    #    FUNCIONES DE ESCRITURA
    # =====================
    def escribir(self, valor):
        actual = self.pantalla.get()
        
        # Validar punto decimal
        if valor == ".":
            numeros = actual.split("+")[-1].split("-")[-1].split("*")[-1].split("/")[-1]
            if "." in numeros:
                return
        
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(0, actual + valor)
    
    def escribir_funcion(self, valor):
        """Escribe funciones científicas con paréntesis"""
        actual = self.pantalla.get()
        self.pantalla.delete(0, tk.END)
        
        # Para x², usamos ^2
        if valor == "x²":
            self.pantalla.insert(0, actual + "^2")
        # Para √, escribimos √(
        elif valor == "√":
            self.pantalla.insert(0, actual + "√(")
        # Para sin, cos, tan, log, escribimos función(
        else:
            self.pantalla.insert(0, actual + valor + "(")
    
    def borrar(self):
        self.pantalla.delete(0, tk.END)
    
    def borrar_ultimo(self):
        actual = self.pantalla.get()
        if actual:
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, actual[:-1])
    
    # =====================
    #    CÁLCULO
    # =====================
    def preprocesar(self, expr):
        """Convierte la expresión del usuario a código Python válido"""
        # Constantes
        expr = expr.replace("π", f"({math.pi})")
        expr = re.sub(r'\be\b', f'({math.e})', expr)
        
        # Funciones trigonométricas (grados → radianes)
        expr = re.sub(r'sin\(', 'math.sin(math.radians(', expr)
        expr = re.sub(r'cos\(', 'math.cos(math.radians(', expr)
        expr = re.sub(r'tan\(', 'math.tan(math.radians(', expr)
        
        # Raíz cuadrada
        expr = expr.replace('√(', 'math.sqrt(')
        
        # Logaritmo base 10
        expr = re.sub(r'(?<!\w)log\(', 'math.log10(', expr)
        
        # Potencia
        expr = expr.replace('^', '**')
        
        return expr
    
    def calcular(self):
        try:
            expresion = self.pantalla.get()
            if not expresion:
                return
            
            # Balancear paréntesis
            abiertos = expresion.count('(')
            cerrados = expresion.count(')')
            expresion += ')' * (abiertos - cerrados)
            
            # Guardar la expresión original para el historial
            expresion_original = self.pantalla.get()
            
            # Preprocesar funciones científicas
            expresion_proc = self.preprocesar(expresion)
            
            # Evaluar
            resultado = eval(expresion_proc)
            
            # Formatear resultado (quitar .0 si es entero)
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)
            elif isinstance(resultado, float):
                resultado = round(resultado, 10)
            
            # Agregar al historial
            self.agregar_historial(expresion_original, resultado)
            
            # Mostrar resultado
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, str(resultado))
        except ZeroDivisionError:
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, "Error: ÷0")
        except Exception:
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, "Error")
    
    # =====================
    #    TEMAS
    # =====================
    def cambiar_tema(self):
        self.tema_actual = "claro" if self.tema_actual == "oscuro" else "oscuro"
        self.aplicar_tema()
    
    def aplicar_tema(self):
        colores = self.temas[self.tema_actual]
        
        # Ventana principal
        self.ventana.configure(bg=colores["fondo"])
        
        # Pantalla
        self.pantalla.configure(
            bg=colores["pantalla_bg"],
            fg=colores["pantalla_fg"],
            insertbackground=colores["pantalla_fg"]
        )
        
        # Historial
        self.historial.configure(
            bg=colores["historial_bg"],
            fg=colores["historial_fg"]
        )
        
        # Frame de botones
        self.frame_botones.configure(bg=colores["fondo"])
        
        # Botones según su tipo
        for boton, tipo in self.botones.items():
            if tipo == "num":
                boton.configure(
                    bg=colores["boton_num"],
                    fg=colores["boton_num_fg"],
                    activebackground=colores["boton_num"]
                )
            elif tipo == "op":
                boton.configure(
                    bg=colores["boton_op"],
                    fg="white",
                    activebackground=colores["boton_op"]
                )
            elif tipo == "eq":
                boton.configure(
                    bg=colores["boton_eq"],
                    fg="white",
                    activebackground=colores["boton_eq"]
                )
            elif tipo == "clear":
                boton.configure(
                    bg=colores["boton_clear"],
                    fg="white",
                    activebackground=colores["boton_clear"]
                )
            elif tipo == "sci":
                boton.configure(
                    bg=colores["boton_sci"],
                    fg="white",
                    activebackground=colores["boton_sci"]
                )
            elif tipo == "tema":
                boton.configure(
                    bg=colores["boton_num"],
                    fg=colores["boton_num_fg"],
                    activebackground=colores["boton_num"]
                )
    
    # =====================
    #    EVENTOS DE TECLADO
    # =====================
    def configurar_eventos(self):
        # Números
        for i in range(10):
            self.ventana.bind(f"<Key-{i}>", lambda e, n=str(i): self.escribir(n))
        
        # Operadores
        self.ventana.bind("<Key-+>", lambda e: self.escribir("+"))
        self.ventana.bind("<Key-->", lambda e: self.escribir("-"))
        self.ventana.bind("<Key-*>", lambda e: self.escribir("*"))
        self.ventana.bind("<Key-/>", lambda e: self.escribir("/"))
        self.ventana.bind("<Key-.>", lambda e: self.escribir("."))
        self.ventana.bind("<Key-(>", lambda e: self.escribir("("))
        self.ventana.bind("<Key-)>", lambda e: self.escribir(")"))
        
        # Teclas especiales
        self.ventana.bind("<Return>", lambda e: (self.calcular(), "break")[1])
        self.ventana.bind("<KP_Enter>", lambda e: (self.calcular(), "break")[1])
        self.ventana.bind("<BackSpace>", lambda e: (self.borrar_ultimo(), "break")[1])
        self.ventana.bind("<Escape>", lambda e: (self.borrar(), "break")[1])
        self.ventana.bind("<Delete>", lambda e: (self.borrar(), "break")[1])
    
    # =====================
    #    INICIAR
    # =====================
    def ejecutar(self):
        self.ventana.mainloop()


# =====================
#    EJECUTAR LA APP
# =====================
if __name__ == "__main__":
    app = CalculadoraCientifica()
    app.ejecutar()