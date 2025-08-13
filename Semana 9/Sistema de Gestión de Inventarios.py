# =========================
# Sistema de Gestión de Inventarios
# =========================
# # Descripción: Este programa permite gestionar un inventario
# mediante un menú en consola, con funciones para añadir,
# eliminar, actualizar, buscar y mostrar productos.
# =========================

# -------------------------
# Clase Producto
# -------------------------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.
        :param id_producto: ID único del producto.
        :param nombre: Nombre del producto.
        :param cantidad: Cantidad en inventario.
        :param precio: Precio del producto.
        """
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Métodos Getters
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Métodos Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        """
        Representación en texto de un producto.
        """
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# -------------------------
# Clase Inventario
# -------------------------
class Inventario:
    def __init__(self):
        """
        Inicializa el inventario como una lista vacía.
        """
        self.productos = []

    def agregar_producto(self, producto):
        """
        Agrega un nuevo producto, verificando que el ID sea único.
        """
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("❌ Error: Ya existe un producto con ese ID.")
                return
        self.productos.append(producto)
        print("✅ Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto por ID.
        """
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("✅ Producto eliminado.")
                return
        print("❌ No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualiza la cantidad y/o precio de un producto por ID.
        """
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("✅ Producto actualizado.")
                return
        print("❌ No se encontró un producto con ese ID.")

    def buscar_producto(self, nombre):
        """
        Busca productos que contengan el nombre indicado.
        """
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("\n🔍 Resultados de búsqueda:")
            for p in resultados:
                print(p)
        else:
            print("❌ No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        """
        Muestra todos los productos del inventario.
        """
        if not self.productos:
            print("📦 El inventario está vacío.")
        else:
            print("\n📋 Lista de productos:")
            for p in self.productos:
                print(p)


# -------------------------
# Menú Interactivo
# -------------------------
def menu():
    inventario = Inventario()

    while True:
        print("\n=== SISTEMA DE GESTIÓN DE INVENTARIOS ===")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_prod = input("Ingrese ID único: ")
            nombre = input("Ingrese nombre: ")
            try:
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
            except ValueError:
                print("❌ Error: cantidad y precio deben ser números.")
                continue
            nuevo_producto = Producto(id_prod, nombre, cantidad, precio)
            inventario.agregar_producto(nuevo_producto)

        elif opcion == "2":
            id_prod = input("Ingrese ID del producto a eliminar: ")
            inventario.eliminar_producto(id_prod)

        elif opcion == "3":
            id_prod = input("Ingrese ID del producto a actualizar: ")
            try:
                nueva_cantidad = input("Ingrese nueva cantidad (dejar vacío si no cambia): ")
                nuevo_precio = input("Ingrese nuevo precio (dejar vacío si no cambia): ")

                nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else None
                nuevo_precio = float(nuevo_precio) if nuevo_precio else None
            except ValueError:
                print("❌ Error: cantidad y precio deben ser números.")
                continue
            inventario.actualizar_producto(id_prod, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            nombre = input("Ingrese el nombre o parte del nombre a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("❌ Opción inválida. Intente de nuevo.")


# -------------------------
# Punto de entrada del programa
# -------------------------
if __name__ == "__main__":
    menu()
