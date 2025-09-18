import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


# ------------------ Funciones ------------------

def agregar_evento():
    """Agrega un nuevo evento a la lista."""
    fecha = entry_fecha.get()
    hora = entry_hora.get()
    descripcion = entry_desc.get()

    if fecha and hora and descripcion:
        tree.insert("", "end", values=(fecha, hora, descripcion))
        entry_hora.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Por favor completa todos los campos.")


def eliminar_evento():
    """Elimina el evento seleccionado de la lista."""
    seleccionado = tree.selection()
    if seleccionado:
        confirmar = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este evento?")
        if confirmar:
            tree.delete(seleccionado)
    else:
        messagebox.showwarning("Error", "Selecciona un evento para eliminar.")


def salir():
    """Cierra la aplicación."""
    ventana.quit()


# ------------------ Ventana principal ------------------

ventana = tk.Tk()
ventana.title("Agenda Personal")
ventana.geometry("600x400")

# ------------------ Frame de entrada ------------------
frame_entrada = tk.Frame(ventana, padx=10, pady=10)
frame_entrada.pack(fill="x")

# Etiquetas y campos de entrada
tk.Label(frame_entrada, text="Fecha:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_fecha = DateEntry(frame_entrada, width=12, background="darkblue", foreground="white", borderwidth=2)
entry_fecha.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Hora:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_hora = tk.Entry(frame_entrada, width=10)
entry_hora.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_entrada, text="Descripción:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
entry_desc = tk.Entry(frame_entrada, width=25)
entry_desc.grid(row=0, column=5, padx=5, pady=5)

# ------------------ Frame de botones ------------------
frame_botones = tk.Frame(ventana, padx=10, pady=10)
frame_botones.pack(fill="x")

btn_agregar = tk.Button(frame_botones, text="Agregar Evento", command=agregar_evento, bg="lightgreen")
btn_agregar.pack(side="left", padx=5)

btn_eliminar = tk.Button(frame_botones, text="Eliminar Evento", command=eliminar_evento, bg="lightcoral")
btn_eliminar.pack(side="left", padx=5)

btn_salir = tk.Button(frame_botones, text="Salir", command=salir, bg="lightgray")
btn_salir.pack(side="right", padx=5)

# ------------------ Frame de lista ------------------
frame_lista = tk.Frame(ventana, padx=10, pady=10)
frame_lista.pack(fill="both", expand=True)

tree = ttk.Treeview(frame_lista, columns=("Fecha", "Hora", "Descripción"), show="headings")
tree.heading("Fecha", text="Fecha")
tree.heading("Hora", text="Hora")
tree.heading("Descripción", text="Descripción")
tree.pack(fill="both", expand=True)

# ------------------ Ejecutar ventana ------------------
ventana.mainloop()
