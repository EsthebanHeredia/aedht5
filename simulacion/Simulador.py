import random
import simpy
from simulacion.GestorMemoria import GestorMemoria
from simulacion.Procesador import Procesador

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

class Simulador:
    def __init__(self, env, num_procesos, capacidad_memoria=200, num_nucleos=1, instrucciones_por_ciclo=3, intervalo_llegada=10):
        self.env = env
        self.memoria = GestorMemoria(env, capacidad_memoria)
        self.procesador = Procesador(env, num_nucleos)
        self.num_procesos = num_procesos
        self.capacidad_memoria = capacidad_memoria
        self.num_nucleos = num_nucleos
        self.instrucciones_por_ciclo = instrucciones_por_ciclo
        self.intervalo_llegada = intervalo_llegada
        
        self.tiempos_inicio = {}
        self.tiempos_fin = {}
        self.tiempos_cpu = {}
        self.memoria_utilizada = []
        self.cpu_utilizada = []
        self.tiempo_inicio_global = 0
        self.tiempo_fin_global = 0

    def proceso(self, id_proceso, instrucciones, memoria_requerida):
        self.tiempos_inicio[id_proceso] = self.env.now
        print(f'[{self.env.now}] Proceso {id_proceso} esperando memoria...')
        yield self.memoria.solicitar_memoria(memoria_requerida)
        self.memoria_utilizada.append(memoria_requerida)

        print(f'[{self.env.now}] Proceso {id_proceso} obtuvo memoria y espera CPU.')
        while instrucciones > 0:
            with self.procesador.cpu.request() as req:
                yield req
                print(f'[{self.env.now}] Proceso {id_proceso} ejecutándose...')
                instrucciones_a_ejecutar = min(instrucciones, self.instrucciones_por_ciclo)
                yield self.env.timeout(instrucciones_a_ejecutar)
                instrucciones -= instrucciones_a_ejecutar
                self.cpu_utilizada.append(instrucciones_a_ejecutar)
                self.tiempos_cpu[id_proceso] = self.tiempos_cpu.get(id_proceso, 0) + instrucciones_a_ejecutar

                if instrucciones == 0:
                    print(f'[{self.env.now}] Proceso {id_proceso} finalizado, liberando memoria.')
                    yield self.memoria.liberar_memoria(memoria_requerida)
                    self.tiempos_fin[id_proceso] = self.env.now
                    self.tiempo_fin_global = self.env.now
                    break
                else:
                    decision = random.randint(1, 2)
                    if decision == 1:
                        print(f'[{self.env.now}] Proceso {id_proceso} esperando I/O.')
                        yield self.env.timeout(random.randint(1, 5))
                    print(f'[{self.env.now}] Proceso {id_proceso} vuelve a ready.')

    def generar_procesos(self):
        for i in range(self.num_procesos):
            yield self.env.timeout(random.expovariate(1.0 / self.intervalo_llegada))
            instrucciones = random.randint(1, 10)
            memoria_requerida = random.randint(1, 10)
            self.env.process(self.proceso(i, instrucciones, memoria_requerida))

    def correr(self):
        self.tiempo_inicio_global = self.env.now
        self.env.process(self.generar_procesos())
        self.env.run()
        
        tiempos_totales = [self.tiempos_fin[i] - self.tiempos_inicio[i] 
                          for i in range(self.num_procesos) if i in self.tiempos_fin]
        
        tiempo_total = self.tiempo_fin_global - self.tiempo_inicio_global
        tiempo_promedio = sum(tiempos_totales) / len(tiempos_totales) if tiempos_totales else 0
        
        uso_memoria_promedio = sum(self.memoria_utilizada) / (self.capacidad_memoria * tiempo_total) if tiempo_total > 0 else 0
        uso_cpu_promedio = sum(self.tiempos_cpu.values()) / (tiempo_total * self.num_nucleos) if tiempo_total > 0 else 0
        
        return {
            'tiempo_total': tiempo_total,
            'tiempo_promedio': tiempo_promedio,
            'uso_cpu': min(uso_cpu_promedio, 1.0),
            'uso_memoria': min(uso_memoria_promedio, 1.0)
        }
