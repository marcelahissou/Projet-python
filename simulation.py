from models import Node, Packet
from network import Network
from storage import sauvegarder_csv
import random

def run_complex_simulation():
    print("="*40)
    print("  SIMULATEUR RÉSEAU INTELLIGENT (BLOC 5)")
    print("="*40)

    # 1. CRÉATION DU RÉSEAU (Topologie)
    net = Network()
    
    # Création des nœuds avec des capacités de file (queue_size) variées
    net.add_node(Node("Source", queue_size=20))
    net.add_node(Node("Routeur_Rapide", queue_size=3))  # Petit goulot potentiel
    net.add_node(Node("Routeur_Fiable", queue_size=15))
    net.add_node(Node("Destination", queue_size=20))

    # Ajout des liens avec des POIDS (représentant la latence ou distance)
    # Chemin 1 : Source -> Routeur_Rapide -> Destination (Poids total = 2)
    net.add_link("Source", "Routeur_Rapide", weight=1)
    net.add_link("Routeur_Rapide", "Destination", weight=1)

    # Chemin 2 : Source -> Routeur_Fiable -> Destination (Poids total = 10)
    net.add_link("Source", "Routeur_Fiable", weight=5)
    net.add_link("Routeur_Fiable", "Destination", weight=5)

    print("\n[CONFIG] Réseau chargé avec deux chemins possibles.")
    
    # 2. CALCUL DU CHEMIN OPTIMAL
    depart = "Source"
    arrivee = "Destination"
    chemin_optimal = net.find_shortest_path(depart, arrivee)

    if not chemin_optimal:
        print("[ERREUR] Aucun chemin trouvé entre ces nœuds !")
        return

    print(f"[ALGO Dijkstra] Meilleure route calculée : {' -> '.join(chemin_optimal)}")

    # 3. SIMULATION DU TRAFIC
    try:
        nb_paquets = int(input("\nCombien de paquets envoyer sur ce chemin ? : "))
    except ValueError:
        nb_paquets = 5

    historique_log = []
    succes = 0

    for i in range(1, nb_paquets + 1):
        p = Packet(id=i, source=depart, destination=arrivee, size=random.randint(10, 100))
        
        # Le paquet tente de traverser tout le chemin calculé
        reussi, bloque_a = net.simulate_routing(p, chemin_optimal)
        
        statut = "SUCCES" if reussi else "ECHEC"
        if reussi: 
            succes += 1
        
        # Bloc 4 : On enregistre les données détaillées pour le CSV
        historique_log.append({
            "ID_Paquet": p.id,
            "Chemin_Utilise": " -> ".join(chemin_optimal),
            "Statut": statut,
            "Point_de_Blocage": bloque_a if not reussi else "Aucun"
        })

    # 4. SAUVEGARDE DES RÉSULTATS (Bloc 4)
    sauvegarder_csv(historique_log, "rapport_bloc5_routage.csv")

    # 5. BILAN
    print("\n" + "="*40)
    print(f" BILAN DE LA SIMULATION")
    print("="*40)
    print(f"Paquets arrivés : {succes} / {nb_paquets}")
    print(f"Chemin analysé  : {' -> '.join(chemin_optimal)}")
    if succes < nb_paquets:
        print(f"Note : Des goulots d'étranglement ont été détectés.")
    print(f"Rapport complet généré dans 'rapport_bloc5_routage.csv'")
    print("="*40)

if __name__ == "__main__":
    run_complex_simulation()
