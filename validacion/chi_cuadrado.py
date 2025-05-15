from collections import Counter
from scipy.stats import chi2

def chi_cuadrado(ui: list[float], k: int = 10, alpha: float = 0.05):
    n = len(ui)
    fe = n / k
    intervalos = [0] * k

    for u in ui:
        index = min(int(u * k), k - 1)
        intervalos[index] += 1

    chi_cuadrado_valor = sum(((fo - fe) ** 2) / fe for fo in intervalos)
    chi_critico = chi2.ppf(1 - alpha, df=k - 1)

    max_desviacion = 0
    intervalo_max_desviacion = 0
    for i, fo in enumerate(intervalos):
        desviacion = abs(fo - fe)
        if desviacion > max_desviacion:
            max_desviacion = desviacion
            intervalo_max_desviacion = i

    return {
        "estadistico": round(chi_cuadrado_valor, 4),
        "critico": round(chi_critico, 4),
        "frecuencia_esperada": fe,
        "frecuencias_observadas": intervalos,
        "pasa": chi_cuadrado_valor < chi_critico,
        "k": k,
        "n": n,
        "max_desviacion": max_desviacion,
        "intervalo_max_desviacion": intervalo_max_desviacion,
        "cumple_criterio_nk": (n / k) >= 5
    }

def mostrar_resultado(resultado):
    print("\n===== ANÁLISIS DEL TEST CHI-CUADRADO =====")

    print("\n📌 Datos del test:")
    print("Este test evalúa si una secuencia de números entre 0 y 1 está distribuida de manera uniforme.")
    print("Para ello, dividimos el intervalo [0, 1] en partes iguales (intervalos) y contamos cuántos números caen en cada uno.")
    print("Si todos los intervalos tienen cantidades similares, podemos decir que la secuencia es uniforme.")
    print(f"- Total de números analizados: {resultado['n']}")
    print(f"- Cantidad de intervalos (k): {resultado['k']}")
    print(f"- Frecuencia esperada por intervalo: {resultado['frecuencia_esperada']:.2f} (calculado como n/k)")

    print("\n📊 ¿Qué es una frecuencia?")
    print("La frecuencia es la cantidad de veces que un valor aparece o cae en cierto rango.\n")
    print("\n• Frecuencia esperada:")
    print("  Es la cantidad de valores que *deberían* caer en cada intervalo si la distribución fuera perfectamente uniforme.")
    print("  En este caso, todos los intervalos deberían tener aproximadamente la misma cantidad de números.")

    print("\n• Frecuencia observada:")
    print("  Es la cantidad de valores que *realmente* cayeron en cada intervalo al analizar la secuencia generada.")

    print("\n📊 Distribución observada por intervalos:")
    print("Cada intervalo es una división del rango [0, 1].")
    for i in range(resultado['k']):
        inicio = i / resultado['k']
        fin = (i + 1) / resultado['k']
        fo = resultado['frecuencias_observadas'][i]
        print(f"  • Intervalo {i+1} [{inicio:.2f}-{fin:.2f}]: {fo} valores observados")

    print("\n📈 Análisis del ajuste:")
    print(f"- Estadístico calculado: {resultado['estadistico']}")
    print("  Este valor representa la suma de todas las diferencias entre lo observado y lo esperado.")
    print("  Cuanto menor sea, más parecida es la secuencia a una distribución uniforme.")
    print(f"- Valor crítico (α = 0.05, gl = {resultado['k'] - 1}): {resultado['critico']}")

    print("\n✅ Conclusión:")
    if not resultado['cumple_criterio_nk']:
        print("El número de datos es bajo en relación con los intervalos elegidos. El test puede no ser confiable. Aumentar la cantidad de números generados para obtener mejores resultados.")
    else:
        if resultado['pasa']:
            print(f"✅ La secuencia PASA el test de Chi-cuadrado.\nEl estadístico calculado ({resultado['estadistico']}) es menor que el valor crítico ({resultado['critico']}).\nEsto indica que las diferencias entre las frecuencias observadas y esperadas no son significativas. La secuencia puede considerarse uniforme.")
        else:
            print(f"❌ La secuencia NO pasa el test de Chi-cuadrado.\nEl estadístico calculado ({resultado['estadistico']}) es mayor que el valor crítico ({resultado['critico']}).\nEsto indica que hay demasiada diferencia entre lo observado y lo esperado.\nLa mayor desviación fue en el intervalo {resultado['intervalo_max_desviacion'] + 1}, con una diferencia de {resultado['max_desviacion']:.2f} valores. Se recomienda generar una nueva secuencia.")
