class Vehiculo:
    def __init__(self, marca):
        self.marca = marca

    def arrancar(self):
        print(f"{self.marca} está arrancando...")


def tocar_bocina():
    print("¡Beep beep!")


class Auto(Vehiculo):
    pass

# Uso
mi_auto = Auto("Toyota")
mi_auto.arrancar()
tocar_bocina()
