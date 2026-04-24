# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import networkx as nx
import csv
import random
from network import Network
from models import Node, Packet
from storage import sauvegarder_csv

# Création de la fenêtre unique
fig = plt.figure(figsize=(14, 7))
fig.canvas.manager.set_window_title("Analyseur de Trafic Reseau - Tout-en-un")

# Emplacement fixe des graphiques
ax_pie = plt.subplot2grid((6, 2), (0, 0), rowspan=4)
ax_net = plt.subplot2grid((6, 2), (0, 1), rowspan=4)

def exécuter_simulation_et_dessiner(nb_paquets):
    """Réinitialise le réseau, exécute la simulation et force le rafraîchissement."""
    
    # CRUCIAL : On recrée le réseau à NEUF à chaque clic pour vider les files d'attente (queues)
    net = Network()
    net.add_node(Node("Source", queue_size=20))
    net.add_node(Node("Routeur_A", queue_size=10))  
    net.add_node(Node("Routeur_B", queue_size=15))
    net.add_node(Node("Destination", queue_size=20))
    net.add_link("Source", "Routeur_A", weight=1)
    net.add_link("Routeur_A", "Destination", weight=1)
    net.add_link("Source", "Routeur_B", weight=5)
    net.add_link("Routeur_B", "Destination", weight=5)
    chemin = net.find_shortest_path("Source", "Destination")

    # 1. Simulation de flux
    historique_log = []
    for i in range(1, nb_paquets + 1):
        p = Packet(id=i, source="Source", destination="Destination", size=random.randint(10, 100))
        trajet_reussi = True
        for node_name in chemin:
            noeud_actuel = net.nodes[node_name]
            if not noeud_actuel.receive_packet(p):
                trajet_reussi = False
                break
        statut = "REUSSI" if trajet_reussi else "ECHEC"
        historique_log.append({"id": p.id, "statut": statut, "chemin": " -> ".join(chemin)})

    csv_file = "rapport_final.csv"
    sauvegarder_csv(historique_log, csv_file)

    # 2. Lecture des nouveaux résultats
    succes, echecs = 0, 0
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['statut'] == 'REUSSI': succes += 1
            else: echecs += 1

    # 3. Nettoyage et nouveau dessin du Camembert
    ax_pie.clear()
    # Si tout a échoué ou réussi, éviter les divisions par zéro visuelles
    if succes == 0 and echecs == 0: echecs = 1 
    ax_pie.pie([succes, echecs], labels=['Succes', 'Echecs'], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
    ax_pie.set_title(f"Taux de Reussite ({nb_paquets} paquets injectes)")

    # 4. Nettoyage et nouveau dessin de la Carte Réseau
    ax_net.clear()
    G = nx.Graph()
    for node_name, node_obj in net.nodes.items():
        for neighbor, weight in node_obj.neighbors.items():
            G.add_edge(node_name, neighbor, weight=weight)
    
    pos = nx.spring_layout(G, seed=42) # Layout stable
    nx.draw(G, pos, ax=ax_net, with_labels=True, node_color='skyblue', node_size=1000, font_weight='bold')
    
    if chemin:
        path_edges = list(zip(chemin, chemin[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax_net, edgelist=path_edges, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos, ax=ax_net, nodelist=chemin, node_color='orange')
    
    ax_net.set_title("Chemin Optimal detecte par Dijkstra")
    
    # FORCER le rafraîchissement graphique de la fenêtre de manière synchrone
    fig.canvas.draw_idle()

# --- Zone des boutons et entrées (hors de la fonction de dessin) ---
ax_box = plt.axes([0.25, 0.05, 0.20, 0.06])
text_box = widgets.TextBox(ax_box, 'Nombre de paquets : ', initial="20")

ax_btn = plt.axes([0.50, 0.05, 0.25, 0.06])
btn_lancer = widgets.Button(ax_btn, 'Lancer la Simulation', color='#2196F3', hovercolor='#0b7dda')

def action_lancer(event):
    try:
        valeur = int(text_box.text)
    except ValueError:
        valeur = 10
    exécuter_simulation_et_dessiner(valeur)

btn_lancer.on_clicked(action_lancer)

# Premier affichage automatique au chargement (avec 20 paquets)
exécuter_simulation_et_dessiner(20)
plt.show()