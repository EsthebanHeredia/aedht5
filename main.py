import simpy
from simulacion.simulador import Simulador

def ejecutar_simulacion(num_procesos):
    print(f"\n==== Simulación con {num_procesos} procesos ====")
    env = simpy.Environment()
    simulador = Simulador(env, num_procesos, capacidad_memoria=100, num_nucleos=2)
    simulador.correr()

if __name__ == "__main__":
    for num in [25, 50, 100, 150, 200]:
        ejecutar_simulacion(num)
