import simpy

class GestorMemoria:
    def __init__(self, env, capacidad):
        """Inicializa la memoria con una capacidad específica."""
        self.env = env
        self.memoria = simpy.Container(env, init=capacidad, capacity=capacidad)

    def solicitar_memoria(self, cantidad):
        """Retorna un evento que simula la solicitud de memoria."""
        return self.memoria.get(cantidad)

    def liberar_memoria(self, cantidad):
        """Libera memoria después de que un proceso termina."""
        return self.memoria.put(cantidad)
