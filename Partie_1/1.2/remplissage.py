import sqlite3
import random
from datetime import datetime, timedelta

# Ouverture/initialisation de la base de données
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Source code suivant:
    # Crée une fonction Python pour insérer des mesures et des factures aléatoires dans une base de données SQLite. 
    # La fonction d'insertion des mesures doit commencer par récupérer tous les identifiants des capteurs depuis la table capteur_actionneur. 
    # Pour chaque capteur, elle doit ajouter deux mesures aléatoires avec des valeurs comprises entre 10 et 30, arrondies à deux décimales. 
    # Les dates d'insertion doivent être aléatoires dans les 30 derniers jours, générées avec datetime.now() et timedelta. Les mesures doivent être insérées dans la table mesure avec les champs valeur, date_insertion et id_capteur.

    # La fonction d'insertion des factures doit récupérer tous les identifiants des logements depuis la table logement. 
    # Pour chaque logement, elle doit générer quatre factures avec un type choisi aléatoirement parmi Électricité, Eau et Déchets.
    # La date de la facture doit être dans les 60 derniers jours, avec des montants aléatoires entre 20 et 100 euros, arrondis à deux décimales.
    # Un champ valeur_consomme doit être ajouté avec des valeurs comprises entre 50 et 500. Les factures doivent être insérées dans la table facture avec les champs type, date, montant, valeur_consomme et id_logement. 
    # Les requêtes SQL doivent utiliser des paramètres sécurisés avec execute() pour éviter les injections SQL.
    
# Fonction pour insérer des mesures pour chaque capteur
def ajouter_mesures():
    c.execute('SELECT id_capteur FROM capteur_actionneur')
    capteurs = [row['id_capteur'] for row in c.fetchall()]

    for id_capteur in capteurs:
        for _ in range(2):  # Ajouter deux mesures par capteur
            valeur = round(random.uniform(10, 30), 2)  # Valeurs aléatoires entre 10 et 30
            date_insertion = datetime.now() - timedelta(days=random.randint(1, 30))
            c.execute("INSERT INTO mesure (valeur, date_insertion, id_capteur) VALUES (?, ?, ?)", 
                      (valeur, date_insertion.strftime('%Y-%m-%d %H:%M:%S'), id_capteur))

# Fonction pour insérer des factures pour le logement
def ajouter_factures():
    c.execute('SELECT id_logement FROM logement')
    logements = [row['id_logement'] for row in c.fetchall()]

    for id_logement in logements:
        types_factures = ['Électricité', 'Eau', 'Déchets']
        for _ in range(4):  # Ajouter quatre factures par logement
            type_facture = random.choice(types_factures)
            date_facture = datetime.now() - timedelta(days=random.randint(1, 60))
            montant = round(random.uniform(20, 100), 2)  # Montant aléatoire entre 20 et 100
            valeur_consomme = round(random.uniform(50, 500), 2)  # Consommation aléatoire entre 50 et 500
            c.execute("INSERT INTO facture (type, date, montant, valeur_consomme, id_logement) VALUES (?, ?, ?, ?, ?)", 
                      (type_facture, date_facture.strftime('%Y-%m-%d'), montant, valeur_consomme, id_logement))

# Appels des fonctions pour ajouter les données
ajouter_mesures()
ajouter_factures()

# Lecture des données pour vérification
c.execute('SELECT * FROM mesure')
print("Mesures insérées :")
print(c.fetchall())

c.execute('SELECT * FROM facture')
print("Factures insérées :")
print(c.fetchall())

# Fermeture de la connexion
conn.commit()
conn.close()
