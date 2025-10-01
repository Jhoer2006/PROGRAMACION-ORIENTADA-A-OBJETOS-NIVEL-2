import json
from pathlib import Path
from producto import Producto

class Inventario:
    def __init__(self, archivo: str = "inventario.txt"):
        self.archivo = Path(archivo)
        self.productos: list[Producto] = []
        self.cargar()

    # ---------- CRUD ----------
    def agregar(self, producto: Producto) -> bool:
        # Evitar duplicados por código
        if any(p.codigo == producto.codigo for p in self.productos):
            return False
        self.productos.append(producto)
        self.guardar()
        return True

    def eliminar(self, codigo: str) -> bool:
        codigo = str(codigo).strip()
        antes = len(self.productos)
        self.productos = [p for p in self.productos if p.codigo != codigo]
        self.guardar()
        return len(self.productos) < antes

    def modificar(self, codigo: str, nombre: str, cantidad: int, precio: float) -> bool:
        codigo = str(codigo).strip()
        for p in self.productos:
            if p.codigo == codigo:
                p.nombre = nombre.strip()
                p.cantidad = int(cantidad)
                p.precio = float(precio)
                self.guardar()
                return True
        return False

    def listar(self) -> list:
        return list(self.productos)

    # ---------- Persistencia ----------
    def guardar(self) -> None:
        data = [p.to_dict() for p in self.productos]
        self.archivo.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def cargar(self) -> None:
        if not self.archivo.exists() or self.archivo.stat().st_size == 0:
            self.productos = []
            return
        try:
            data = json.loads(self.archivo.read_text(encoding="utf-8"))
            self.productos = [Producto(**d) for d in data]
        except Exception:
            # Si el archivo está corrupto, no romper la app
            self.productos = []

