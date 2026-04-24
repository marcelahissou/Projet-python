import matplotlib.pyplot as plt
import networkx as nx
import csv

def generer_statistiques(nom_fichier_csv, net_obj, chemin_optimal):
    """Génère le camembert de performance et la carte du réseau."""
    succes, echecs = 0, 0
    try:
        # 1. Lecture des stats
        with open(nom_fichier_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['statut'] == 'REUSSI': succes += 1
                else: echecs += 1
        
        plt.figure(figsize=(14, 6))
        
        # Sous-graphe 1 : Le Camembert
        plt.subplot(1, 2, 1)
        plt.pie([succes, echecs], labels=['Succès', 'Échecs'], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
        plt.title("Taux de Réussite des Paquets")

        # Sous-graphe 2 : La Carte du Réseau
        plt.subplot(1, 2, 2)
        G = nx.Graph()
        
        # On parcourt le dictionnaire neighbors de chaque nœud
        for node_name, node_obj in net_obj.nodes.items():
            for neighbor, weight in node_obj.neighbors.items():
                G.add_edge(node_name, neighbor, weight=weight)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')
        
        # On surligne le chemin Dijkstra en rouge
        if chemin_optimal:
            path_edges = list(zip(chemin_optimal, chemin_optimal[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
            nx.draw_networkx_nodes(G, pos, nodelist=chemin_optimal, node_color='orange')

        plt.title("Chemin Optimal détecté par Dijkstra")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Erreur lors de la visualisation : {e}")
