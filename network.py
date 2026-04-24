import json

class Network:
    def __init__(self):
        self.nodes = {} # Dictionnaire {nom_du_noeud: objet_Node}

    def add_node(self, node):
        """Ajoute un nœud au réseau."""
        self.nodes[node.name] = node

    def add_link(self, name1, name2):
        """Crée une connexion bidirectionnelle entre deux nœuds."""
        if name1 in self.nodes and name2 in self.nodes:
            node1 = self.nodes[name1]
            node2 = self.nodes[name2]
            # On s'assure que l'attribut neighbors existe dans la classe Node (models.py)
            node1.neighbors[name2] = node2
            node2.neighbors[name1] = node1
        else:
            print(f"[Erreur] Un des nœuds ({name1} ou {name2}) n'existe pas.")

    # --- AJOUT BLOC 4 : PERSISTANCE DE LA TOPOLOGIE ---

    def export_topology(self, filename="topology.json"):
        """Sauvegarde la structure actuelle du réseau en JSON."""
        topology = {
            "nodes": [node.name for node in self.nodes.values()],
            "links": []
        }
        # On récupère les liens sans doublons
        seen_links = set()
        for node_name, node_obj in self.nodes.items():
            for neighbor in node_obj.neighbors:
                link = tuple(sorted((node_name, neighbor)))
                if link not in seen_links:
                    topology["links"].append(link)
                    seen_links.add(link)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(topology, f, indent=4)
        print(f"[Bloc 4] Topologie réseau sauvegardée dans {filename}")
