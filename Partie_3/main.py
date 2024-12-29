from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
import traceback  # Pour afficher plus d'infos

app = FastAPI()

# Middleware pour autoriser les requêtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modèles Pydantic
class Logement(BaseModel):
    nom: str
    numero: str
    rue: str
    code_postal: str
    ville: str

class Facture(BaseModel):
    id_logement: int
    id_type: int
    montant: float
    mois: str  # Ajout du champ mois dans le modèle Pydantic

class Capteur(BaseModel):
    nom: str
    #reference: str
    port_communication: str
    id_logement: int
    id_piece: int
    id_type: int

class Piece(BaseModel):
    id_logement: int
    nom: str

class TypeCapteur(BaseModel):
    nom: str

class Capteur(BaseModel):
    nom: str
    port_communication: str
    id_logement: int
    id_piece: int
    id_type: int

# Routes HTML
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/consommation", response_class=HTMLResponse)
async def consommation():
    with open("templates/consommation.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/capteurs", response_class=HTMLResponse)
async def capteurs():
    with open("templates/capteurs.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/configuration", response_class=HTMLResponse)
async def configuration():
    with open("templates/configuration.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())
    
@app.get("/logement", response_class=HTMLResponse)
async def logement():
    with open("templates/logement.html", "r", encoding="utf-8") as file:
        content = file.read()
        return HTMLResponse(content=content)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Print les erreurs dans la console pour débug
    print("Erreur de validation :", exc.errors())
    print("Corps reçu :", await request.json())
    
    # Retourne un message détaillé à l'utilisateur
    return JSONResponse(
        status_code=422,
        content={
            "message": "Erreur de validation",
            "details": exc.errors(),  # Détails des erreurs
            "body": await request.json()  # Données envoyées par le client
        }
    )




# API pour gérer les logements
@app.get("/api/logements")
async def get_logements():
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Modifier la requête SQL pour utiliser les nouveaux champs d'adresse
    cursor.execute("""
        SELECT 
            l.id, 
            l.nom, 
            l.numero,
            l.rue,
            l.code_postal,
            l.ville,
            COUNT(p.id) AS nb_pieces
        FROM logement l
        LEFT JOIN piece p ON l.id = p.id_logement
        GROUP BY l.id
    """)

    # Reconstituer l'adresse à partir des champs
    logements = [{
        "id": row["id"],
        "nom": row["nom"],
        "adresse": f"{row['numero']} {row['rue']}, {row['code_postal']} {row['ville']}",  # Reformater l'adresse
        "nb_pieces": row["nb_pieces"]
    } for row in cursor.fetchall()]

    conn.close()
    return logements


@app.get("/api/logements/{id_logement}")
async def get_logement_details(id_logement: int):
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Récupérer les pièces du logement
    cursor.execute("SELECT nom FROM piece WHERE id_logement = ?", (id_logement,))
    pieces = [{"nom": row["nom"]} for row in cursor.fetchall()]

    # Récupérer les factures du logement, regroupées par mois
    cursor.execute("""
        SELECT f.mois, tf.nom AS type, SUM(f.montant) AS total
        FROM facture f
        JOIN type_facture tf ON f.id_type = tf.id
        WHERE f.id_logement = ?
        GROUP BY f.mois, tf.nom
        ORDER BY f.mois
    """, (id_logement,))
    factures = {}
    for row in cursor.fetchall():
        mois = row["mois"]
        if mois not in factures:
            factures[mois] = []
        factures[mois].append({"type": row["type"], "total": row["total"]})

    conn.close()
    return {"pieces": pieces, "factures": factures}



@app.post("/api/logement")
async def add_logement(logement: Logement):
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO logement (nom, numero, rue, code_postal, ville)
        VALUES (?, ?, ?, ?, ?)
    """, (logement.nom, logement.numero, logement.rue, logement.code_postal, logement.ville))
    
    conn.commit()
    conn.close()
    print(logement.nom, logement.numero, logement.rue, logement.code_postal, logement.ville)  # Debug
    return {"message": "Logement ajouté avec succès"}

# API pour gérer les factures
@app.get("/api/factures/{id_logement}")
async def get_factures(id_logement: int):
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
    SELECT tf.nom AS type, SUM(f.montant) AS total
    FROM facture f
    JOIN type_facture tf ON f.id_type = tf.id
    WHERE f.id_logement = ?
    GROUP BY tf.nom
    """
    cursor.execute(query, (id_logement,))
    results = cursor.fetchall()
    conn.close()
    return [{"type": row["type"], "total": row["total"]} for row in results]



@app.get("/api/facture-montants")
async def get_facture_montants(id_logement: int = None):
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Requête pour regrouper les montants des factures par type
    if id_logement:
        query = """
        SELECT tf.nom AS type, SUM(f.montant) AS total
        FROM facture f
        JOIN type_facture tf ON f.id_type = tf.id
        WHERE f.id_logement = ?
        GROUP BY tf.nom
        """
        cursor.execute(query, (id_logement,))
    else:
        query = """
        SELECT tf.nom AS type, SUM(f.montant) AS total
        FROM facture f
        JOIN type_facture tf ON f.id_type = tf.id
        GROUP BY tf.nom
        """
        cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    return [{"type": row["type"], "montant": row["total"]} for row in results]

@app.post("/api/facture")
async def add_facture(facture: Facture):
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO facture (montant, id_logement, id_type, mois) VALUES (?, ?, ?, ?)",
        (facture.montant, facture.id_logement, facture.id_type, facture.mois),
    )
    conn.commit()
    conn.close()
    print(facture.montant, facture.id_logement, facture.id_type, facture.mois)  # Debug
    return {"message": "Facture ajoutée avec succès"}

# API pour gérer les capteurs
@app.get("/api/capteurs")
async def get_capteurs():
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, etat FROM capteur_actionneur")
    capteurs = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "nom": row["nom"], "etat": row["etat"]} for row in capteurs]

@app.post("/api/capteurs/{capteur_id}/toggle")
async def toggle_capteur(capteur_id: int):
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row  # Assure un retour sous forme de dictionnaire
    cursor = conn.cursor()

    # Récupérer l'état actuel du capteur
    cursor.execute("SELECT etat FROM capteur_actionneur WHERE id = ?", (capteur_id,))
    current_state = cursor.fetchone()

    if current_state is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Capteur non trouvé"}
        )

    # Basculer l'état
    new_state = "inactif" if current_state["etat"] == "actif" else "actif"

    # Mettre à jour l'état dans la base de données
    cursor.execute("UPDATE capteur_actionneur SET etat = ? WHERE id = ?", (new_state, capteur_id))
    conn.commit()

    # Rechercher le capteur mis à jour
    cursor.execute("SELECT id, nom, etat FROM capteur_actionneur WHERE id = ?", (capteur_id,))
    updated_capteur = cursor.fetchone()

    # Si aucun capteur n'est retourné (ce qui ne devrait pas arriver mais au cas où)
    if updated_capteur is None:
        conn.close()
        return JSONResponse(
            status_code=500,
            content={"error": "Erreur lors de la récupération du capteur mis à jour"}
        )

    conn.close()

    # Retourner l'état mis à jour
    return {
        "capteur": {
            "id": updated_capteur["id"],
            "nom": updated_capteur["nom"],
            "etat": updated_capteur["etat"]
        }
    }


@app.get("/api/capteurs-groupes")
async def get_capteurs_groupes():
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Requête pour récupérer les capteurs avec leurs logements et pièces
    query = """
    SELECT l.nom AS logement_nom, p.nom AS piece_nom, c.nom AS capteur_nom, c.etat, c.id
    FROM capteur_actionneur c
    JOIN piece p ON c.id_piece = p.id
    JOIN logement l ON c.id_logement = l.id
    ORDER BY l.nom, p.nom, c.nom
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Regrouper les résultats par logement et par pièce
    logements = {}
    for row in results:
        logement_nom = row["logement_nom"]
        piece_nom = row["piece_nom"]

        if logement_nom not in logements:
            logements[logement_nom] = {}

        if piece_nom not in logements[logement_nom]:
            logements[logement_nom][piece_nom] = []

        logements[logement_nom][piece_nom].append({
            "id": row["id"],
            "nom": row["capteur_nom"],
            "etat": row["etat"],
        })

    # Structurer les données pour le frontend
    response = []
    for logement_nom, pieces in logements.items():
        response.append({
            "nom": logement_nom,
            "pieces": [
                {
                    "nom": piece_nom,
                    "capteurs": capteurs
                } for piece_nom, capteurs in pieces.items()
            ]
        })

    return response

# API pour gérer les types de factures
@app.get("/api/logements/{id_logement}/pieces")
async def get_pieces_par_logement(id_logement: int):
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM piece WHERE id_logement = ?", (id_logement,))
    pieces = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "nom": row["nom"]} for row in pieces]

@app.get("/api/types-facture")
async def get_types_facture():
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM type_facture")
    types_facture = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "nom": row["nom"]} for row in types_facture]

@app.post("/api/type-facture")
async def add_type_facture(request: Request):
    body = await request.json()  # Lire le JSON du body
    type_nom = body.get("nom")

    if not type_nom:
        return {"error": "Le nom du type de facture est requis"}, 400
    
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO type_facture (nom) VALUES (?)
    """, (type_nom,))

    conn.commit()
    conn.close()
    return {"message": "Type de facture ajouté avec succès"}

@app.put("/api/type-facture/{type_id}")
async def update_type_facture(type_id: int, request: Request):
    body = await request.json()
    new_nom = body.get("nom")

    if not new_nom:
        return {"error": "Le nom du type de facture est requis"}, 400
    
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE type_facture
        SET nom = ?
        WHERE id = ?
    """, (new_nom, type_id))

    conn.commit()
    conn.close()
    return {"message": "Type de facture mis à jour avec succès"}

@app.delete("/api/type-facture/{type_id}")
async def delete_type_facture(type_id: int):
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM type_facture WHERE id = ?", (type_id,))
    conn.commit()
    conn.close()

    return {"message": "Type de facture supprimé avec succès"}




@app.post("/api/piece")
async def add_piece(piece: Piece):
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO piece (id_logement, nom) VALUES (?, ?)", (piece.id_logement, piece.nom))
    conn.commit()
    conn.close()
    #print les informations de la pièce
    print(piece.id_logement)
    print(piece.nom)
    return {"message": "Pièce ajoutée avec succès"}

@app.post("/api/type-capteur")
async def add_type_capteur(type_capteur: TypeCapteur):
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO type_capteur (nom) VALUES (?)", (type_capteur.nom,))
    conn.commit()
    conn.close()
    return {"message": "Type de capteur ajouté avec succès"}

@app.get("/api/types-capteur")
async def get_types_capteur():
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM type_capteur")
    types_capteur = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "nom": row["nom"]} for row in types_capteur]

@app.post("/api/capteur")
async def add_capteur(capteur: Capteur, request: Request):
    body = await request.json()  # Lire le body brut
    print("Données reçues :", body)
    print("Données validées (Pydantic) :", capteur)
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()
    reference = f"Ref_{capteur.id_piece}_{capteur.id_type}"
    cursor.execute("""
        INSERT INTO capteur_actionneur (nom, reference, port_communication, etat, id_logement, id_piece, id_type)
        VALUES (?, ?, ?, 'actif', ?, ?, ?)
    """, (capteur.nom, reference, capteur.port_communication, capteur.id_logement, capteur.id_piece, capteur.id_type))
    
    conn.commit()
    conn.close()
    return {"message": "Capteur ajouté avec succès"}

@app.post("/api/facture")
async def add_facture(facture: Facture):
    conn = sqlite3.connect("logement.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO facture (montant, id_logement, id_type, mois) VALUES (?, ?, ?, ?)",
        (facture.montant, facture.id_logement, facture.id_type, facture.mois),
    )
    conn.commit()
    conn.close()
    print(facture.montant, facture.id_logement, facture.id_type, facture.mois)  # Debug
    return {"message": "Facture ajoutée avec succès"}

@app.get("/api/progression-mensuelle")
async def get_progression_mensuelle(id_logement: int):
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT mois, SUM(montant) AS total
        FROM facture
        WHERE id_logement = ? AND mois IS NOT NULL
        GROUP BY mois
        ORDER BY mois;
    """
    cursor.execute(query, (id_logement,))
    results = cursor.fetchall()
    conn.close()

    # Debugging print
    print("Résultats progression mensuelle :", results)
    print("Résultat brut :", results)
    for row in results:
        print("Ligne :", dict(row))

    
    return [{"mois": row["mois"], "total": row["total"]} for row in results]
