import sqlite3
import random
from datetime import datetime, timedelta

# Ouverture/initialisation de la base de données
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

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
