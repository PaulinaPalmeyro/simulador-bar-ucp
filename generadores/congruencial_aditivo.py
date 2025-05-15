def mostrar_formula():
    print("=== MÉTODO CONGRUENCIAL ADITIVO ===")
    print("Fórmula: x_i = (x_{i-n} + x_{i-1}) mod m\n")


def pedir_semillas():
    semillas = []
    print("🔸 Cargar semillas iniciales:")
    print("   (Se necesitan al menos 2. Ingrese una por una.)")
    while True:
        try:
            valor = int(input(f"Ingrese semilla #{len(semillas) + 1} (entero positivo): "))
            if valor < 0:
                print("❌ La semilla debe ser positiva.")
                continue
            semillas.append(valor)
            if len(semillas) >= 2:
                continuar = input("¿Desea ingresar otra semilla? (s/n): ").lower()
                if continuar != 's':
                    break
        except ValueError:
            print("❌ Solo se permiten números enteros.")
    return semillas


def pedir_modulo(_):
    while True:
        print("\n🔸 Ingrese el módulo (m):")
        print("   Debe ser un número entero positivo.")
        try:
            m = int(input("Módulo m: "))
            if m <= 0:
                print("❌ El módulo debe ser mayor a 0.")
                continue
            return m
        except ValueError:
            print("❌ Solo se permiten números enteros.")


def pedir_cantidad(minima):
    while True:
        print("\n🔸 Ingrese la cantidad total de números a generar:")
        print(f"   Debe ser mayor que la cantidad de semillas ({minima}).")
        try:
            c = int(input("Cantidad total: "))
            if c <= minima:
                print("❌ Debe generar más números que la cantidad de semillas.")
                continue
            return c
        except ValueError:
            print("❌ Solo se permiten números enteros.")


def congruencial_aditivo(semillas: list[int], m: int, cantidad: int):
    resultados = []
    secuencia = semillas.copy()
    n = len(semillas)

    for i in range(cantidad):
        if i < n:
            x = secuencia[i]
        else:
            x = (secuencia[i - n] + secuencia[i - 1]) % m
            secuencia.append(x)

        u = round(x / m, 4)
        resultados.append({'i': i, 'x_i': x, 'u_i': u})

    return resultados


def mostrar_resultados(resultados):
    print("\n📊 Resultados del método Congruencial Aditivo:")
    print("-" * 40)
    print(f"{'i':<5} {'x_i':<10} {'u_i':<10}")
    print("-" * 40)
    for r in resultados:
        print(f"{r['i']:<5} {r['x_i']:<10} {r['u_i']:<10}")


# ESTA FUNCIÓN NUEVA ES LA QUE DEBES USAR EN EL MENÚ PRINCIPAL
def run_congruencial_aditivo():
    mostrar_formula()
    semillas = pedir_semillas()
    m = pedir_modulo(semillas)
    cantidad = pedir_cantidad(len(semillas))
    resultados = congruencial_aditivo(semillas, m, cantidad)
    mostrar_resultados(resultados)
    return resultados, [r["u_i"] for r in resultados]


if __name__ == "__main__":
    run_congruencial_aditivo()
