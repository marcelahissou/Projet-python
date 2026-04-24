import collections

class Packet:
    def __init__(self, id, source, destination, size):
        self.id = id
        self.source = source
        self.destination = destination
        self.size = size

class Node:
    def __init__(self, name, queue_size=5):
        self.name = name
        # On utilise maxlen pour limiter la file (Goulot d'étranglement)
        self.queue = collections.deque(maxlen=queue_size)
        # Bloc 4 : Dictionnaire pour stocker les nœuds voisins connectés
        self.neighbors = {} 

    def receive_packet(self, packet):
        """Tente de recevoir un paquet dans la file d'attente."""
        if len(self.queue) < self.queue.maxlen:
            self.queue.append(packet)
            print(f"[{self.name}] Paquet {packet.id} reçu.")
            return True
        else:
            print(f"[{self.name}] !!! GOULOT D'ÉTRANGLEMENT !!! Paquet {packet.id} perdu.")
            return False
