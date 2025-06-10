

class ClimaSemanal:
    """
    Clase para representar la información del clima diario y calcular el promedio semanal.
    Encapsula las temperaturas de la semana.
    """

    def __init__(self):
        """
        Constructor de la clase. Inicializa la lista de temperaturas vacía.
        """
        self.__temperaturas = []  # Atributo privado para encapsular las temperaturas
        self.__dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    def ingresar_temperaturas(self):
        """
        Solicita al usuario las temperaturas diarias y las almacena en el objeto.
        """
        self.__temperaturas = []  # Asegura que la lista esté vacía antes de ingresar nuevas temperaturas
        print("Por favor, ingresa las temperaturas diarias de la semana:")
        for i in range(7):
            while True:
                try:
                    temp = float(input(f"Temperatura del {self.__dias[i]}: "))
                    self.__temperaturas.append(temp)
                    break
                except ValueError:
                    print("Entrada inválida. Por favor, ingresa un número para la temperatura.")

    def calcular_promedio(self):
        """
        Calcula el promedio de las temperaturas almacenadas en el objeto.
        Returns:
            float: El promedio de las temperaturas.
        """
        if not self.__temperaturas:
            print("No hay temperaturas ingresadas para calcular el promedio.")
            return 0.0

        suma_temperaturas = sum(self.__temperaturas)
        promedio = suma_temperaturas / len(self.__temperaturas)
        return promedio

    def obtener_temperaturas(self):
        """
        Retorna la lista de temperaturas almacenadas.
        Esto es un 'getter' para acceder al atributo privado.
        """
        return self.__temperaturas


# --- Programa Principal (POO) ---
if __name__ == "__main__":
    print("--- Calculador de Promedio Semanal de Temperaturas (Programación Orientada a Objetos) ---")

    # 1. Crear una instancia de la clase ClimaSemanal
    clima_semana = ClimaSemanal()

    # 2. Ingresar las temperaturas usando un método de la instancia
    clima_semana.ingresar_temperaturas()

    # 3. Calcular el promedio usando un método de la instancia
    promedio_final = clima_semana.calcular_promedio()

    # 4. Mostrar el resultado
    print(f"\nLas temperaturas ingresadas fueron: {clima_semana.obtener_temperaturas()}")
    print(f"El promedio semanal de temperaturas es: {promedio_final:.2f}°C")

#Programación Orientada a Objetos (POO) modela el problema de manera más cercana al mundo real. Se crean clases para
    # representar los días y la semana, encapsulando la temperatura como un atributo. Esto facilita la reutilización de
    # código y mejora la organización.