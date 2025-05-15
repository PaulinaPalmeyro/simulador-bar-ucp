def mostrar_formula():
    print("=== MÉTODO DE CUADRADOS MEDIOS ===")
    print("Fórmula: xₙ = parte media de (xₙ₋₁)²\n")


def pedir_entero(nombre: str, restriccion=None):
    while True:
        try:
            valor = int(input(f"Ingrese {nombre}: "))
            if restriccion and not restriccion(valor):
                print("❌ Valor no válido.")
                continue
            return valor
        except ValueError:
            print("❌ Solo se permiten números enteros.")


def calcular_medio(numero: int, digitos: int) -> str:
    numero_str = str(numero)
    sobra = len(numero_str) - digitos

    if sobra % 2 != 0:
        numero_str = "0" + numero_str
        sobra += 1

    inicio = sobra // 2
    medio = numero_str[inicio:inicio + digitos]
    return medio


def cuadrados_medios(seed: int, digitos: int, cantidad: int):
    resultados = []
    actual = seed

    for n in range(1, cantidad + 1):
        cuadrado = actual ** 2
        medio = calcular_medio(cuadrado, digitos)

        try:
            nuevo = int(medio)
        except ValueError:
            print(f"Error al convertir '{medio}' en entero.")
            break

        u = nuevo / (10 ** digitos)

        resultados.append({
            'n': n,
            'R(n)': actual,
            'R(n)²': cuadrado,
            'M.R(n)²': medio,
            'U(n)': round(u, 4)
        })

        actual = nuevo
        if nuevo == 0:
            print("La semilla se volvió 0. El proceso termina.")
            break

    return resultados


def mostrar_resultados(resultados):
    print("\n📊 Resultados del método de Cuadrados Medios:")
    print("-" * 70)
    print(f"{'n':<5} {'R(n)':<10} {'R(n)²':<15} {'M.R(n)²':<10} {'U(n)':<10}")
    print("-" * 70)

    for r in resultados:
        print(f"{r['n']:<5} {r['R(n)']:<10} {r['R(n)²']:<15} {r['M.R(n)²']:<10} {r['U(n)']:<10}")


def run_cuadrados_medios():
    mostrar_formula()

    print("🔸 Semilla inicial (entero ≥ 100)")
    semilla = pedir_entero("semilla", lambda x: x >= 100)

    print("\n🔸 Cantidad de dígitos significativos a extraer (ej: 4)")
    digitos = pedir_entero("dígitos", lambda x: x > 0)

    print("\n🔸 Cantidad total de números a generar (mínimo 1)")
    cantidad = pedir_entero("cantidad", lambda x: x > 0)

    resultados = cuadrados_medios(semilla, digitos, cantidad)
    mostrar_resultados(resultados)
    ui = [r["U(n)"] for r in resultados]
    return resultados, ui


if __name__ == "__main__":
    run_cuadrados_medios()
