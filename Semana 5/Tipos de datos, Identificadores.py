# Este prográma se usa para registrar y mostrar información básica de una persona.
# Utiliza distintos tipos de datos como: string, int, float, bool.
# Aplica buenas prácticas de nombres e incluye comentarios para comprensión.

def mostrar_registro(nombre: str, edad: int, altura: float, inscrito: bool):
    """Muestra en pantalla los datos de una persona registrados."""
    print("\n--- Registro de Persona ---")
    print(f"Nombre      : {nombre}")
    print(f"Edad        : {edad} años")
    print(f"Altura      : {altura} m")
    print(f"Inscrito    : {'Sí' if inscrito else 'No'}")


# Solicitar datos al usuario
nombre_persona = input("Ingresa el nombre de la persona: ")
edad_persona = int(input("Ingresa la edad: "))
altura_persona = float(input("Ingresa la altura en metros: "))

# Entrada para booleano: se transforma a minúsculas y se interpreta
respuesta_inscripcion = input("¿Está inscrito? (sí/no): ").lower()
esta_inscrito = respuesta_inscripcion == "sí"

# Llamar a la función para mostrar los datos
mostrar_registro(nombre_persona, edad_persona, altura_persona, esta_inscrito)
