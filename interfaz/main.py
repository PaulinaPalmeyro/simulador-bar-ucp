from generadores.cuadrados_medios import run_cuadrados_medios
from generadores.fibonacci import run_fibonacci
from generadores.congruencial_aditivo import run_congruencial_aditivo
from generadores.congruencial_mixto import run_congruencial_mixto
from generadores.congruencial_multiplicativo import run_congruencial_multiplicativo
from validacion.chi_cuadrado import chi_cuadrado, mostrar_resultado
from simulacion.bar_ucp import simular_bar_ucp

ultima_secuencia_ui = []
ultima_secuencia_valida = False

def validar_secuencia(secuencia):
    global ultima_secuencia_valida
    print("\nRealizando validación automática con Test Chi-cuadrado...")
    resultado = chi_cuadrado(secuencia, k=10)
    mostrar_resultado(resultado)
    ultima_secuencia_valida = resultado['pasa']
    return resultado['pasa']

def menu():
    global ultima_secuencia_ui, ultima_secuencia_valida

    while True:
        print("\n===== SIMULADOR TP2 - Modelos y Simulación =====")
        print("1. Generar números - Cuadrados Medios")
        print("2. Generar números - Fibonacci")
        print("3. Generar números - Congruencial Aditivo")
        print("4. Generar números - Congruencial Mixto")
        print("5. Generar números - Congruencial Multiplicativo")
        print("6. Validar última secuencia con Test Chi-cuadrado")
        print("7. Simular atención en el Bar UCP")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- Método de Cuadrados Medios ---")
            try:
                resultados, ui = run_cuadrados_medios()
                ultima_secuencia_ui = ui
                validar_secuencia(ultima_secuencia_ui)

            except ValueError:
                print("Por favor, ingrese solo números enteros válidos.")

        elif opcion == "2":
            
            try:
                resultados, ui = run_fibonacci()
                ultima_secuencia_ui = ui
                validar_secuencia(ultima_secuencia_ui)

            except ValueError:
                print("Entrada inválida. Ingrese solo números enteros.")

        elif opcion == "3":
            try:
                resultados, ui = run_congruencial_aditivo()
                ultima_secuencia_ui = ui
                validar_secuencia(ultima_secuencia_ui)

            except ValueError:
                print("Entrada inválida. Ingrese solo números enteros.")

        elif opcion == "4":
            try:
                resultados, ui = run_congruencial_mixto()
                ultima_secuencia_ui = ui
                validar_secuencia(ultima_secuencia_ui)

            except ValueError:
                print("Entrada inválida. Ingrese solo números enteros.")

        elif opcion == "5":
            try:
                resultados, ui = run_congruencial_multiplicativo()
                ultima_secuencia_ui = ui
                validar_secuencia(ultima_secuencia_ui)

            except ValueError:
                print("Entrada inválida. Ingrese solo números enteros.")

        elif opcion == "6":
            print("\n--- Validación con Test Chi-cuadrado ---")
            if not ultima_secuencia_ui:
                print("⚠️ No hay ninguna secuencia generada todavía.")
            else:
                try:
                    k = int(input("Ingrese la cantidad de intervalos (k): "))
                    resultado = chi_cuadrado(ultima_secuencia_ui, k)
                    mostrar_resultado(resultado)
                    ultima_secuencia_valida = resultado['pasa']
                except ValueError:
                    print("Ingrese un número entero válido.")

        elif opcion == "7":
            print("\n--- Simulación del Bar UCP ---")
            if not ultima_secuencia_ui:
                print("⚠️ No hay ninguna secuencia generada. Genere una primero con opciones 1–5.")
            elif not ultima_secuencia_valida:
                print("⚠️ La última secuencia generada no pasó el test de chi-cuadrado.")
                print("Por favor, genere una nueva secuencia o valide la actual con la opción 6.")
            else:
                try:
                    lambd = float(input("Ingrese una aproximación de la cantidad de alumnos que entran al bar por minuto: "))
                    duracion = int(input("Ingrese la duración del recreo en segundos (ej: 600): "))
                    cant_cajeros = int(input("Ingrese la cantidad de cajeros: "))
                    cant_preparadores = int(input("Ingrese la cantidad de preparadores: "))

                    simular_bar_ucp(
                        ui=ultima_secuencia_ui,
                        lambd=lambd,
                        duracion=duracion,
                        cant_cajeros=cant_cajeros,
                        cant_preparadores=cant_preparadores
                    )
                except ValueError:
                    print("Error: Ingrese valores válidos.")

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
