import random
from simulacion.GestorMemoria import GestorMemoria
from simulacion.Procesador import Procesador


class Simulador:
    def __init__(self, env, num_procesos, capacidad_memoria, num_nucleos):
        """Inicializa la simulación con memoria y procesador."""
        self.env = env
        self.memoria = GestorMemoria(env, capacidad_memoria)
        self.procesador = Procesador(env, num_nucleos)
        self.num_procesos = num_procesos
        self.capacidad_memoria = capacidad_memoria
        self.num_nucleos = num_nucleos
        
        # Estadísticas
        self.tiempos_inicio = {}
        self.tiempos_fin = {}
        self.tiempos_cpu = {}
        self.memoria_utilizada = []
        self.cpu_utilizada = []
        self.tiempo_inicio_global = 0
        self.tiempo_fin_global = 0

    def proceso(self, id_proceso, tiempo_uso, memoria_requerida):
        """Simula la ejecución de un proceso."""
        self.tiempos_inicio[id_proceso] = self.env.now
        
        print(f'[{self.env.now}] Proceso {id_proceso} esperando memoria...')
        yield self.memoria.solicitar_memoria(memoria_requerida)
        self.memoria_utilizada.append(memoria_requerida)

        print(f'[{self.env.now}] Proceso {id_proceso} obtuvo memoria y espera CPU.')
        inicio_espera_cpu = self.env.now
        
        with self.procesador.cpu.request() as req:
            yield req
            tiempo_espera_cpu = self.env.now - inicio_espera_cpu
            print(f'[{self.env.now}] Proceso {id_proceso} ejecutándose...')
            
            # Registrar uso de CPU
            self.cpu_utilizada.append(1)  # Un núcleo está ocupado
            
            yield self.env.timeout(tiempo_uso)
            
            # Registrar tiempo en CPU
            self.tiempos_cpu[id_proceso] = tiempo_uso

        print(f'[{self.env.now}] Proceso {id_proceso} finalizado, liberando memoria.')
        yield self.memoria.liberar_memoria(memoria_requerida)
        
        # Registrar finalización
        self.tiempos_fin[id_proceso] = self.env.now
        self.tiempo_fin_global = self.env.now

    def correr(self):
        """Crea y ejecuta los procesos en el entorno de simulación."""
        self.tiempo_inicio_global = self.env.now
        
        for i in range(self.num_procesos):
            tiempo_uso = random.expovariate(1.0 / 10)
            memoria_requerida = random.randint(1, 10)
            self.env.process(self.proceso(i, tiempo_uso, memoria_requerida))
        
        self.env.run()
        
        # Calcular estadísticas
        tiempos_totales = [self.tiempos_fin[i] - self.tiempos_inicio[i] 
                          for i in range(self.num_procesos) if i in self.tiempos_fin]
        
        tiempo_total = self.tiempo_fin_global - self.tiempo_inicio_global
        tiempo_promedio = sum(tiempos_totales) / len(tiempos_totales) if tiempos_totales else 0
        
        # Cálculos aproximados de uso
        uso_memoria_promedio = sum(self.memoria_utilizada) / (self.capacidad_memoria * tiempo_total) if tiempo_total > 0 else 0
        uso_cpu_promedio = sum(self.tiempos_cpu.values()) / (tiempo_total * self.num_nucleos) if tiempo_total > 0 else 0
        
        return {
            'tiempo_total': tiempo_total,
            'tiempo_promedio': tiempo_promedio,
            'uso_cpu': min(uso_cpu_promedio, 1.0),  # No puede ser mayor que 1
            'uso_memoria': min(uso_memoria_promedio, 1.0)  # No puede ser mayor que 1
        }