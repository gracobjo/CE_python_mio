import tkinter as tk

# --- 1. Crear la ventana principal ---
ventana = tk.Tk()
ventana.title("Mi Primera App")      # Título en la barra superior
ventana.geometry("400x200")          # Tamaño: 300px de ancho, 200px de alto

# --- 2. Crear una función (lo que pasará al hacer clic) ---
def saludar():
    # Cambiamos el texto de la etiqueta cuando se hace clic
    etiqueta.config(text="¡Hola! Has hecho clic en el botón 🎉", fg="green")

# --- 3. Crear los Widgets (los componentes) ---
# Una etiqueta de texto
etiqueta = tk.Label(ventana, text="Bienvenido a Tkinter", font=("Arial", 16))

# Un botón. 'command' llama a la función 'saludar'
boton = tk.Button(ventana, text="Haz clic aquí", command=saludar, bg="lightblue")

# --- 4. Organizar los Widgets en la ventana ---
etiqueta.pack(pady=20)  # pady añade espacio vertical (padding en Y)
boton.pack()

# --- 5. Iniciar el bucle principal ---
ventana.mainloop()