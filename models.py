import collections

class Packet:
    def __init__(self, id, source, destination, size):
        self.id = id
        self.source = source
        self.destination = destination
        self.size = size

class Node:
    # L'argument queue_size doit être présent ici avec une valeur par défaut
    def __init__(self, name, queue_size=5): 
        self.name = name
        # On utilise maxlen pour limiter automatiquement la taille de la file
        self.queue = collections.deque(maxlen=queue_size) 

    def receive_packet(self, packet):
        if len(self.queue) < self.queue.maxlen:
            self.queue.append(packet)
            print(f"[{self.name}] Paquet {packet.id} reçu.")
            return True
        else:
            print(f"[{self.name}] !!! GOULOT D'ÉTRANGLEMENT !!! Paquet {packet.id} perdu.")
            return False
