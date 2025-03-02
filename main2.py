import simpy
from simulacion.Simulador import Simulador
import statistics
import matplotlib.pyplot as plt

def ejecutar_simulacion(num_procesos):
    print(f"\n==== Simulación con {num_procesos} procesos ====")
    env = simpy.Environment()
    sim = Simulador(env, num_procesos)
    resultados = sim.correr()
    return resultados

if __name__ == "__main__":
    todos_resultados = []
    
    for num in [25, 50, 100, 150, 200]:
        resultado = ejecutar_simulacion(num)
        todos_resultados.append({
            'num_procesos': num,
            'datos': resultado
        })
    
    # Mostrar resumen final
    print("\n\n=========== RESULTADOS FINALES ===========")
    print("Núm. Procesos | Tiempo Total | Tiempo Promedio | % Uso CPU | % Uso Memoria | Desviación Estándar")
    print("-------------|-------------|----------------|-----------|-------------|--------------------")
    
    tiempos_promedios = []
    num_procesos_list = []
    
    for res in todos_resultados:
        datos = res['datos']
        tiempos_promedios.append(datos['tiempo_promedio'])
        num_procesos_list.append(res['num_procesos'])
        desviacion_estandar = statistics.stdev(tiempos_promedios) if len(tiempos_promedios) > 1 else 0
        print(f"{res['num_procesos']:13} | {datos['tiempo_total']:11.2f} | {datos['tiempo_promedio']:14.2f} | {datos['uso_cpu']*100:9.2f}% | {datos['uso_memoria']*100:12.2f}% | {desviacion_estandar:18.2f}")
    
    # Graficar número de procesos vs tiempo promedio
    plt.figure(figsize=(10, 6))
    plt.plot(num_procesos_list, tiempos_promedios, marker='o')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Tiempo Promedio')
    plt.title('Número de Procesos vs Tiempo Promedio')
    plt.grid(True)
    plt.show()