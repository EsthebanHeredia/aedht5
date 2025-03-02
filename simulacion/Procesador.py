import simpy

class Procesador:
    def __init__(self, env, num_nucleos):
        """Inicializa un procesador con un número de núcleos específico."""
        self.env = env
        self.cpu = simpy.Resource(env, capacity=num_nucleos)
