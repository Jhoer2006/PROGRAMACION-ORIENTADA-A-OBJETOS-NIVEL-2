import json

# =============================
# Clase Producto
# =============================
class Producto:
    def __init__(self, id_unico, nombre, cantidad, precio):
        self.id_unico = id_unico
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters
    def get_id(self):
        return self.id_unico

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def to_dict(self):
        """Convierte el producto en un diccionario (para guardarlo en JSON)"""
        return {
            "id": self.id_unico,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Producto desde un diccionario"""
        return Producto(data["id"], data["nombre"], data["cantidad"], data["precio"])


# =============================
# Clase Inventario
# =============================
class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.productos = {}  # Diccionario {id: Producto}
        self.archivo = archivo
        self.cargar_desde_archivo()

    # Añadir producto
    def agregar_producto(self, producto):
        if producto.get_id() in self.productos:
            print("⚠️ Ya existe un producto con ese ID.")
        else:
            self.productos[producto.get_id()] = producto
            self.guardar_en_archivo()
            print("✅ Producto añadido con éxito.")

    # Eliminar producto
    def eliminar_producto(self, id_unico):
        if id_unico in self.productos:
            del self.productos[id_unico]
            self.guardar_en_archivo()
            print("🗑️ Producto eliminado.")
        else:
            print("⚠️ No se encontró el producto.")

    # Actualizar producto
    def actualizar_producto(self, id_unico, cantidad=None, precio=None):
        if id_unico in self.productos:
            if cantidad is not None:
                self.productos[id_unico].set_cantidad(cantidad)
            if precio is not None:
                self.productos[id_unico].set_precio(precio)
            self.guardar_en_archivo()
            print("🔄 Producto actualizado.")
        else:
            print("⚠️ Producto no encontrado.")

    # Buscar por nombre
    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos.values() if p.get_nombre().lower() == nombre.lower()]
        if resultados:
            for p in resultados:
                print(f"🔎 {p.get_id()} - {p.get_nombre()} | Cantidad: {p.get_cantidad()} | Precio: {p.get_precio()}")
        else:
            print("⚠️ No se encontró ningún producto con ese nombre.")

    # Mostrar todos
    def mostrar_todos(self):
        if self.productos:
            print("\n📦 Inventario completo:")
            for p in self.productos.values():
                print(f"ID: {p.get_id()} | Nombre: {p.get_nombre()} | Cantidad: {p.get_cantidad()} | Precio: {p.get_precio()}")
        else:
            print("⚠️ El inventario está vacío.")

    # =============================
    # Manejo de Archivos
    # =============================
    def guardar_en_archivo(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump({id_: p.to_dict() for id_, p in self.productos.items()}, f, indent=4)
        except PermissionError:
            print("❌ Error: No tienes permisos para escribir en el archivo.")

    def cargar_desde_archivo(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.productos = {int(id_): Producto.from_dict(p) for id_, p in data.items()}
        except FileNotFoundError:
            print("📂 Archivo no encontrado. Se creará uno nuevo al guardar.")
            self.productos = {}
        except json.JSONDecodeError:
            print("⚠️ Archivo corrupto. Se reiniciará el inventario.")
            self.productos = {}


# =============================
# Interfaz de Usuario (Consola)
# =============================
def menu():
    inventario = Inventario()

    while True:
        print("\n=== MENÚ INVENTARIO ===")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos")
        print("6. Salir")

        opcion = input("Seleccione opción: ")

        if opcion == "1":
            id_unico = int(input("ID único: "))
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            inventario.agregar_producto(Producto(id_unico, nombre, cantidad, precio))

        elif opcion == "2":
            id_unico = int(input("ID del producto a eliminar: "))
            inventario.eliminar_producto(id_unico)

        elif opcion == "3":
            id_unico = int(input("ID del producto a actualizar: "))
            cantidad = input("Nueva cantidad (Enter para no cambiar): ")
            precio = input("Nuevo precio (Enter para no cambiar): ")
            inventario.actualizar_producto(
                id_unico,
                cantidad=int(cantidad) if cantidad else None,
                precio=float(precio) if precio else None
            )

        elif opcion == "4":
            nombre = input("Nombre del producto: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("👋 Saliendo del programa...")
            break

        else:
            print("⚠️ Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    menu()
