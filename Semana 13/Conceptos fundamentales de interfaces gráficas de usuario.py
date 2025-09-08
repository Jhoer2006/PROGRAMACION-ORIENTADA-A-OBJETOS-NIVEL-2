import tkinter as tk
from tkinter import messagebox

# ---------------------------
# Clase de la Aplicación GUI
# ---------------------------
class AplicacionGUI:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Aplicación de Gestión de Datos")
        self.root.geometry("400x300")  # tamaño de ventana
        self.root.resizable(False, False)  # bloquear redimensionado

        # Etiqueta principal
        self.label = tk.Label(root, text="Ingrese un dato:", font=("Arial", 12))
        self.label.pack(pady=10)

        # Campo de texto
        self.entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.entry.pack(pady=5)

        # Botón Agregar
        self.btn_agregar = tk.Button(root, text="Agregar", command=self.agregar_dato, bg="lightgreen")
        self.btn_agregar.pack(pady=5)

        # Lista para mostrar los datos agregados
        self.lista = tk.Listbox(root, width=40, height=8, font=("Arial", 11))
        self.lista.pack(pady=10)

        # Botón Limpiar
        self.btn_limpiar = tk.Button(root, text="Limpiar", command=self.limpiar_datos, bg="lightcoral")
        self.btn_limpiar.pack(pady=5)

    # ---------------------------
    # Función para agregar datos
    # ---------------------------
    def agregar_dato(self):
        dato = self.entry.get().strip()
        if dato:  # validar que no esté vacío
            self.lista.insert(tk.END, dato)
            self.entry.delete(0, tk.END)  # limpiar campo de texto
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un dato antes de agregarlo.")

    # ---------------------------
    # Función para limpiar datos
    # ---------------------------
    def limpiar_datos(self):
        seleccion = self.lista.curselection()  # verifica si hay un item seleccionado
        if seleccion:
            self.lista.delete(seleccion)  # elimina solo el seleccionado
        else:
            # Preguntar si quiere borrar todo
            respuesta = messagebox.askyesno("Confirmar", "¿Desea limpiar toda la lista?")
            if respuesta:
                self.lista.delete(0, tk.END)


# ---------------------------
# Punto de entrada del programa
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGUI(root)
    root.mainloop()
