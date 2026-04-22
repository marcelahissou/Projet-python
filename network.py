class Network:
    def __init__(self):
        self.nodes = {} # Dictionnaire {nom_du_noeud: objet_Node}

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_link(self, name1, name2):
        # On dit au nœud 1 qu'il peut envoyer au nœud 2 et vice-versa
        node1 = self.nodes[name1]
        node2 = self.nodes[name2]
        node1.neighbors[name2] = node2
        node2.neighbors[name1] = node1
