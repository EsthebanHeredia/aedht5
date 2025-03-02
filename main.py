import simpy
from simulacion.Simulador import Simulador
import statistics

def ejecutar_simulacion(num_procesos):
    print(f"\n==== Simulación con {num_procesos} procesos ====")
    env = simpy.Environment()
    sim = Simulador(env, num_procesos, capacidad_memoria=100, num_nucleos=2)
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
    print("Núm. Procesos | Tiempo Total | Tiempo Promedio | % Uso CPU | % Uso Memoria")
    print("-------------|-------------|----------------|-----------|-------------")
    
    for res in todos_resultados:
        datos = res['datos']
        print(f"{res['num_procesos']:13} | {datos['tiempo_total']:11.2f} | {datos['tiempo_promedio']:14.2f} | {datos['uso_cpu']*100:9.2f}% | {datos['uso_memoria']*100:12.2f}%")
    
    print("\n* Todos los tiempos están en unidades de simulación")