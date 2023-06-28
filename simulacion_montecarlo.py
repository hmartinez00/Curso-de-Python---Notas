import random

def lanzamiento_dado():
    return random.randint(1, 6)  # Genera un número aleatorio entre 1 y 6 simulando un lanzamiento de dado

def simulacion_montecarlo(num_lanzamientos):
    conteo_objetivo = 0  # Contador para el número de veces que se obtiene el número objetivo
    objetivo = 5  # Número objetivo a obtener
    
    for _ in range(num_lanzamientos):
        resultado = lanzamiento_dado()
        if resultado == objetivo:
            conteo_objetivo += 1
    
    probabilidad = conteo_objetivo / num_lanzamientos
    return probabilidad

# Ejemplo de uso
num_lanzamientos = 10000
probabilidad = simulacion_montecarlo(num_lanzamientos)
print(f"La probabilidad estimada de obtener el número 5 en un lanzamiento de dado es: {probabilidad}")
