from models import Node, Packet
from network import Network
from storage import sauvegarder_csv
from visualisation import generer_statistiques
import random

def run_simulation_interactive():
    print("="*50)
    print("   ANALYSEUR DE TRAFIC RÉSEAU - BLOC 6")
    print("="*50)

    # 1. INITIALISATION DU RÉSEAU
    net = Network()
    
    # On crée une topologie fixe pour le test
    net.add_node(Node("Source", queue_size=20))
    net.add_node(Node("Routeur_A", queue_size=5))  # Goulot potentiel
    net.add_node(Node("Routeur_B", queue_size=15))
    net.add_node(Node("Destination", queue_size=20))

    # Liens avec poids (Dijkstra choisira le chemin le plus léger)
    net.add_link("Source", "Routeur_A", weight=1)
    net.add_link("Routeur_A", "Destination", weight=1)
    net.add_link("Source", "Routeur_B", weight=5)
    net.add_link("Routeur_B", "Destination", weight=5)

    # 2. CALCUL DU CHEMIN OPTIMAL
    chemin = net.find_shortest_path("Source", "Destination")
    print(f"\n[ALGO] Meilleur itinéraire : {' -> '.join(chemin)}")

    # 3. SAISIE UTILISATEUR DU TRAFIC
    try:
        # L'utilisateur donne ici le nombre de paquets
        nb_paquets = int(input("\nCombien de paquets souhaitez-vous injecter ? : "))
    except ValueError:
        print("[!] Valeur invalide, envoi de 5 paquets par défaut.")
        nb_paquets = 5

    # 4. SIMULATION DU FLUX
    historique_log = []
    succes = 0

    print(f"\n>>> Lancement de la simulation sur {nb_paquets} paquets...")

    for i in range(1, nb_paquets + 1):
        p = Packet(id=i, source="Source", destination="Destination", size=random.randint(10, 100))
        
        trajet_reussi = True
        for node_name in chemin:
            noeud_actuel = net.nodes[node_name]
            if not noeud_actuel.receive_packet(p):
                trajet_reussi = False
                break
        
        statut = "REUSSI" if trajet_reussi else "ECHEC"
        if trajet_reussi: succes += 1
        
        historique_log.append({
            "id": p.id,
            "statut": statut,
            "chemin": " -> ".join(chemin)
        })

    # 5. SAUVEGARDE ET VISUALISATION
    csv_file = "rapport_final.csv"
    sauvegarder_csv(historique_log, csv_file)

    print("\n" + "="*50)
    print(f" BILAN : {succes}/{nb_paquets} paquets délivrés.")
    print(f" Rapport sauvegardé dans {csv_file}")
    print("="*50)
    
    # Appel de la visualisation avec le graphe et le camembert
    print("\n[VUE] Génération des graphiques en cours...")
    generer_statistiques(csv_file, net, chemin)

if __name__ == "__main__":
    run_simulation_interactive()
