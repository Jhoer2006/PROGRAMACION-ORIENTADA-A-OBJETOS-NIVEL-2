import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

# -----------------------------
# Aplicacion: Lista de Tareas
# - Entry para escribir nueva tarea
# - Treeview para mostrar tareas
# - Botones: Añadir, Marcar como Completada, Eliminar
# - Enter en Entry agrega tarea; doble click marca/ desmarca
# -----------------------------


class ListaTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("500x420")

        # --- Frame de entrada ---
        frame_in = tk.Frame(root, padx=10, pady=10)
        frame_in.pack(fill="x")

        lbl = tk.Label(frame_in, text="Nueva tarea:")
        lbl.grid(row=0, column=0, sticky="w")

        # Campo de texto para nueva tarea
        self.entry_tarea = tk.Entry(frame_in, width=50)
        self.entry_tarea.grid(row=0, column=1, padx=8)
        self.entry_tarea.focus_set()

        # Bind: presionar Enter agrega la tarea
        self.entry_tarea.bind("<Return>", self.añadir_tarea_event)

        # --- Frame de botones ---
        frame_btns = tk.Frame(root, padx=10, pady=5)
        frame_btns.pack(fill="x")

        btn_añadir = tk.Button(frame_btns, text="➕ Añadir Tarea", width=15, command=self.añadir_tarea)
        btn_añadir.pack(side="left", padx=6)

        btn_marcar = tk.Button(frame_btns, text="✅ Marcar como Completada", width=20, command=self.marcar_completada)
        btn_marcar.pack(side="left", padx=6)

        btn_eliminar = tk.Button(frame_btns, text="❌ Eliminar Tarea", width=15, command=self.eliminar_tarea)
        btn_eliminar.pack(side="left", padx=6)

        # --- Frame de lista (Treeview) ---
        frame_lista = tk.Frame(root, padx=10, pady=10)
        frame_lista.pack(fill="both", expand=True)

        # Usamos Treeview por facilidad de tags/estilos
        self.tree = ttk.Treeview(frame_lista, columns=("tarea",), show="headings", selectmode="browse")
        self.tree.heading("tarea", text="Tareas")
        self.tree.column("tarea", anchor="w")
        self.tree.pack(fill="both", expand=True, side="left")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Configurar estilos / fuentes para 'completado' (tachado)
        default_font = tkfont.nametofont("TkDefaultFont").copy()
        strike_font = default_font.copy()
        strike_font.configure(overstrike=1)  # activar tachado (overstrike)

        # Tag para completadas: texto gris y tachado
        self.tree.tag_configure("completed", foreground="gray40", font=strike_font)
        # Tag para pendientes: font normal
        self.tree.tag_configure("pending", foreground="black", font=default_font)

        # Bind: doble click en item => marcar/desmarcar completada
        self.tree.bind("<Double-1>", self._on_double_click)

        # Mensaje de ayuda (opcional)
        ayuda = tk.Label(root, text="Doble clic en una tarea para marcar/desmarcar como completada.", fg="gray60")
        ayuda.pack(pady=(0, 8))

    # -------------------------
    # Funciones de la app
    # -------------------------
    def añadir_tarea_event(self, event):
        """Wrapper para binding de Enter."""
        self.añadir_tarea()

    def añadir_tarea(self):
        """Añade la tarea ingresada al Treeview con tag 'pending'."""
        texto = self.entry_tarea.get().strip()
        if not texto:
            messagebox.showwarning("Atención", "No puedes añadir una tarea vacía.")
            return
        # Insertar en la lista con tag pending
        self.tree.insert("", tk.END, values=(texto,), tags=("pending",))
        self.entry_tarea.delete(0, tk.END)

    def marcar_completada(self):
        """Marca o desmarca la tarea seleccionada como completada (toggle)."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una tarea para marcarla como completada.")
            return
        item = sel[0]
        tags = list(self.tree.item(item, "tags"))
        if "completed" in tags:
            # desmarcar -> dejar 'pending'
            self.tree.item(item, tags=("pending",))
        else:
            # marcar completada
            self.tree.item(item, tags=("completed",))

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una tarea para eliminar.")
            return
        # Confirmacion opcional
        respuesta = messagebox.askyesno("Confirmar", "¿Deseas eliminar la tarea seleccionada?")
        if respuesta:
            for item in sel:
                self.tree.delete(item)

    def _on_double_click(self, event):
        """Handler del doble clic: marca/desmarca la tarea en la fila doble clickeada."""
        # identificar item debajo del cursor
        item = self.tree.identify_row(event.y)
        if not item:
            return
        tags = list(self.tree.item(item, "tags"))
        if "completed" in tags:
            self.tree.item(item, tags=("pending",))
        else:
            self.tree.item(item, tags=("completed",))


# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = ListaTareasApp(root)
    root.mainloop()
