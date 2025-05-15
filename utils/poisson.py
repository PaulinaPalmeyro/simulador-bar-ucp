import math

def generar_poisson(lambd: float, ui: list[float], cantidad: int) -> list[int]:
    """
    Genera 'cantidad' valores con distribución de Poisson usando el algoritmo de Knuth.

    :param lambd: Valor de λ (media esperada de eventos por intervalo)
    :param ui: Lista de números pseudoaleatorios (valores entre 0 y 1)
    :param cantidad: Cuántos valores Poisson generar
    :return: Lista de números enteros distribuidos Poisson
    """
    resultados = []
    index = 0
    for _ in range(cantidad):
        L = math.exp(-lambd)
        p = 1
        k = 0
        while p > L:
            if index >= len(ui):
                raise ValueError("No hay suficientes valores pseudoaleatorios.")
            p *= ui[index]
            index += 1
            k += 1
        resultados.append(k - 1)
    return resultados
