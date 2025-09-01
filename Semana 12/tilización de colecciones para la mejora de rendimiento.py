"""
Biblioteca Digital - Sistema de Gestión
- Archivo: biblioteca_digital.py
- Funcionalidades:
  - Añadir / quitar libros
  - Registrar / dar de baja usuarios
  - Prestar / devolver libros
  - Buscar libros por título, autor o categoría
  - Listar libros prestados por usuario
- Estructuras utilizadas:
  - Tuplas para atributos inmutables del libro (título, autor)
  - Listas para los libros prestados por usuario
  - Diccionarios para catálogo de libros por ISBN
  - Conjuntos para IDs de usuarios únicos
- Persistencia:
  - Guarda y carga en archivo JSON 'biblioteca.json' (manejo de excepciones incluido)
"""

import json
import os
from datetime import datetime

# -------------------------
# Clase Libro
# -------------------------
class Libro:
    """
    Representa un libro.
    - info: tupla (titulo, autor) -> inmutable
    - categoria: cadena (mutable)
    - isbn: identificador único (string)
    """
    def __init__(self, titulo, autor, categoria, isbn):
        # Guardamos título y autor en una tupla para inmutabilidad
        self.info = (str(titulo), str(autor))
        self.categoria = str(categoria)
        self.isbn = str(isbn)

    # Getters (no setters para título/autor porque son inmutables)
    def get_titulo(self):
        return self.info[0]

    def get_autor(self):
        return self.info[1]

    def get_categoria(self):
        return self.categoria

    def get_isbn(self):
        return self.isbn

    # Setter sólo para categoría (si queremos reclasificar un libro)
    def set_categoria(self, nueva_cat):
        self.categoria = str(nueva_cat)

    # Serialización
    def to_dict(self):
        return {
            "titulo": self.get_titulo(),
            "autor": self.get_autor(),
            "categoria": self.categoria,
            "isbn": self.isbn
        }

    @staticmethod
    def from_dict(d):
        return Libro(d["titulo"], d["autor"], d["categoria"], d["isbn"])

    def __str__(self):
        return f"[ISBN: {self.isbn}] \"{self.get_titulo()}\" - {self.get_autor()} | Categoría: {self.categoria}"


# -------------------------
# Clase Usuario
# -------------------------
class Usuario:
    """
    Representa un usuario de la biblioteca.
    - nombre: string
    - user_id: identificador único (string)
    - prestados: lista de ISBNs de libros actualmente prestados
    """
    def __init__(self, nombre, user_id):
        self.nombre = str(nombre)
        self.user_id = str(user_id)
        self.prestados = []  # lista de ISBNs

    def get_nombre(self):
        return self.nombre

    def get_id(self):
        return self.user_id

    def get_prestados(self):
        return list(self.prestados)  # devolver copia

    def prestar_libro(self, isbn):
        if isbn not in self.prestados:
            self.prestados.append(isbn)

    def devolver_libro(self, isbn):
        if isbn in self.prestados:
            self.prestados.remove(isbn)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "user_id": self.user_id,
            "prestados": list(self.prestados)
        }

    @staticmethod
    def from_dict(d):
        u = Usuario(d["nombre"], d["user_id"])
        u.prestados = list(d.get("prestados", []))
        return u

    def __str__(self):
        return f"{self.nombre} (ID: {self.user_id}) - Prestados: {len(self.prestados)}"


# -------------------------
# Clase Biblioteca
# -------------------------
class Biblioteca:
    """
    Gestiona:
    - libros: dict { isbn: Libro }
    - usuarios: dict { user_id: Usuario }
    - user_ids: set -> asegura unicidad de los IDs
    - prestamos: dict { isbn: user_id } -> rápido lookup de a quién está prestado un libro
    """
    def __init__(self, archivo="biblioteca.json"):
        self.libros = {}   # isbn -> Libro
        self.usuarios = {} # user_id -> Usuario
        self.user_ids = set()
        self.prestamos = {} # isbn -> user_id
        self.archivo = archivo
        self._cargar_archivo()

    # ---------- Operaciones de libros ----------
    def añadir_libro(self, libro: Libro):
        isbn = libro.get_isbn()
        if isbn in self.libros:
            print(f"⚠️ Ya existe un libro con ISBN {isbn}.")
            return False
        self.libros[isbn] = libro
        self._guardar_archivo()
        print("✅ Libro añadido:")
        print("  ", libro)
        return True

    def quitar_libro(self, isbn):
        isbn = str(isbn)
        if isbn not in self.libros:
            print("❌ No existe ese ISBN en el catálogo.")
            return False
        if isbn in self.prestamos:
            print("❌ No se puede eliminar: el libro está prestado actualmente.")
            return False
        removed = self.libros.pop(isbn)
        self._guardar_archivo()
        print("🗑️ Libro eliminado:")
        print("  ", removed)
        return True

    # ---------- Operaciones de usuarios ----------
    def registrar_usuario(self, usuario: Usuario):
        uid = usuario.get_id()
        if uid in self.user_ids:
            print("⚠️ Ya existe un usuario con ese ID.")
            return False
        self.usuarios[uid] = usuario
        self.user_ids.add(uid)
        self._guardar_archivo()
        print("✅ Usuario registrado:", usuario)
        return True

    def dar_baja_usuario(self, user_id):
        user_id = str(user_id)
        if user_id not in self.user_ids:
            print("❌ Usuario no encontrado.")
            return False
        # No permitir baja si usuario tiene libros prestados
        if self.usuarios[user_id].prestados:
            print("❌ El usuario tiene libros prestados. Debe devolverlos antes de darse de baja.")
            return False
        del self.usuarios[user_id]
        self.user_ids.remove(user_id)
        self._guardar_archivo()
        print("🗑️ Usuario dado de baja:", user_id)
        return True

    # ---------- Préstamos ----------
    def prestar(self, isbn, user_id):
        isbn = str(isbn); user_id = str(user_id)
        if isbn not in self.libros:
            print("❌ ISBN no encontrado en catálogo.")
            return False
        if user_id not in self.user_ids:
            print("❌ Usuario no registrado.")
            return False
        if isbn in self.prestamos:
            print("❌ El libro ya está prestado a otro usuario.")
            return False
        # Registrar préstamo
        self.prestamos[isbn] = user_id
        self.usuarios[user_id].prestar_libro(isbn)
        self._guardar_archivo()
        print(f"✅ Libro (ISBN {isbn}) prestado a usuario {user_id}.")
        return True

    def devolver(self, isbn, user_id):
        isbn = str(isbn); user_id = str(user_id)
        if isbn not in self.prestamos:
            print("❌ Ese libro no está prestado.")
            return False
        if self.prestamos[isbn] != user_id:
            print("❌ Este libro no está prestado a ese usuario.")
            return False
        # Procesar devolución
        del self.prestamos[isbn]
        self.usuarios[user_id].devolver_libro(isbn)
        self._guardar_archivo()
        print(f"📚 Libro (ISBN {isbn}) devuelto por usuario {user_id}.")
        return True

    # ---------- Búsquedas ----------
    def buscar_por_titulo(self, texto):
        texto = texto.lower()
        resultados = [l for l in self.libros.values() if texto in l.get_titulo().lower()]
        self._imprimir_lista(resultados, "título")

    def buscar_por_autor(self, texto):
        texto = texto.lower()
        resultados = [l for l in self.libros.values() if texto in l.get_autor().lower()]
        self._imprimir_lista(resultados, "autor")

    def buscar_por_categoria(self, categoria):
        categoria = categoria.lower()
        resultados = [l for l in self.libros.values() if categoria == l.get_categoria().lower()]
        self._imprimir_lista(resultados, "categoría")

    def _imprimir_lista(self, lista, criterio=""):
        if not lista:
            print("🔎 No se encontraron resultados.")
            return
        print(f"\n🔎 Resultados por {criterio}:")
        for l in lista:
            estado = "Disponible" if l.get_isbn() not in self.prestamos else f"Prestado a {self.prestamos[l.get_isbn()]}"
            print(" ", l, "|", estado)

    # ---------- Mostrar ----------
    def mostrar_todos(self):
        if not self.libros:
            print("📚 Catálogo vacío.")
            return
        print("\n📚 Catálogo completo:")
        for l in self.libros.values():
            estado = "Disponible" if l.get_isbn() not in self.prestamos else f"Prestado a {self.prestamos[l.get_isbn()]}"
            print(" ", l, "|", estado)

    def listar_prestados_por_usuario(self, user_id):
        user_id = str(user_id)
        if user_id not in self.user_ids:
            print("❌ Usuario no registrado.")
            return
        user = self.usuarios[user_id]
        if not user.prestados:
            print("📭 El usuario no tiene libros prestados.")
            return
        print(f"\n📄 Libros prestados a {user.get_nombre()} (ID: {user_id}):")
        for isbn in user.prestados:
            libro = self.libros.get(isbn)
            if libro:
                print(" ", libro)
            else:
                print("  - ISBN:", isbn, "(no encontrado en catálogo)")

    # ---------- Persistencia en archivo ----------
    def _guardar_archivo(self):
        tmp = self.archivo + ".tmp"
        try:
            data = {
                "libros": {isbn: lib.to_dict() for isbn, lib in self.libros.items()},
                "usuarios": {uid: u.to_dict() for uid, u in self.usuarios.items()},
                "prestamos": dict(self.prestamos)
            }
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self.archivo)
            # Mensaje opcional:
            # print(f"💾 Archivo '{self.archivo}' actualizado.")
            return True
        except PermissionError:
            print("❌ Permiso denegado: no se pudo escribir el archivo de biblioteca.")
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            return False
        except Exception as e:
            print("❌ Error guardando archivo:", e)
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            return False

    def _cargar_archivo(self):
        if not os.path.exists(self.archivo):
            # Crear archivo vacío
            try:
                with open(self.archivo, "w", encoding="utf-8") as f:
                    json.dump({"libros": {}, "usuarios": {}, "prestamos": {}}, f)
                print(f"🆕 Archivo '{self.archivo}' creado (nuevo catálogo vacío).")
            except PermissionError:
                print("❌ Permiso denegado: no se puede crear archivo de biblioteca.")
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Cargar libros
            libros_data = data.get("libros", {})
            for isbn, ld in libros_data.items():
                try:
                    self.libros[isbn] = Libro.from_dict(ld)
                except Exception:
                    continue
            # Cargar usuarios
            usuarios_data = data.get("usuarios", {})
            for uid, ud in usuarios_data.items():
                try:
                    user = Usuario.from_dict(ud)
                    self.usuarios[uid] = user
                    self.user_ids.add(uid)
                except Exception:
                    continue
            # Cargar prestamos
            prestamos_data = data.get("prestamos", {})
            self.prestamos = {str(k): str(v) for k, v in prestamos_data.items()}
            # Asegurar consistencia: que usuarios tengan sus libros en la lista 'prestados'
            for isbn, uid in self.prestamos.items():
                if uid in self.usuarios:
                    if isbn not in self.usuarios[uid].prestados:
                        self.usuarios[uid].prestados.append(isbn)
            print(f"📂 Biblioteca cargada: {len(self.libros)} libros, {len(self.usuarios)} usuarios.")
        except json.JSONDecodeError:
            # Archivo corrupto -> renombrar y crear uno nuevo
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            corrupt_name = f"{self.archivo}.corrupt-{ts}"
            try:
                os.replace(self.archivo, corrupt_name)
                with open(self.archivo, "w", encoding="utf-8") as f:
                    json.dump({"libros": {}, "usuarios": {}, "prestamos": {}}, f)
                print(f"⚠️ Archivo corrupto renombrado a '{corrupt_name}'. Se creó un nuevo archivo vacío.")
            except PermissionError:
                print("❌ Permiso denegado al manejar archivo corrupto.")
        except PermissionError:
            print("❌ Permiso denegado al leer el archivo de biblioteca.")
        except Exception as e:
            print("❌ Error cargando archivo de biblioteca:", e)

# -------------------------
# Interfaz de consola (menú)
# -------------------------
def menu():
    biblioteca = Biblioteca()

    while True:
        print("\n=== BIBLIOTECA DIGITAL ===")
        print("1. Añadir libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libros (título/autor/categoría)")
        print("8. Mostrar todos los libros")
        print("9. Listar libros prestados por usuario")
        print("0. Salir")

        opcion = input("Selecciona opción: ").strip()

        if opcion == "1":
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            categoria = input("Categoría: ").strip()
            isbn = input("ISBN (único): ").strip()
            biblioteca.añadir_libro(Libro(titulo, autor, categoria, isbn))

        elif opcion == "2":
            isbn = input("ISBN a quitar: ").strip()
            biblioteca.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Nombre del usuario: ").strip()
            user_id = input("ID de usuario (único): ").strip()
            biblioteca.registrar_usuario(Usuario(nombre, user_id))

        elif opcion == "4":
            user_id = input("ID de usuario a dar de baja: ").strip()
            biblioteca.dar_baja_usuario(user_id)

        elif opcion == "5":
            isbn = input("ISBN a prestar: ").strip()
            user_id = input("ID del usuario receptor: ").strip()
            biblioteca.prestar(isbn, user_id)

        elif opcion == "6":
            isbn = input("ISBN a devolver: ").strip()
            user_id = input("ID del usuario que devuelve: ").strip()
            biblioteca.devolver(isbn, user_id)

        elif opcion == "7":
            sub = input("Buscar por (t)ítulo, (a)utor o (c)ategoría? ").strip().lower()
            if sub == "t":
                tx = input("Texto de título: ").strip()
                biblioteca.buscar_por_titulo(tx)
            elif sub == "a":
                tx = input("Texto de autor: ").strip()
                biblioteca.buscar_por_autor(tx)
            elif sub == "c":
                tx = input("Categoría (exacta): ").strip()
                biblioteca.buscar_por_categoria(tx)
            else:
                print("❌ Opción inválida de búsqueda.")

        elif opcion == "8":
            biblioteca.mostrar_todos()

        elif opcion == "9":
            user_id = input("ID de usuario: ").strip()
            biblioteca.listar_prestados_por_usuario(user_id)

        elif opcion == "0":
            print("👋 Saliendo. ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida. Intenta de nuevo.")


# -------------------------
# Pruebas automáticas simples (se ejecutan si corres este archivo directamente)
# -------------------------
def pruebas_demo():
    """
    Demo: añade algunos libros y usuarios y simula préstamos.
    Sirve para validar que todas las piezas funcionan.
    """
    print("\n=== DEMO RÁPIDA ===")
    b = Biblioteca(archivo="biblioteca_demo.json")

    # Limpiar demo previo (no borrar archivos reales)
    try:
        if os.path.exists("biblioteca_demo.json"):
            os.remove("biblioteca_demo.json")
    except Exception:
        pass

    b = Biblioteca(archivo="biblioteca_demo.json")
    b.añadir_libro(Libro("Cien años de soledad", "Gabriel García Márquez", "Novela", "ISBN-1001"))
    b.añadir_libro(Libro("El Principito", "Antoine de Saint-Exupéry", "Infantil", "ISBN-1002"))
    b.registrar_usuario(Usuario("María Pérez", "U100"))
    b.registrar_usuario(Usuario("Juan López", "U101"))
    b.prestar("ISBN-1002", "U100")
    b.listar_prestados_por_usuario("U100")
    b.mostrar_todos()
    print("=== FIN DEMO ===\n")


# -------------------------
# Punto de entrada
# -------------------------
if __name__ == "__main__":
    # Si quieres ejecutar la demo al inicio descomenta la línea siguiente:
    # pruebas_demo()
    menu()
