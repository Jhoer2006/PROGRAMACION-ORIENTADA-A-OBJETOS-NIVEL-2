"""
Sistema de Gestión de Biblioteca
Este programa modela una biblioteca con libros, usuarios y préstamos.
"""


class Libro:
    """
    Clase que representa un libro en la biblioteca
    """

    def __init__(self, titulo: str, autor: str, isbn: str, ejemplares: int = 1):
        """
        Constructor de la clase Libro

        :param titulo: Título del libro
        :param autor: Autor del libro
        :param isbn: Código ISBN único
        :param ejemplares: Número de copias disponibles (por defecto 1)
        """
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self._ejemplares_disponibles = ejemplares  # Atributo protegido
        self._ejemplares_totales = ejemplares  # Atributo protegido

    @property
    def disponibilidad(self) -> bool:
        """Indica si hay ejemplares disponibles"""
        return self._ejemplares_disponibles > 0

    def prestar(self) -> bool:
        """
        Método para prestar un ejemplar del libro

        :return: True si se pudo prestar, False si no hay ejemplares disponibles
        """
        if self._ejemplares_disponibles > 0:
            self._ejemplares_disponibles -= 1
            return True
        return False

    def devolver(self) -> None:
        """Método para devolver un ejemplar del libro"""
        if self._ejemplares_disponibles < self._ejemplares_totales:
            self._ejemplares_disponibles += 1
        else:
            print("¡Error! No puede haber más ejemplares disponibles que los totales.")

    def __str__(self) -> str:
        """Representación en string del libro"""
        return f"'{self.titulo}' por {self.autor} (ISBN: {self.isbn}) - Disponibles: {self._ejemplares_disponibles}/{self._ejemplares_totales}"


class Usuario:
    """
    Clase que representa un usuario de la biblioteca
    """

    def __init__(self, nombre: str, id_usuario: str):
        """
        Constructor de la clase Usuario

        :param nombre: Nombre completo del usuario
        :param id_usuario: Identificador único del usuario
        """
        self.nombre = nombre
        self.id_usuario = id_usuario
        self._libros_prestados = []  # Lista protegida de libros prestados

    def tomar_prestado(self, libro: Libro) -> bool:
        """
        Método para que el usuario tome prestado un libro

        :param libro: Libro a prestar
        :return: True si el préstamo fue exitoso, False en caso contrario
        """
        if libro.prestar():
            self._libros_prestados.append(libro)
            print(f"'{libro.titulo}' prestado con éxito a {self.nombre}.")
            return True
        else:
            print(f"No hay ejemplares disponibles de '{libro.titulo}'.")
            return False

    def devolver_libro(self, libro: Libro) -> None:
        """
        Método para que el usuario devuelva un libro

        :param libro: Libro a devolver
        """
        if libro in self._libros_prestados:
            libro.devolver()
            self._libros_prestados.remove(libro)
            print(f"'{libro.titulo}' devuelto con éxito por {self.nombre}.")
        else:
            print(f"Error: {self.nombre} no tiene prestado '{libro.titulo}'.")

    def mostrar_libros_prestados(self) -> None:
        """Muestra los libros que el usuario tiene prestados"""
        if not self._libros_prestados:
            print(f"{self.nombre} no tiene libros prestados.")
        else:
            print(f"Libros prestados a {self.nombre}:")
            for libro in self._libros_prestados:
                print(f"- {libro.titulo}")

    def __str__(self) -> str:
        """Representación en string del usuario"""
        return f"Usuario: {self.nombre} (ID: {self.id_usuario})"


class Estudiante(Usuario):
    """
    Clase que representa un estudiante, hereda de Usuario
    """

    def __init__(self, nombre: str, id_usuario: str, carrera: str):
        """
        Constructor de la clase Estudiante

        :param carrera: Carrera que estudia el estudiante
        """
        super().__init__(nombre, id_usuario)
        self.carrera = carrera
        self._limite_prestamos = 3  # Límite específico para estudiantes

    @property
    def puede_tomar_prestado(self) -> bool:
        """Indica si el estudiante puede tomar más libros prestados"""
        return len(self._libros_prestados) < self._limite_prestamos

    def tomar_prestado(self, libro: Libro) -> bool:
        """
        Sobreescribe el método para incluir el límite de préstamos

        :param libro: Libro a prestar
        :return: True si el préstamo fue exitoso, False en caso contrario
        """
        if not self.puede_tomar_prestado:
            print(f"{self.nombre} ha alcanzado el límite de {self._limite_prestamos} préstamos.")
            return False
        return super().tomar_prestado(libro)

    def __str__(self) -> str:
        """Representación en string del estudiante"""
        return f"Estudiante: {self.nombre} (ID: {self.id_usuario}), Carrera: {self.carrera}"


class Profesor(Usuario):
    """
    Clase que representa un profesor, hereda de Usuario
    """

    def __init__(self, nombre: str, id_usuario: str, departamento: str):
        """
        Constructor de la clase Profesor

        :param departamento: Departamento al que pertenece el profesor
        """
        super().__init__(nombre, id_usuario)
        self.departamento = departamento
        self._limite_prestamos = 5  # Límite específico para profesores

    @property
    def puede_tomar_prestado(self) -> bool:
        """Indica si el profesor puede tomar más libros prestados"""
        return len(self._libros_prestados) < self._limite_prestamos

    def tomar_prestado(self, libro: Libro) -> bool:
        """
        Sobreescribe el método para incluir el límite de préstamos

        :param libro: Libro a prestar
        :return: True si el préstamo fue exitoso, False en caso contrario
        """
        if not self.puede_tomar_prestado:
            print(f"{self.nombre} ha alcanzado el límite de {self._limite_prestamos} préstamos.")
            return False
        return super().tomar_prestado(libro)

    def __str__(self) -> str:
        """Representación en string del profesor"""
        return f"Profesor: {self.nombre} (ID: {self.id_usuario}), Departamento: {self.departamento}"


class Biblioteca:
    """
    Clase que representa la biblioteca y gestiona los préstamos
    """

    def __init__(self):
        """Constructor de la clase Biblioteca"""
        self.catalogo = []
        self.usuarios = []

    def agregar_libro(self, libro: Libro) -> None:
        """Agrega un libro al catálogo de la biblioteca"""
        self.catalogo.append(libro)
        print(f"Libro agregado al catálogo: {libro.titulo}")

    def registrar_usuario(self, usuario: Usuario) -> None:
        """Registra un usuario en la biblioteca"""
        self.usuarios.append(usuario)
        print(f"Usuario registrado: {usuario.nombre}")

    def buscar_libro(self, titulo: str = None, autor: str = None, isbn: str = None) -> list:
        """
        Busca libros en el catálogo por título, autor o ISBN

        :return: Lista de libros que coinciden con los criterios
        """
        resultados = []
        for libro in self.catalogo:
            if (titulo and titulo.lower() in libro.titulo.lower()) or \
                    (autor and autor.lower() in libro.autor.lower()) or \
                    (isbn and isbn == libro.isbn):
                resultados.append(libro)
        return resultados

    def mostrar_catalogo(self) -> None:
        """Muestra todos los libros en el catálogo"""
        print("\nCatálogo de la Biblioteca:")
        for libro in self.catalogo:
            print(libro)
        print()

    def mostrar_usuarios(self) -> None:
        """Muestra todos los usuarios registrados"""
        print("\nUsuarios registrados:")
        for usuario in self.usuarios:
            print(usuario)
        print()


# Ejemplo de uso del sistema de biblioteca
if __name__ == "__main__":
    # Crear una instancia de biblioteca
    biblioteca = Biblioteca()

    # Agregar algunos libros al catálogo
    libro1 = Libro("Python Crash Course", "Eric Matthes", "978-1593279288", 3)
    libro2 = Libro("Clean Code", "Robert C. Martin", "978-0132350884", 2)
    libro3 = Libro("Design Patterns", "Erich Gamma", "978-0201633610", 1)

    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)

    # Registrar algunos usuarios
    estudiante = Estudiante("María López", "S1001", "Ingeniería Informática")
    profesor = Profesor("Dr. Carlos Ruiz", "P2001", "Ciencias de la Computación")

    biblioteca.registrar_usuario(estudiante)
    biblioteca.registrar_usuario(profesor)

    # Mostrar el catálogo y usuarios
    biblioteca.mostrar_catalogo()
    biblioteca.mostrar_usuarios()

    # Realizar algunos préstamos
    print("\n=== Realizando préstamos ===")
    estudiante.tomar_prestado(libro1)  # María toma Python Crash Course
    profesor.tomar_prestado(libro1)  # Dr. Ruiz toma Python Crash Course
    profesor.tomar_prestado(libro2)  # Dr. Ruiz toma Clean Code
    profesor.tomar_prestado(libro3)  # Dr. Ruiz toma Design Patterns

    # Intentar exceder el límite de préstamos
    estudiante.tomar_prestado(libro2)  # María intenta tomar otro libro
    estudiante.tomar_prestado(libro3)  # María intenta tomar otro libro

    # Mostrar libros prestados
    print("\n=== Libros prestados ===")
    estudiante.mostrar_libros_prestados()
    profesor.mostrar_libros_prestados()

    # Devolver algunos libros
    print("\n=== Devolviendo libros ===")
    estudiante.devolver_libro(libro1)
    profesor.devolver_libro(libro3)

    # Mostrar estado final
    print("\n=== Estado final ===")
    biblioteca.mostrar_catalogo()
    estudiante.mostrar_libros_prestados()
    profesor.mostrar_libros_prestados()