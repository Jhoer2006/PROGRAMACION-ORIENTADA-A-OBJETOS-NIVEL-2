# =========================
# Sistema de Gestión de Inventarios - Versión Mejorada (con archivos y excepciones)
# =========================
# Autor: (pon tu nombre)
# Lenguaje: Python 3.x
# Descripción:
#   - Gestión de inventario con persistencia en archivo de texto (JSON en inventario.txt).
#   - Manejo de excepciones para errores comunes de archivo.
#   - Escritura atómica para evitar archivos dañados.
#   - Menú de consola con notificaciones de éxito/fracaso en operaciones.
# =========================

import json
import os
from datetime import datetime


# -------------------------
# Clase Producto
# -------------------------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = str(id_producto)
        self.nombre = str(nombre)
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    def set_nombre(self, nombre):
        self.nombre = str(nombre)

    def set_cantidad(self, cantidad):
        self.cantidad = int(cantidad)

    def set_precio(self, precio):
        self.precio = float(precio)

    def to_dict(self):
        return {
            "id": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    @staticmethod
    def from_dict(d):
        return Producto(d["id"], d["nombre"], d["cantidad"], d["precio"])

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# -------------------------
# Clase Inventario
# -------------------------
class Inventario:
    def __init__(self, ruta_archivo="inventario.txt"):
        self.productos = []
        self.ruta_archivo = ruta_archivo
        self._cargar_archivo()

    def _guardar_archivo(self):
        tmp_path = self.ruta_archivo + ".tmp"
        try:
            data = [p.to_dict() for p in self.productos]
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.ruta_archivo)
            print(f"💾 Cambios guardados en '{self.ruta_archivo}'.")
            return True
        except PermissionError:
            print("❌ Permiso denegado: no se pudo escribir en el archivo.")
            return False
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")
            return False

    def _cargar_archivo(self):
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
            print("🆕 Archivo de inventario creado.")
            return

        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.productos = [Producto.from_dict(item) for item in data]
            print(f"📂 {len(self.productos)} producto(s) cargado(s).")
        except json.JSONDecodeError:
            backup = f"{self.ruta_archivo}.corrupt-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            os.rename(self.ruta_archivo, backup)
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
            print(f"⚠️ Archivo corrupto renombrado a {backup}. Nuevo archivo creado.")
        except FileNotFoundError:
            print("❌ Archivo no encontrado. Se creará uno nuevo.")
        except PermissionError:
            print("❌ Permiso denegado al leer el archivo.")
        except Exception as e:
            print(f"❌ Error al cargar archivo: {e}")

    def agregar_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print("❌ Ya existe un producto con ese ID.")
            return
        self.productos.append(producto)
        self._guardar_archivo()

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                self._guardar_archivo()
                print("✅ Producto eliminado.")
                return
        print("❌ No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                self._guardar_archivo()
                print("✅ Producto actualizado.")
                return
        print("❌ No se encontró un producto con ese ID.")

    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("\n🔍 Resultados:")
            for p in resultados:
                print(p)
        else:
            print("❌ No se encontraron productos.")

    def mostrar_todos(self):
        if not self.productos:
            print("📦 Inventario vacío.")
        else:
            print("\n📋 Inventario:")
            for p in self.productos:
                print(p)


# -------------------------
# Menú Interactivo
# -------------------------
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
            id_prod = input("ID único: ")
            nombre = input("Nombre: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
            except ValueError:
                print("❌ Error: cantidad y precio deben ser números.")
                continue
            inventario.agregar_producto(Producto(id_prod, nombre, cantidad, precio))

        elif opcion == "2":
            id_prod = input("ID a eliminar: ")
            inventario.eliminar_producto(id_prod)

        elif opcion == "3":
            id_prod = input("ID a actualizar: ")
            try:
                nueva_cantidad = input("Nueva cantidad (vacío si no cambia): ")
                nuevo_precio = input("Nuevo precio (vacío si no cambia): ")
                nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else None
                nuevo_precio = float(nuevo_precio) if nuevo_precio else None
            except ValueError:
                print("❌ Error en los datos ingresados.")
                continue
            inventario.actualizar_producto(id_prod, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    menu()

