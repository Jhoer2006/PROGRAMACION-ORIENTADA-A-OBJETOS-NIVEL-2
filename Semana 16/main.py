import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
from form_producto import FormProducto
from inventario import Inventario

APP_W, APP_H = 980, 620

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UEA - Sistema de Gestión de Inventario (POO)")
        self.geometry(f"{APP_W}x{APP_H}")
        self.resizable(False, False)

        self.inventario = Inventario()

        # ---------- Fondo ----------
        self._bg_img = Image.open("FONDO-1.jpeg").resize((APP_W, APP_H))
        self._bg_photo = ImageTk.PhotoImage(self._bg_img)
        canvas = tk.Canvas(self, width=APP_W, height=APP_H, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor="nw", image=self._bg_photo)

        # ... imports y clase App arriba iguales ...

        # ---------- Panel central ----------
        panel = ttk.Frame(canvas, padding=20)
        canvas.create_window(APP_W // 2, 210, window=panel, anchor="center")

        # Logo
        logo_img = Image.open("logo_uea.png")
        max_w = 460
        ratio = max_w / logo_img.width
        logo_img = logo_img.resize((int(logo_img.width * ratio), int(logo_img.height * ratio)), Image.LANCZOS)
        self._logo_photo = ImageTk.PhotoImage(logo_img)
        ttk.Label(panel, image=self._logo_photo).grid(row=0, column=0, pady=(0, 10))

        # Textos institucionales
        ttk.Label(panel, text="UNIVERSIDAD ESTATAL AMAZÓNICA", font=("Segoe UI", 14, "bold")).grid(row=1, column=0, pady=2)
        ttk.Label(panel, text="Ingeniería en Tecnologías de la Información", font=("Segoe UI", 11)).grid(row=2, column=0)
        ttk.Label(panel, text="Programación Orientada a Objetos", font=("Segoe UI", 10)).grid(row=3, column=0, pady=(0, 8))

        # Información de estudiantes
        ttk.Label(panel, text="Estudiantes:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, pady=(10, 0))
        ttk.Label(panel, text="Jhoer Fernando Fernández Medina").grid(row=5, column=0)
        ttk.Label(panel, text="María Elizabeth González Bravo").grid(row=6, column=0)
        ttk.Label(panel, text="Liz Sandra Peña Véliz").grid(row=7, column=0)


        # ---------- Menú ----------
        menu = tk.Menu(self)
        self.config(menu=menu)
        opciones = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Opciones", menu=opciones)
        opciones.add_command(label="Productos", command=self._abrir_productos)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.destroy)

        # Botón grande igual al menú (por si el profe quiere clic visual)
        ttk.Button(self, text="Abrir Productos", command=self._abrir_productos).place(x=APP_W//2-80, y=APP_H-90, width=160, height=36)

        # Atajo para cerrar
        self.bind("<Escape>", lambda e: self.destroy())

    def _abrir_productos(self):
        FormProducto(self, self.inventario)

if __name__ == "__main__":
    App().mainloop()
