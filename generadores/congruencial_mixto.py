def mostrar_formula():
    print("=== MÉTODO CONGRUENCIAL MIXTO ===")
    print("Fórmula: xᵢ₊₁ = (a * xᵢ + b) mod m\n")


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


def congruencial_mixto(x0: int, a: int, b: int, m: int, cantidad: int):
    resultados = []
    xi = x0

    for i in range(cantidad):
        ui = round(xi / m, 4)
        resultados.append({
            'i': i,
            'x_i': xi,
            'u_i': ui
        })
        xi = (a * xi + b) % m

    return resultados


def mostrar_resultados(resultados):
    print("\n📊 Resultados del método Congruencial Mixto:")
    print("-" * 40)
    print(f"{'i':<5} {'x_i':<10} {'u_i':<10}")
    print("-" * 40)
    for r in resultados:
        print(f"{r['i']:<5} {r['x_i']:<10} {r['u_i']:<10}")


def run_congruencial_mixto():
    mostrar_formula()
    print("🔸 x₀: Semilla inicial (entero positivo)")
    x0 = pedir_entero("x₀", lambda x: x >= 0)

    print("\n🔸 a: Multiplicador (entero positivo)")
    a = pedir_entero("a", lambda x: x > 0)

    print("\n🔸 b: Constante aditiva (entero positivo)")
    b = pedir_entero("b", lambda x: x >= 0)

    print("\n🔸 m: Módulo (entero positivo)")
    m = pedir_entero("m", lambda x: x > 0)

    print("\n🔸 cantidad: Total de números a generar (mínimo 1)")
    cantidad = pedir_entero("cantidad", lambda x: x > 0)

    resultados = congruencial_mixto(x0, a, b, m, cantidad)
    mostrar_resultados(resultados)
    return resultados, [r["u_i"] for r in resultados]


if __name__ == "__main__":
    run_congruencial_mixto()
