import heapq

class Network:
    def __init__(self):
        self.nodes = {} # {nom_du_noeud: objet_Node}

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_link(self, name1, name2, weight=1):
        """Crée un lien entre deux nœuds avec un poids (latence/distance)."""
        if name1 in self.nodes and name2 in self.nodes:
            # On stocke le poids pour l'algorithme de Dijkstra
            self.nodes[name1].neighbors[name2] = weight
            self.nodes[name2].neighbors[name1] = weight
        else:
            print(f"[Erreur] Impossible de lier {name1} et {name2}.")

    def find_shortest_path(self, start_name, end_name):
        """
        Algorithme de Dijkstra pour trouver le chemin le plus rapide.
        """
        # Distances infinies au départ
        distances = {node: float('inf') for node in self.nodes}
        distances[start_name] = 0
        
        # File de priorité : (distance_cumulée, nom_noeud)
        priority_queue = [(0, start_name)]
        # Pour reconstruire le trajet
        previous_nodes = {node: None for node in self.nodes}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Si on est arrivés, on arrête
            if current_node == end_name:
                break

            if current_distance > distances[current_node]:
                continue

            # On explore les voisins
            for neighbor_name, weight in self.nodes[current_node].neighbors.items():
                distance = current_distance + weight
                
                if distance < distances[neighbor_name]:
                    distances[neighbor_name] = distance
                    previous_nodes[neighbor_name] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor_name))

        # Reconstruction du chemin final
        path = []
        node = end_name
        while node is not None:
            path.append(node)
            node = previous_nodes[node]
        path.reverse()

        return path if path[0] == start_name else []

    def simulate_routing(self, packet, path):
        """
        Fait voyager le paquet à travers le chemin calculé.
        """
        print(f"\n[ROUTAGE] Trajet prévu : {' -> '.join(path)}")
        for node_name in path:
            current_node = self.nodes[node_name]
            if not current_node.receive_packet(packet):
                print(f"  > Bloqué à {node_name} (Goulot d'étranglement)")
                return False, node_name
        return True, "Destination"
