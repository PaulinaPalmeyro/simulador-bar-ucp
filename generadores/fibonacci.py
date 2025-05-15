def mostrar_formula():
    print("=== MÉTODO DE FIBONACCI ===")
    print("Fórmula: xₙ = (xₙ₋₁ + xₙ₋₂) mod m\n")


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


def fibonacci(seed1: int, seed2: int, m: int, cantidad: int):
    resultados = []
    x_prev2 = seed1
    x_prev1 = seed2

    for n in range(cantidad):
        if n == 0:
            x = x_prev2
        elif n == 1:
            x = x_prev1
        else:
            x = (x_prev1 + x_prev2) % m
            x_prev2, x_prev1 = x_prev1, x

        u = round(x / m, 4)
        resultados.append({
            'n': n,
            'x_n': x,
            'u_n': u
        })

    return resultados


def mostrar_resultados(resultados):
    print("\n📊 Resultados del método de Fibonacci:")
    print("-" * 40)
    print(f"{'n':<5} {'x_n':<10} {'u_n':<10}")
    print("-" * 40)

    for r in resultados:
        print(f"{r['n']:<5} {r['x_n']:<10} {r['u_n']:<10}")


def run_fibonacci():
    mostrar_formula()

    print("🔸 x₀: Primera semilla (entero positivo)")
    x0 = pedir_entero("x₀", lambda x: x >= 0)

    print("\n🔸 x₁: Segunda semilla (entero positivo)")
    x1 = pedir_entero("x₁", lambda x: x >= 0)

    print("\n🔸 m: Módulo (entero positivo)")
    m = pedir_entero("m", lambda x: x > 0)

    print("\n🔸 cantidad: Total de números a generar (mínimo 1)")
    cantidad = pedir_entero("cantidad", lambda x: x > 0)

    resultados = fibonacci(x0, x1, m, cantidad)
    mostrar_resultados(resultados)
    return resultados, [r["u_n"] for r in resultados]


if __name__ == "__main__":
    run_fibonacci()
