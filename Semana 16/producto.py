class Producto:
    def __init__(self, codigo: str, nombre: str, cantidad: int, precio: float):
        # Siempre manejar código como string para evitar inconsistencias
        self.codigo = str(codigo).strip()
        self.nombre = nombre.strip()
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.cantidad}) - ${self.precio:.2f}"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

