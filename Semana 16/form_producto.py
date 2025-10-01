# form_producto.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image, ImageTk  # pip install pillow
from producto import Producto


def _to_decimal(x) -> Decimal:
    """Convierte con seguridad a Decimal (maneja '', None, etc.)."""
    try:
        s = str(x).strip()
        if s == "":
            return Decimal("0")
        return Decimal(s)
    except Exception:
        return Decimal("0")


class FormProducto(tk.Toplevel):
    def __init__(self, parent, inventario):
        super().__init__(parent)
        self.title("Productos")
        self.geometry("900x540")
        self.resizable(False, False)
        self.inventario = inventario
        self._box_photo = None  # mantener referencia a imagen

        # --------- Estilos ----------
        style = ttk.Style(self)
        style.configure("Toolbar.TButton", padding=(10, 6))
        style.configure("Treeview", rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TFrame", padding=16)
        style.configure("Big.TButton", padding=(14, 8))
        style.configure("Emph.TLabel", font=("Segoe UI", 10, "bold"))

        # --------- TOP: Buscar + Toolbar ----------
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=(12, 8))

        ttk.Label(top, text="Buscar:").pack(side=tk.LEFT, padx=(0, 6))
        self.var_buscar = tk.StringVar()
        ent_buscar = ttk.Entry(top, textvariable=self.var_buscar, width=38)
        ent_buscar.pack(side=tk.LEFT)
        ttk.Button(top, text="🔎 Buscar", style="Toolbar.TButton",
                   command=self._buscar).pack(side=tk.LEFT, padx=6)

        toolbar = ttk.Frame(top)
        toolbar.pack(side=tk.RIGHT)
        ttk.Button(toolbar, text="➕ Nuevo", style="Toolbar.TButton",
                   command=self._nuevo).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="✏️ Modificar", style="Toolbar.TButton",
                   command=self._modificar).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="🗑️ Eliminar", style="Toolbar.TButton",
                   command=self._eliminar).pack(side=tk.LEFT, padx=4)

        # --------- TABLA (con columna TOTAL) ----------
        cols = ("codigo", "nombre", "cantidad", "precio", "total")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)

        headers = (
            ("codigo",   "Código",   110, "center"),
            ("nombre",   "Nombre",   360, "w"),
            ("cantidad", "Cantidad", 110, "center"),
            ("precio",   "Precio",   140, "e"),
            ("total",    "Total",    140, "e"),
        )
        for c, txt, w, anchor in headers:
            self.tree.heading(c, text=txt, command=lambda k=c: self._ordenar_por(k, False))
            self.tree.column(c, width=w, anchor=anchor, stretch=False)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0), pady=(0, 12))
        vsb.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12), pady=(0, 12))

        # Zebra rows
        self.tree.tag_configure("even", background="#f6f7fb")
        self.tree.tag_configure("odd", background="white")

        # --------- STATUS BAR (resumen) ----------
        self.status = ttk.Label(self, anchor="w")
        self.status.pack(fill=tk.X, padx=12, pady=(0, 10))

        # --------- CONTEXT MENU (clic derecho) ----------
        self.menu_ctx = tk.Menu(self, tearoff=0)
        self.menu_ctx.add_command(label="Modificar", command=self._modificar)
        self.menu_ctx.add_command(label="Eliminar", command=self._eliminar)
        self.tree.bind("<Button-3>", self._abrir_menu_ctx)

        # --------- Atajos ----------
        self.bind("<Delete>", lambda e: self._eliminar())
        self.bind("<Escape>", lambda e: self.destroy())
        ent_buscar.bind("<KeyRelease>", lambda e: self._refrescar(self.var_buscar.get()))

        self._refrescar()

    # ---------- Helpers ----------
    def _abrir_menu_ctx(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.tree.focus(iid)
        self.menu_ctx.tk_popup(event.x_root, event.y_root)

    def _resumen_inventario(self, productos):
        total_items = sum(int(p.cantidad) for p in productos)
        total_valor = sum(
            (_to_decimal(p.cantidad) * _to_decimal(p.precio) for p in productos),
            start=Decimal("0")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.status.config(
            text=f"{len(productos)} producto(s) | Ítems: {total_items} | Valor total: ${total_valor:,.2f}"
        )

    def _refrescar(self, filtro: str | None = None):
        self.tree.delete(*self.tree.get_children())
        productos = self.inventario.listar()
        if filtro:
            f = filtro.lower().strip()
            productos = [p for p in productos if f in p.codigo.lower() or f in p.nombre.lower()]

        for i, p in enumerate(productos):
            tag = "even" if i % 2 == 0 else "odd"
            precio = _to_decimal(p.precio).quantize(Decimal("0.01"))
            total = (_to_decimal(p.cantidad) * _to_decimal(p.precio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            precio_fmt = f"${precio:,.2f}"
            total_fmt = f"${total:,.2f}"
            self.tree.insert("", tk.END,
                             values=(p.codigo, p.nombre, p.cantidad, precio_fmt, total_fmt),
                             tags=(tag,))
        self._resumen_inventario(productos)

    def _buscar(self):
        self._refrescar(self.var_buscar.get())

    def _seleccion(self):
        iid = self.tree.focus() or (self.tree.selection()[0] if self.tree.selection() else None)
        if not iid:
            return None
        return self.tree.item(iid, "values")

    # ---------- Acciones ----------
    def _nuevo(self):
        self._form_producto("Nuevo Producto")

    def _modificar(self):
        valores = self._seleccion()
        if not valores:
            messagebox.showwarning("Atención", "Seleccione un producto para modificar.")
            return
        self._form_producto("Modificar Producto", valores)

    def _eliminar(self):
        valores = self._seleccion()
        if not valores:
            messagebox.showinfo("Información", "Seleccione un producto para eliminar.")
            return
        codigo = str(valores[0]).strip()
        if messagebox.askyesno("Confirmar", f"¿Eliminar el producto con código {codigo}?"):
            ok = self.inventario.eliminar(codigo)
            if not ok:
                messagebox.showerror("Error", "No se pudo eliminar. Intente nuevamente.")
            self._refrescar(self.var_buscar.get())

    # ---------- Formulario bonito: NUEVO / MODIFICAR ----------
    def _form_producto(self, titulo: str, valores=None):
        win = tk.Toplevel(self)
        win.title(titulo)
        win.resizable(False, False)

        padd = {"padx": 12, "pady": 8}

        # Card contenedor
        card = ttk.Frame(win, style="Card.TFrame")
        card.grid(row=0, column=0, sticky="nsew")
        win.grid_columnconfigure(0, weight=1)

        # Izquierda: imagen/emoji
        left = ttk.Frame(card)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 16))

        img_label = ttk.Label(left)
        img_label.grid(row=0, column=0, pady=(0, 6))

        # Cargar box.png si existe; si no, emoji
        if os.path.exists("box.png"):
            try:
                _img = Image.open("box.png")
                _img.thumbnail((120, 120), Image.LANCZOS)
                self._box_photo = ImageTk.PhotoImage(_img)
                img_label.configure(image=self._box_photo)
            except Exception:
                img_label.configure(text="📦", font=("Segoe UI Emoji", 40))
        else:
            img_label.configure(text="📦", font=("Segoe UI Emoji", 40))

        ttk.Label(left, text="Producto", style="Emph.TLabel").grid(row=1, column=0)

        # Derecha: campos
        right = ttk.Frame(card)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(right, text="Código:").grid(row=0, column=0, sticky="e", **padd)
        ttk.Label(right, text="Nombre:").grid(row=1, column=0, sticky="e", **padd)
        ttk.Label(right, text="Cantidad:").grid(row=2, column=0, sticky="e", **padd)
        ttk.Label(right, text="Precio (USD):").grid(row=3, column=0, sticky="e", **padd)

        var_codigo   = tk.StringVar()
        var_nombre   = tk.StringVar()
        var_cantidad = tk.StringVar(value="1")      # StringVar para evitar errores cuando queda vacío
        var_precio   = tk.StringVar(value="0.00")   # idem

        e_cod = ttk.Entry(right, textvariable=var_codigo, width=34)
        e_nom = ttk.Entry(right, textvariable=var_nombre, width=34)

        sp_can = ttk.Spinbox(
            right, textvariable=var_cantidad, from_=0, to=1_000_000,
            increment=1, width=10, justify="center"
        )
        sp_pre = ttk.Spinbox(
            right, textvariable=var_precio, from_=0.0, to=1_000_000.0,
            increment=0.1, width=10, justify="center", format="%.2f"
        )

        e_cod.grid(row=0, column=1, **padd, sticky="w")
        e_nom.grid(row=1, column=1, **padd, sticky="w")
        sp_can.grid(row=2, column=1, **padd, sticky="w")
        sp_pre.grid(row=3, column=1, **padd, sticky="w")

        # Total en vivo con Decimal (preciso)
        total_var = tk.StringVar(value="$0.00")

        def actualizar_total(*_):
            q = _to_decimal(var_cantidad.get())
            p = _to_decimal(var_precio.get())
            t = (q * p).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_var.set(f"${t:,.2f}")

        var_cantidad.trace_add("write", actualizar_total)
        var_precio.trace_add("write", actualizar_total)
        actualizar_total()

        ttk.Label(right, text="Total:", style="Emph.TLabel").grid(row=4, column=0, sticky="e", **padd)
        ttk.Label(right, textvariable=total_var).grid(row=4, column=1, sticky="w", **padd)

        # Si es Modificar, precargar datos
        if valores:
            var_codigo.set(str(valores[0]))
            var_nombre.set(str(valores[1]))
            try:
                var_cantidad.set(str(int(str(valores[2]).replace(",", ""))))
            except Exception:
                var_cantidad.set("0")
            try:
                limpio = str(valores[3]).replace("$", "").replace(",", "")
                var_precio.set(f"{_to_decimal(limpio).quantize(Decimal('0.01'))}")
            except Exception:
                var_precio.set("0.00")
            e_cod.state(["disabled"])

        # Botones
        btns = ttk.Frame(card)
        btns.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="e")
        b_guardar = ttk.Button(btns, text="Guardar", style="Big.TButton")
        b_cancel  = ttk.Button(btns, text="Cancelar", command=win.destroy)
        b_guardar.pack(side=tk.RIGHT, padx=6)
        b_cancel.pack(side=tk.RIGHT)

        def guardar():
            try:
                codigo = var_codigo.get().strip()
                nombre = var_nombre.get().strip()
                cantidad = int(_to_decimal(var_cantidad.get()))
                precio_dec = _to_decimal(var_precio.get()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                precio = float(precio_dec)  # para JSON, pero ya con 2 decimales
                if not codigo or not nombre:
                    raise ValueError("Código y Nombre son obligatorios.")
                if cantidad < 0 or precio < 0:
                    raise ValueError("Cantidad y precio deben ser positivos.")
            except Exception as ex:
                messagebox.showerror("Datos inválidos", str(ex), parent=win)
                return

            if valores:  # modificar
                ok = self.inventario.modificar(codigo, nombre, cantidad, precio)
                if not ok:
                    messagebox.showerror("Error", "No se pudo modificar el producto.", parent=win)
            else:        # nuevo
                ok = self.inventario.agregar(Producto(codigo, nombre, cantidad, precio))
                if not ok:
                    messagebox.showwarning("Duplicado", f"Ya existe un producto con código {codigo}.", parent=win)
                    return

            self._refrescar(self.var_buscar.get())
            win.destroy()

        b_guardar.configure(command=guardar)

        # accesos rápidos
        win.bind("<Return>", lambda e: guardar())
        win.bind("<Escape>", lambda e: win.destroy())
        e_cod.focus_set()

    # ---------- Ordenar por columna ----------
    def _ordenar_por(self, col, reverse):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        def _key(v):
            # cantidad, precio y total se ordenan como número
            if col in ("cantidad", "precio", "total"):
                try:
                    return float(str(v).replace("$", "").replace(",", ""))
                except:
                    return 0.0
            return str(v).lower()
        items.sort(key=lambda t: _key(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)
        for i, k in enumerate(self.tree.get_children("")):
            self.tree.item(k, tags=("even" if i % 2 == 0 else "odd",))
        self.tree.heading(col, command=lambda: self._ordenar_por(col, not reverse))

