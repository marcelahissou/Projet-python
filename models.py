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
        # maxlen limite automatiquement la taille de la file (concept de goulot)
        self.queue = collections.deque(maxlen=queue_size)
        # Bloc 5 : On utilise un dictionnaire pour stocker {nom_voisin: poids_du_lien}
        self.neighbors = {} 

    def receive_packet(self, packet):
        """
        Tente d'ajouter un paquet à la file d'attente.
        Retourne True si accepté, False si rejeté (goulot d'étranglement).
        """
        if len(self.queue) < self.queue.maxlen:
            self.queue.append(packet)
            # On laisse le print pour le debug console
            print(f"[{self.name}] Paquet {packet.id} accepté dans la file.")
            return True
        else:
            print(f"[{self.name}] !!! saturation !!! Paquet {packet.id} rejeté.")
            return False

    def process_packet(self):
        """
        Simule le traitement d'un paquet (libère une place dans la file).
        """
        if self.queue:
            return self.queue.popleft()
        return None
