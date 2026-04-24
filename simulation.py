from models import Node, Packet
from storage import sauvegarder_csv, sauvegarder_config_json # Import du Bloc 4
import random

def run_interactive_simulation():
    print("--- TEST DU BLOC 4 ---")
    node_name = input("Nom du routeur : ")
    q_size = int(input("Capacité (ex: 3) : "))
    
    router = Node(node_name, queue_size=q_size)
    nb_paquets = int(input("Nombre de paquets à envoyer (ex: 10) : "))

    historique_simulation = []

    for i in range(1, nb_paquets + 1):
        p = Packet(id=i, source="PC", destination="Cloud", size=random.randint(10, 100))
        statut = "RECU" if router.receive_packet(p) else "PERDU"
        
        # On remplit la liste pour le storage
        historique_simulation.append({
            "ID_Paquet": p.id,
            "Source": p.source,
            "Destination": p.destination,
            "Taille": p.size,
            "Resultat": statut
        })

    # APPEL DU BLOC 4
    sauvegarder_csv(historique_simulation)
    sauvegarder_config_json(node_name, q_size)
    
    print("\nSimulation terminée. Vérifiez vos fichiers .csv et .json !")

if __name__ == "__main__":
    run_interactive_simulation()
