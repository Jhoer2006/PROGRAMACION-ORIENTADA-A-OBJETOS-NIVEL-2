class Ave:
    def volar(self):
        print("Esta ave vuela.")

class Pinguino(Ave):
    def volar(self):
        print("El pingüino no puede volar.")

class Aguila(Ave):
    def volar(self):
        print("El águila si puede volar")

# Uso
aves = [Pinguino(), Aguila()]
for ave in aves:
    ave.volar()
