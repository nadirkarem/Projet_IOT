# Projet_IOT
# EcoLogement - Projet de Gestion de Logements et Capteurs

## Description
Ce projet permet de gérer des logements, des capteurs et de visualiser les données associées. L'application est construite en FastAPI pour le backend et utilise du HTML/CSS/JS pour le frontend.

## Prérequis
Avant de commencer, assurez-vous que votre machine dispose des éléments suivants :

- **Python** : 3.9.13  
  ```bash
  python --version
  ```
- **Pip** : 24.3.1  
  ```bash
  pip --version
  ```
- **SQLite** : 3.39.3  
  ```bash
  sqlite3 --version
  ```

---

## Installation des dépendances
Toutes les dépendances sont listées dans le fichier `requirements.txt`. Utilisez la commande suivante pour les installer :

```bash
pip install -r requirements.txt
```

### Liste des principales dépendances :
- `fastapi` (0.115.5) - Framework API
- `uvicorn` (0.32.1) - Serveur ASGI
- `sqlite3` (3.39.3) - Base de données

---

## Structure du projet
```bash
Partie_3/
│
├── static/                     # Fichiers CSS, JS et images
│   ├── css/                    # Feuilles de style
│   ├── images/                 # Images du site
│   └── js/                     # Fichiers JavaScript
│
├── templates/                  # Templates HTML
│   ├── index.html
│   ├── configuration.html
│   ├── consommation.html
│   ├── logement.html
│   └── capteurs.html
│
├── logement.db                 # Base de données SQLite (pré-remplie)
├── main.py                     # Point d'entrée d'application FastAPI
├── remplissage.py              # Remplissage de la base de données
├── requirements.txt            # Liste des dépendances Python
└── tp-4.pdf                    # Sujet du projet
```

---

## Lancement de l'application
### Étape 1 : Remplissage de la base de données
Si vous souhaitez repartir avec une nouvelle base de données (optionnel) :
```bash
python remplissage.py
```
Cela supprimera et recréera la base de données `logement.db`.

---

### Étape 2 : Démarrer le serveur
Pour lancer le serveur FastAPI, exécutez la commande suivante :
```bash
uvicorn main:app --reload
```

- **Accès au site web** : [http://localhost:8000](http://localhost:8000)  
- **Documentation API (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Fonctionnalités principales
- **Gestion des logements** : Ajout, modification et suppression de logements
- **Capteurs** : Visualisation et ajout de capteurs par pièce
- **Factures** : Ajout et suivi des factures énergétiques par mois
- **Mode clair/sombre** : Basculer entre mode clair et sombre avec un bouton

---

## Recommandations pour le professeur
1. **Si la base de données est vide** :  
   Exécutez `python remplissage.py` pour régénérer les données.

2. **Dépendances** :  
   Si des erreurs apparaissent lors de l'installation des dépendances, exécutez :
   ```bash
   pip install --upgrade pip
   ```

3. **Rapidité de test** :  
   La base de données `logement.db` fournie est déjà pré-remplie pour faciliter les tests. Libre à vous de la supprimer et de repartir à zéro.

---

## Développement et personnalisation
- **Modification du frontend** : Modifiez les fichiers HTML dans `templates/`.
- **CSS et thèmes** : Personnalisez les styles dans `static/css/style.css`.
- **AJAX et interactivité** : JavaScript dans `static/js/`.

---

Si vous rencontrez des problèmes, n'hésitez pas à me contacter.
