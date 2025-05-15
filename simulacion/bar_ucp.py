from collections import deque
import math

def escalar_ui(ui: float, min_val: int, max_val: int) -> int:
    return int(min_val + ui * (max_val - min_val + 1))

def generar_poisson(lambd, ui, minutos):
    resultados = []
    idx = 0
    for _ in range(minutos):
        L = math.exp(-lambd)
        k = 0
        p = 1
        while p > L:
            if idx >= len(ui):
                raise ValueError("No hay suficientes números pseudoaleatorios")
            p *= ui[idx]
            idx += 1
            k += 1
        resultados.append(k - 1)
    return resultados, idx

def simular_bar_ucp(ui: list[float], lambd: float, duracion: int, cant_cajeros: int, cant_preparadores: int):
    index_ui = 0
    alumnos = []
    minutos = duracion // 60
    llegadas_por_minuto, index_ui = generar_poisson(lambd, ui, minutos)

    for minuto, cantidad in enumerate(llegadas_por_minuto):
        for _ in range(cantidad):
            if index_ui + 4 >= len(ui):
                break
            llegada = minuto * 60 + escalar_ui(ui[index_ui], 0, 59)
            tipo = "simple" if ui[index_ui + 1] < 0.6 else "preparado"
            t_caja = escalar_ui(ui[index_ui + 2], 35, 40)
            t_barra = escalar_ui(ui[index_ui + 3], 70, 80) if tipo == "preparado" else 0
            llegada = min(llegada, duracion - 1)
            alumnos.append({
                "llegada": llegada,
                "tipo": tipo,
                "t_caja": t_caja,
                "t_barra": t_barra,
                "atendido": False
            })
            index_ui += 4

    llegadas_por_minuto_real = [0] * minutos
    for a in alumnos:
        minuto = a["llegada"] // 60
        llegadas_por_minuto_real[minuto] += 1

    cola_caja = deque()
    cola_barra = deque()
    cajeros = [0] * cant_cajeros
    preparadores = [0] * cant_preparadores
    atendidos = []
    pendientes = sorted(alumnos, key=lambda x: x["llegada"])

    for tiempo in range(duracion):
        while pendientes and pendientes[0]["llegada"] == tiempo:
            cola_caja.append(pendientes.pop(0))

        actuales_caja = list(cola_caja)
        cola_caja.clear()
        for alumno in actuales_caja:
            for i in range(cant_cajeros):
                if cajeros[i] <= tiempo:
                    inicio = tiempo
                    fin = inicio + alumno["t_caja"]
                    if fin <= duracion:
                        alumno["inicio_caja"] = inicio
                        alumno["fin_caja"] = fin
                        cajeros[i] = fin
                        if alumno["tipo"] == "simple":
                            alumno["atendido"] = True
                            atendidos.append(alumno)
                        else:
                            cola_barra.append(alumno)
                        break
            else:
                cola_caja.append(alumno)

        actuales_barra = list(cola_barra)
        cola_barra.clear()
        for alumno in actuales_barra:
            for i in range(cant_preparadores):
                if preparadores[i] <= tiempo:
                    inicio = max(tiempo, alumno["fin_caja"])
                    fin = inicio + alumno["t_barra"]
                    if fin <= duracion:
                        alumno["inicio_barra"] = inicio
                        alumno["fin_barra"] = fin
                        alumno["atendido"] = True
                        preparadores[i] = fin
                        atendidos.append(alumno)
                        break
            else:
                cola_barra.append(alumno)

    total_alumnos_generados = len(alumnos)
    total_pedidos_simples_generados = sum(1 for a in alumnos if a["tipo"] == "simple")
    total_pedidos_preparados_generados = total_alumnos_generados - total_pedidos_simples_generados

    alumnos_atendidos = [a for a in alumnos if a["atendido"]]
    alumnos_no_atendidos = [a for a in alumnos if not a["atendido"]]
    alumnos_no_atendidos_en_caja = [a for a in cola_caja if "inicio_caja" not in a]
    alumnos_no_atendidos_en_barra = [a for a in cola_barra if "inicio_barra" not in a]

    atendidos_simples = [a for a in alumnos_atendidos if a["tipo"] == "simple"]
    atendidos_preparados = [a for a in alumnos_atendidos if a["tipo"] == "preparado"]

    promedio_tiempo_en_caja = round(sum(a["t_caja"] for a in alumnos_atendidos) / len(alumnos_atendidos), 2) if alumnos_atendidos else 0
    promedio_tiempo_en_barra = round(sum(a["t_barra"] for a in atendidos_preparados) / len(atendidos_preparados), 2) if atendidos_preparados else 0

    porcentaje_alumnos_atendidos = round((len(alumnos_atendidos) / total_alumnos_generados) * 100, 2) if total_alumnos_generados else 0
    porcentaje_rechazo_en_caja = round((len(alumnos_no_atendidos_en_caja) / total_alumnos_generados) * 100, 2) if total_alumnos_generados else 0
    porcentaje_rechazo_en_barra = round((len(alumnos_no_atendidos_en_barra) / total_pedidos_preparados_generados) * 100, 2) if total_pedidos_preparados_generados else 0

    cuello_de_botella_detectado = "BARRA" if len(alumnos_no_atendidos_en_barra) > len(alumnos_no_atendidos_en_caja) else "CAJA"

    print("\n===RESULTADOS DE LA SIMULACIÓN DEL BAR UCP===")

    print("\n\n ===== PARÁMETROS BASE GENERADOS ===== ")
    print("Estos valores representan la cantidad de alumnos generados al inicio de la simulación.")
    print(f"- Total de alumnos con intención de compra: {total_alumnos_generados}")
    print(f"- Cantidad de alumnos con intención de compra simple: {total_pedidos_simples_generados}")
    print(f"- Cantidad de alumnos con intención de compra preparado: {total_pedidos_preparados_generados}")
    print("- Alumnos con intención de compra entrando al bar por minuto:")
    for minuto, cantidad in enumerate(llegadas_por_minuto_real):
        print(f"  Minuto {minuto:2}: {cantidad} alumnos")

    print("\n\n ===== RESULTADOS DE ATENCIÓN EN LA SIMULACIÓN ===== ")
    print("Estos valores muestran cuántos alumnos fueron realmente atendidos o no.")
    print(f"- Alumnos atendidos completamente: {len(alumnos_atendidos)}")
    print(f"  • Atendidos solo en CAJA (pedido simple): {len(atendidos_simples)}")
    print(f"  • Atendidos en CAJA y BARRA (pedido preparado): {len(atendidos_preparados)}")
    print(f"- Alumnos no atendidos completamente: {len(alumnos_no_atendidos)}")
    print(f"  • Alumnos no atendidos en CAJA: {len(alumnos_no_atendidos_en_caja)}")
    print(f"  • Alumnos no atendidos en BARRA: {len(alumnos_no_atendidos_en_barra)}")

    print("\n\n ===== MÉTRICAS ESTADÍSTICAS ===== ")
    print("Indicadores de rendimiento del sistema durante el recreo.")
    print(f"- Porcentaje de alumnos atendidos: {porcentaje_alumnos_atendidos}%")
    print(f"- Porcentaje de rechazo en CAJA: {porcentaje_rechazo_en_caja}%")
    print(f"- Porcentaje de rechazo en BARRA: {porcentaje_rechazo_en_barra}%")
    print(f"- Promedio de tiempo de atención en CAJA: {promedio_tiempo_en_caja}s")
    print(f"- Promedio de tiempo de atención en BARRA: {promedio_tiempo_en_barra}s (solo preparados)")

    print("\n\n ===== USO DE NÚMEROS PSEUDOALEATORIOS ===== ")
    print("Se detallan a continuación los valores generados a partir de números pseudoaleatorios, qué representan y cómo se calculan:")

    print("\n• Llegadas por minuto (Poisson)")
    print("  - ¿Qué representa?: Cantidad de alumnos que entran al bar en cada minuto.")
    print("  - ¿Cómo se calcula?: Se aplica el algoritmo de Poisson: se multiplican números pseudoaleatorios hasta que el producto sea menor a e^(-λ).")

    print("\n• Momento exacto de llegada")
    print("  - ¿Qué representa?: El segundo exacto del minuto en que el alumno llega al bar.")
    print("  - ¿Cómo se calcula?: Se escala con la fórmula: segundo = min + ui × (max - min + 1), donde min=0 y max=59.")

    print("\n• Tipo de pedido")
    print("  - ¿Qué representa?: Determina si el alumno hará un pedido simple o preparado.")
    print("  - ¿Cómo se calcula?: Si el número generado es menor a 0.6, se considera 'simple'; si es 0.6 o más, es 'preparado'.")

    print("\n• Tiempo en CAJA")
    print("  - ¿Qué representa?: Tiempo que tarda el alumno en ser atendido en caja.")
    print("  - ¿Cómo se calcula?: Se usa la misma fórmula de escalado: t_caja = min + ui × (max - min + 1), donde min=35 y max=40.")

    print("\n• Tiempo en BARRA (solo si el pedido es preparado)")
    print("  - ¿Qué representa?: Tiempo que demora el preparador en realizar el pedido del alumno.")
    print("  - ¿Cómo se calcula?: t_barra = min + ui × (max - min + 1), donde min=70 y max=80.")

    print("\n📌 En resumen:")
    print("- Cada alumno utiliza 4 números pseudoaleatorios para su generación y atención.")
    print("- Además, el algoritmo de Poisson al inicio consume números extra para calcular la cantidad de llegadas por minuto.")
