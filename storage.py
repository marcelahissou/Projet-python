import csv
import json

def sauvegarder_csv(donnees, nom_fichier="rapport_trafic.csv"):
    """
    Sauvegarde l'historique de la simulation dans un fichier CSV.
    Idéal pour l'analyse dans Excel.
    """
    if not donnees:
        print("[Erreur] Aucune donnée à sauvegarder.")
        return

    try:
        # On récupère les clés du premier dictionnaire pour les colonnes
        colonnes = donnees[0].keys()
        
        with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(donnees)
        print(f"[Bloc 4] Rapport CSV généré avec succès : {nom_fichier}")
    except Exception as e:
        print(f"[Erreur] Impossible d'écrire le fichier CSV : {e}")

def sauvegarder_config_json(nom_noeud, capacite, nom_fichier="config_last_run.json"):
    """
    Sauvegarde la configuration du nœud pour pouvoir la réutiliser plus tard.
    """
    config = {
        "nom_du_noeud": nom_noeud,
        "capacite_file": capacite
    }
    try:
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print(f"[Bloc 4] Configuration sauvegardée en JSON : {nom_fichier}")
    except Exception as e:
        print(f"[Erreur] Impossible d'écrire le fichier JSON : {e}")
