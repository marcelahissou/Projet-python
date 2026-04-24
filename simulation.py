from models import Node, Packet
from network import Network
from storage import sauvegarder_csv
import random

def run_simulation_interactive():
    print("="*50)
    print("   ANALYSEUR DE TRAFIC RÉSEAU - BLOC 6")
    print("="*50)

    # 1. INITIALISATION DU RÉSEAU
    net = Network()
    
    net.add_node(Node("Source", queue_size=20))
    net.add_node(Node("Routeur_A", queue_size=10))  
    net.add_node(Node("Routeur_B", queue_size=15))
    net.add_node(Node("Destination", queue_size=20))

    net.add_link("Source", "Routeur_A", weight=1)
    net.add_link("Routeur_A", "Destination", weight=1)
    net.add_link("Source", "Routeur_B", weight=5)
    net.add_link("Routeur_B", "Destination", weight=5)

    # 2. CALCUL DU CHEMIN OPTIMAL
    chemin = net.find_shortest_path("Source", "Destination")
    print(f"\n[ALGO] Meilleur itinéraire : {' -> '.join(chemin)}")

    # 3. SAISIE UTILISATEUR DU TRAFIC
    try:
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

    # 5. SAUVEGARDE UNIQUE
    csv_file = "rapport_final.csv"
    sauvegarder_csv(historique_log, csv_file)

    print("\n" + "="*50)
    print(f" BILAN : {succes}/{nb_paquets} paquets délivrés.")
    print(f" Rapport sauvegardé dans {csv_file}")
    print(" Fin du  trajet")
    print("="*50)

if __name__ == "__main__":
    run_simulation_interactive()
