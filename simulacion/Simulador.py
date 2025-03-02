import random
from simulacion.GestorMemoria import GestorMemoria
from simulacion.Procesador import Procesador


class Simulador:  # Cambiado de "simulador" a "Simulador"
    def __init__(self, env, num_procesos, capacidad_memoria, num_nucleos):
        """Inicializa la simulación con memoria y procesador."""
        self.env = env
        self.memoria = GestorMemoria(env, capacidad_memoria)
        self.procesador = Procesador(env, num_nucleos)
        self.num_procesos = num_procesos

    def proceso(self, id_proceso, tiempo_uso, memoria_requerida):
        """Simula la ejecución de un proceso."""
        print(f'[{self.env.now}] Proceso {id_proceso} esperando memoria...')
        yield self.memoria.solicitar_memoria(memoria_requerida)

        print(f'[{self.env.now}] Proceso {id_proceso} obtuvo memoria y espera CPU.')
        with self.procesador.cpu.request() as req:
            yield req
            print(f'[{self.env.now}] Proceso {id_proceso} ejecutándose...')
            yield self.env.timeout(tiempo_uso)

        print(f'[{self.env.now}] Proceso {id_proceso} finalizado, liberando memoria.')
        yield self.memoria.liberar_memoria(memoria_requerida)

    def correr(self):
        """Crea y ejecuta los procesos en el entorno de simulación."""
        for i in range(self.num_procesos):
            tiempo_uso = random.expovariate(1.0 / 10)
            memoria_requerida = random.randint(1, 10)
            self.env.process(self.proceso(i, tiempo_uso, memoria_requerida))
        self.env.run()