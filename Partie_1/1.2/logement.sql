TIMESTAMP DEFAULT CURRENT_TIMESTAMP

-- Qst 2 : Suppression de toutes les tables de la base de données
DROP TABLE IF EXISTS logement;
DROP TABLE IF EXISTS piece;
DROP TABLE IF EXISTS capteur_actionneur;
DROP TABLE IF EXISTS type_capteur_actionneur;
DROP TABLE IF EXISTS mesure;
DROP TABLE IF EXISTS facture;

-- Qst 3 : Création des tables de la base de données
-- Création de la table 'logement'
CREATE TABLE logement (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,
    numero_telephone TEXT,
    adresse_ip TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table 'piece'
CREATE TABLE piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    coordonnee_x INTEGER,
    coordonnee_y INTEGER,
    coordonnee_z INTEGER,
    id_logement INTEGER,
    FOREIGN KEY (id_logement) REFERENCES logement(id_logement)
);

-- Création de la table 'type_capteur_actionneur'
CREATE TABLE type_capteur_actionneur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    unite_mesure TEXT,
    plage_precision TEXT
);

-- Création de la table 'capteur_actionneur'
CREATE TABLE capteur_actionneur (
    id_capteur INTEGER PRIMARY KEY AUTOINCREMENT, -- ID généré automatiquement
    reference TEXT NOT NULL,
    port_communication TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_piece INTEGER,
    id_type INTEGER,
    FOREIGN KEY (id_piece) REFERENCES piece(id_piece),
    FOREIGN KEY (id_type) REFERENCES type_capteur_actionneur(id_type)
);

-- Création de la table 'mesure'
CREATE TABLE mesure (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    valeur REAL NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_capteur INTEGER,
    FOREIGN KEY (id_capteur) REFERENCES capteur_actionneur(id_capteur)
);

-- Création de la table 'facture'
CREATE TABLE facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    date TIMESTAMP,
    montant REAL,
    valeur_consomme REAL,
    id_logement INTEGER,
    FOREIGN KEY (id_logement) REFERENCES logement(id_logement)
);

-- Insertion de données dans les tables

-- Qst 4 : Insertion de données de pièces

-- Insertion d'un logement, ce logement sera associé à quatre pièces.
INSERT INTO logement (adresse, numero_telephone, adresse_ip) VALUES 
('3, rue Bani Ouriaghel', '0661221310', '192.168.1.10');

-- Récupération de l'id du logement pour l'associer aux pièces
-- Ici, on suppose que l'ID généré automatiquement est le dernier inséré
-- Si l'ID est généré autrement, adapte la commande en conséquence.

-- Insertion des pièces du logement
-- Chaque pièce est nommée et localisée dans une matrice 3D (x, y, z).
INSERT INTO piece (nom, coordonnee_x, coordonnee_y, coordonnee_z, id_logement) VALUES 
('Salon', 0, 0, 0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1)),
('Cuisine', 1, 0, 0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1)),
('Chambre', 0, 1, 0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1)),
('Salle de bain', 1, 1, 0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1));

-- Qst 5 : Insertion de données de type apteurs/actionneurs
-- Chaque type a un nom, une unité de mesure et une plage de précision.

INSERT INTO type_capteur_actionneur (type, unite_mesure, plage_precision) VALUES 
('Température', '°C', '-40 à 125'),
('Luminosité', 'lux', '0 à 10000'),
('Consommation électrique', 'kWh', '0 à 10000'),
('Niveau eau', 'litres', '0 à 500');

-- Qst 6 : Insertion de capteurs/actionneurs
-- Chaque capteur/actionneur est associé à un type, une pièce, et un port de communication.

INSERT INTO capteur_actionneur (reference, port_communication, id_piece, id_type) VALUES 
('Capteur_Temperature_1', 'COM1', (SELECT id_piece FROM piece WHERE nom = 'Salon' LIMIT 1), (SELECT id_type FROM type_capteur_actionneur WHERE type = 'Température' LIMIT 1)),
('Capteur_Luminosite_1', 'COM2', (SELECT id_piece FROM piece WHERE nom = 'Cuisine' LIMIT 1), (SELECT id_type FROM type_capteur_actionneur WHERE type = 'Luminosité' LIMIT 1));

-- Qst 7 : Insertion de mesures

-- Mesures pour le capteur de température dans le Salon
INSERT INTO mesure (valeur, id_capteur) VALUES 
(22.5, (SELECT id_capteur FROM capteur_actionneur WHERE reference = 'Capteur_Temperature_1' LIMIT 1)),
(23.1, (SELECT id_capteur FROM capteur_actionneur WHERE reference = 'Capteur_Temperature_1' LIMIT 1));

-- Mesures pour le capteur de luminosité dans la Cuisine
INSERT INTO mesure (valeur, id_capteur) VALUES 
(300.0, (SELECT id_capteur FROM capteur_actionneur WHERE reference = 'Capteur_Luminosite_1' LIMIT 1)),
(320.5, (SELECT id_capteur FROM capteur_actionneur WHERE reference = 'Capteur_Luminosite_1' LIMIT 1));

-- Qst 8 : Insertion de factures

INSERT INTO facture (type, date, montant, valeur_consomme, id_logement) VALUES 
('Électricité', '2024-01-15', 75.50, 300.0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1)),
('Eau', '2024-01-15', 30.00, 25.0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1)),
('Déchets', '2024-02-15', 15.00, 50.0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1)),
('Électricité', '2024-02-15', 80.00, 320.0, (SELECT id_logement FROM logement ORDER BY id_logement DESC LIMIT 1));


