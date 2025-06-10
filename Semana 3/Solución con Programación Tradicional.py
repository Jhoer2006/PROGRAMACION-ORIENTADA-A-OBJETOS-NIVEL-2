

def obtener_temperaturas_diarias():
    """
    Solicita al usuario las temperaturas diarias de la semana.
    Retorna una lista con las 7 temperaturas.
    """
    temperaturas = []
    print("Por favor, ingresa las temperaturas diarias de la semana:")
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    for i in range(7):
        while True:
            try:
                temp = float(input(f"Temperatura del {dias[i]}: "))
                temperaturas.append(temp)
                break # Sale del bucle si la entrada es válida
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número para la temperatura.")
    return temperaturas

def calcular_promedio_semanal(temperaturas):
    """
    Calcula el promedio de una lista de temperaturas.
    Args:
        temperaturas (list): Una lista de números que representan las temperaturas.
    Returns:
        float: El promedio de las temperaturas.
    """
    if not temperaturas:
        return 0.0 # Retorna 0.0 si la lista está vacía para evitar división por cero
    suma_temperaturas = sum(temperaturas)
    promedio = suma_temperaturas / len(temperaturas)
    return promedio

# --- Programa Principal (Tradicional) ---
if __name__ == "__main__":
    print("--- Calculador de Promedio Semanal de Temperaturas (Programación Tradicional) ---")

    # 1. Obtener las temperaturas
    temps_semana = obtener_temperaturas_diarias()

    # 2. Calcular el promedio
    promedio_final = calcular_promedio_semanal(temps_semana)

    # 3. Mostrar el resultado
    print(f"\nLas temperaturas ingresadas fueron: {temps_semana}")
    print(f"El promedio semanal de temperaturas es: {promedio_final:.2f}°C") # Formato a 2 decimales

    #programación tradicional, el programa está estructurado en funciones independientes,
    # lo que facilita su lectura y ejecución lineal. Sin embargo,
    # no agrupa la información ni los comportamientos en entidades lógicas.