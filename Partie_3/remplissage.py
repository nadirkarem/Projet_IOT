import sqlite3
import random
from datetime import datetime, timedelta

# Nom du fichier de la base de données
DB_PATH = "logement.db"

# Fonction pour créer les tables
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table logement (modifiée pour inclure l'adresse détaillée)
    c.execute("""
    CREATE TABLE logement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        numero TEXT NOT NULL,
        rue TEXT NOT NULL,
        code_postal TEXT NOT NULL,
        ville TEXT NOT NULL
    )
    """)

    # Table pièce
    c.execute("""
    CREATE TABLE piece (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_logement INTEGER NOT NULL,
        nom TEXT NOT NULL,
        FOREIGN KEY (id_logement) REFERENCES logement (id)
    )
    """)

    # Table type_facture
    c.execute("""
    CREATE TABLE type_facture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL
    )
    """)

    # Table type_capteur
    c.execute("""
    CREATE TABLE type_capteur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL
    )
    """)

    # Table facture
    c.execute("""
    CREATE TABLE facture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        montant REAL NOT NULL,
        id_logement INTEGER NOT NULL,
        id_type INTEGER NOT NULL,
        mois TEXT NOT NULL,
        FOREIGN KEY (id_logement) REFERENCES logement (id),
        FOREIGN KEY (id_type) REFERENCES type_facture (id)
    )
    """)

    # Table capteur_actionneur
    c.execute("""
    CREATE TABLE capteur_actionneur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        reference TEXT NOT NULL,
        port_communication TEXT NOT NULL,
        etat TEXT CHECK(etat IN ('actif', 'inactif')) DEFAULT 'actif',
        id_logement INTEGER NOT NULL,
        id_piece INTEGER NOT NULL,
        id_type INTEGER NOT NULL,
        FOREIGN KEY (id_logement) REFERENCES logement (id),
        FOREIGN KEY (id_piece) REFERENCES piece (id),
        FOREIGN KEY (id_type) REFERENCES type_capteur (id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tables créées avec succès.")

# Fonction pour insérer des données initiales
def insert_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Insérer des logements avec des adresses détaillées
    logements = [
        ("Alice Dupont", "123", "Rue Principale", "75001", "Paris"),
        ("Bob Martin", "456", "Avenue Centrale", "69002", "Lyon"),
        ("Charlie Leroy", "789", "Boulevard Sud", "13008", "Marseille"),
    ]
    c.executemany("INSERT INTO logement (nom, numero, rue, code_postal, ville) VALUES (?, ?, ?, ?, ?)", logements)

    # Récupérer les IDs des logements
    c.execute("SELECT id FROM logement")
    logement_ids = [row[0] for row in c.fetchall()]

    # Insérer des types de factures
    types_factures = [("Électricité",), ("Eau",), ("Gaz",), ("WiFi",), ("Déchets",)]
    c.executemany("INSERT INTO type_facture (nom) VALUES (?)", types_factures)

    # Insérer des types de capteurs
    types_capteurs = [("Température",), ("Humidité",), ("Lumière",)]
    c.executemany("INSERT INTO type_capteur (nom) VALUES (?)", types_capteurs)

    # Récupérer les IDs des types de factures et capteurs
    c.execute("SELECT id FROM type_facture")
    type_facture_ids = [row[0] for row in c.fetchall()]

    c.execute("SELECT id FROM type_capteur")
    type_capteur_ids = [row[0] for row in c.fetchall()]

    # Insérer des pièces pour chaque logement
    noms_pieces = ["Salon", "Chambre", "Cuisine", "Salle de bain", "Garage", "Bureau"]
    pieces = []
    for logement_id in logement_ids:
        nb_pieces = random.randint(3, 5)  # Entre 3 et 5 pièces par logement
        used_pieces = set()  # Éviter les doublons de pièces
        while len(used_pieces) < nb_pieces:
            piece = random.choice(noms_pieces)
            if piece not in used_pieces:
                used_pieces.add(piece)
                pieces.append((logement_id, piece))
    c.executemany("INSERT INTO piece (id_logement, nom) VALUES (?, ?)", pieces)

    # Récupérer les IDs des pièces
    c.execute("SELECT id, nom, id_logement FROM piece")
    piece_data = c.fetchall()

    # Insérer des capteurs pour chaque pièce
    capteurs = []
    for piece_id, piece_nom, logement_id in piece_data:
        for type_id in type_capteur_ids:
            capteur_nom = f"Capteur de {piece_nom} {random.choice(['Température', 'Humidité', 'Lumière'])}"
            capteurs.append((capteur_nom, f"Ref_{piece_id}_{type_id}", f"Port_{piece_id}_{type_id}", "actif", logement_id, piece_id, type_id))
    
    c.executemany("""
    INSERT INTO capteur_actionneur (nom, reference, port_communication, etat, id_logement, id_piece, id_type)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, capteurs)

    # Insérer des factures mensuelles pour chaque logement
    factures = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    current_date = start_date

    while current_date <= end_date:
        mois = current_date.strftime("%Y-%m")
        for logement_id in logement_ids:
            for type_id in type_facture_ids:
                montant = round(random.uniform(50, 200), 2)  # Montants aléatoires
                factures.append((montant, logement_id, type_id, mois))
        current_date += timedelta(days=30)
    c.executemany("INSERT INTO facture (montant, id_logement, id_type, mois) VALUES (?, ?, ?, ?)", factures)

    conn.commit()
    conn.close()
    print("Données insérées avec succès.")

if __name__ == "__main__":
    try:
        import os
        os.remove(DB_PATH)
        print(f"Base de données '{DB_PATH}' supprimée.")
    except FileNotFoundError:
        print(f"Aucune base de données existante trouvée sous '{DB_PATH}'.")

    # Créer les tables et insérer les données
    create_tables()
    insert_data()
