# Ejemplo de clases con constructores y destructores en Python

class Logger:
    """
    Clase que gestiona la escritura en un archivo de log.
    El constructor abre el archivo y el destructor lo cierra.
    """
    def __init__(self, filename):
        """
        Constructor (__init__): se llama automáticamente cuando
        se crea un objeto de la clase.
        Aquí inicializamos los atributos y abrimos el archivo.
        """
        self.filename = filename
        self.file = open(self.filename, 'a')  # Abrimos en modo agregar
        print(f"Logger creado. Archivo '{self.filename}' abierto.")

    def log(self, message):
        """Método para escribir un mensaje en el archivo de log."""
        self.file.write(message + '\n')
        print(f"Mensaje logueado: {message}")

    def __del__(self):
        """
        Destructor (__del__): se llama automáticamente cuando
        el objeto es destruido (por ejemplo, cuando se sale del alcance
        o se llama a del objeto explícitamente).
        Aquí cerramos el archivo para liberar el recurso.
        """
        if self.file:
            self.file.close()
            print(f"Logger destruido. Archivo '{self.filename}' cerrado.")


# Otra clase para demostrar que no siempre el destructor gestiona archivos
class Persona:
    """
    Clase que representa una persona.
    Solo imprime mensajes en la creación y destrucción.
    """
    def __init__(self, nombre, edad):
        """
        Constructor: inicializa los atributos nombre y edad.
        """
        self.nombre = nombre
        self.edad = edad
        print(f"Persona creada: {self.nombre}, {self.edad} años.")

    def __del__(self):
        """
        Destructor: imprime un mensaje cuando el objeto Persona es destruido.
        """
        print(f"Persona destruida: {self.nombre}.")


# Programa principal
if __name__ == "__main__":
    # Crear un objeto Logger y escribir en el log
    logger = Logger("mi_log.txt")
    logger.log("Este es el primer mensaje.")
    logger.log("Este es el segundo mensaje.")

    # Crear un objeto Persona
    persona = Persona("Alice", 30)

    # Aquí los objetos siguen existiendo hasta que salgan del alcance
    print("Fin del programa. Los destructores se llamarán automáticamente.")
