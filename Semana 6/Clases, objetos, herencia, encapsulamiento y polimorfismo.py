# Clase base: Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.__velocidad = 0  # Encapsulado

    def acelerar(self):
        self.__velocidad += 10
        return f"{self.marca} {self.modelo} ahora va a {self.__velocidad} km/h."

    def obtener_velocidad(self):
        return self.__velocidad

    def descripcion(self):
        return f"{self.marca} {self.modelo}"

# Clase derivada: Auto
class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)
        self.puertas = puertas

    def acelerar(self):
        return f"El auto {self.marca} acelera suavemente. {super().acelerar()}"

    def descripcion(self):
        return f"Auto: {self.marca} {self.modelo} con {self.puertas} puertas"

# Clase derivada: Moto
class Moto(Vehiculo):
    def __init__(self, marca, modelo, tipo_moto):
        super().__init__(marca, modelo)
        self.tipo_moto = tipo_moto

    def acelerar(self):
        return f"La moto {self.marca} ruge fuerte. {super().acelerar()}"

    def descripcion(self):
        return f"Moto: {self.marca} {self.modelo} tipo {self.tipo_moto}"

# Instancias
camion = Vehiculo("Volvo", "FH16")
auto = Auto("Toyota", "Corolla", 4)
moto = Moto("Yamaha", "FZ", "Deportiva")

# Mostrar resultados
print("--- DEMO DE VEHÍCULOS ---\n")

print(f"Camión: {camion.descripcion()}")
print(camion.acelerar())
print()

print(auto.descripcion())
print(auto.acelerar())
print(auto.acelerar())
print(f"Velocidad actual del auto: {auto.obtener_velocidad()} km/h\n")

print(moto.descripcion())
print(moto.acelerar())
print(f"Velocidad actual de la moto: {moto.obtener_velocidad()} km/h")
