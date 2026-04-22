from models import Node, Packet
import random

def run_interactive_simulation():
    print("="*40)
    print("   ANALYSEUR DE TRAFIC RÉSEAU (INTERACTIF)")
    print("="*40)

    # 1. Configuration du matériel par l'utilisateur
    print("\n--- ÉTAPE 1 : Configuration du Nœud Central ---")
    node_name = input("Nom du routeur à tester (ex: Routeur_Sud) : ")
    try:
        q_size = int(input(f"Capacité de la file d'attente pour {node_name} (nombre de paquets) : "))
    except ValueError:
        print("Erreur : Veuillez entrer un nombre entier. Valeur par défaut (5) appliquée.")
        q_size = 5

    # Création du nœud selon les choix de l'utilisateur
    router = Node(node_name, queue_size=q_size)

    # 2. Configuration du trafic
    print("\n--- ÉTAPE 2 : Simulation du Flux ---")
    try:
        nb_paquets = int(input("Combien de paquets souhaitez-vous injecter dans le réseau ? : "))
    except ValueError:
        print("Erreur : Nombre de paquets invalide. Valeur par défaut (10) appliquée.")
        nb_paquets = 10

    print(f"\n>>> Simulation en cours sur {node_name}...")
    
    succes = 0
    echecs = 0

    # Envoi des paquets
    for i in range(1, nb_paquets + 1):
        # On génère des données aléatoires pour simuler un vrai trafic
        p = Packet(id=i, source="Utilisateur", destination="Serveur_Cloud", size=random.randint(10, 100))
        
        if router.receive_packet(p):
            succes += 1
        else:
            echecs += 1

    # 3. Rapport d'analyse final
    print("\n" + "="*40)
    print("          RAPPORT D'ANALYSE")
    print("="*40)
    print(f"Nœud analysé        : {router.name}")
    print(f"Trafic total envoyé : {nb_paquets}")
    print(f"Paquets délivrés    : {succes}")
    print(f"Paquets rejetés     : {echecs}")

    if echecs > 0:
        taux_perte = (echecs / nb_paquets) * 100
        print(f"\n[ALERTE] GOULOT D'ÉTRANGLEMENT DÉTECTÉ !")
        print(f"Le nœud '{router.name}' est sous-dimensionné.")
        print(f"Taux de perte : {taux_perte:.1f}%")
    else:
        print(f"\n[OK] Le réseau est fluide. La file d'attente est bien dimensionnée.")
    print("="*40)

if __name__ == "__main__":
    run_interactive_simulation()
