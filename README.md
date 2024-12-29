# Projet_IOT
# EcoLogement - Projet de Gestion de Logements et Capteurs

## Description
Ce projet permet de gérer des logements, des capteurs et de visualiser les données associées. L'application est construite en FastAPI pour le backend et utilise du HTML/CSS/JS pour le frontend.

## Table des Matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Structure du Projet](#structure-du-projet)
4. [Détails des Parties](#détails-des-parties)
5. [Lancement du Projet](#lancement-du-projet)
6. [Fonctionnalités Clés](#fonctionnalités-clés)


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
Projet_IOT/
│
├── partie1/                   # Partie 1 - Base de données
│   ├── logement.sql            # Création des tables et insertion des données
│   └── remplissage.py          # Remplissage des données avec Python
│
├── partie2/                   # Partie 2 - Serveur RESTful
│   ├── serveur.py              # Serveur FastAPI pour les requêtes REST
│   └── remplissage.py          # API de remplissage avec POST/GET
│
├── partie3/                   # Partie 3 - Application Web
│   ├── static/                 # Fichiers CSS, JS et images
│   │   ├── css/                # Feuilles de style
│   │   ├── images/             # Images du site
│   │   └── js/                 # Fichiers JavaScript
│   │
│   ├── templates/              # Templates HTML
│   │   ├── index.html
│   │   ├── configuration.html
│   │   ├── consommation.html
│   │   ├── logement.html
│   │   └── capteurs.html
│   │
│   ├── logement.db             # Base de données SQLite (pré-remplie)
│   ├── main.py                 # Point d'entrée FastAPI pour l'application web
│   └── tp-4.pdf                # Sujet du TP complet

```

## Lancement de l'application
### Étape 1 : Remplissage de la base de données
Si vous souhaitez repartir avec une nouvelle base de données (optionnel) :
```bash
python remplissage.py
```
Cela supprimera et recréera la base de données `logement.db`.



### Étape 2 : Démarrer le serveur
Pour lancer le serveur FastAPI, exécutez la commande suivante :
```bash
uvicorn main:app --reload
```

- **Accès au site web** : [http://localhost:8000](http://localhost:8000)  

Voici une mise à jour détaillée du README en tenant compte de toutes les parties du projet (Partie 1, Partie 2 et Partie 3). J'ai également ajouté des détails sur le mode nuit/jour et la structure du projet.


## Détails des Parties
### Partie 1 - Base de Données
- **Objectif** : Création et remplissage de la base de données `logement.db` pour stocker les logements, capteurs/actionneurs, mesures et factures.
- **Fichier** : `logement.sql` (création des tables, types de capteurs et exemples de mesures)
- **Complément** : `remplissage.py` insère des données initiales et simule des mesures régulières.

### Partie 2 - Serveur RESTful
- **Objectif** : Développement du serveur REST avec FastAPI permettant la manipulation des données via des requêtes GET et POST.
- **Exercices** :
  - **Exercice 1** : Remplissage via API REST (`remplissage.py`)
  - **Exercice 2** : Génération de graphiques interactifs (Google Charts)
  - **Exercice 3** : Intégration d'une API météo
  - **Exercice 4** : Utilisation des capteurs et actionneurs pour agir sur les logements

### Partie 3 - Application Web
- **Objectif** : Création de l'interface utilisateur pour la visualisation et la gestion des capteurs, logements et consommations.
- **Fonctionnalités** :
  - **Visualisation des consommations** (graphiques interactifs)
  - **Gestion des capteurs** (activation/désactivation)
  - **Ajout de nouveaux capteurs/logements**
  - **Mode nuit/jour** : Bouton interactif permettant de basculer entre mode clair et sombre.



## Fonctionnalités principales
- **Gestion des logements** : Ajout, modification et suppression de logements
- **Capteurs** : Visualisation et ajout de capteurs par pièce
- **Factures** : Ajout et suivi des factures énergétiques par mois
- **Mode clair/sombre** : Basculer entre mode clair et sombre avec un bouton
- **Responsive Design** : Le site utilise Bootstrap pour une compatibilité maximale avec les différents appareils (PC, tablette, mobile).
- **Graphiques Dynamiques** : Les consommations énergétiques sont affichées sous forme de graphiques interactifs (Google Charts).


## Recommandations pour le professeur
1. **Si la base de données est vide** :  
   Exécutez `python remplissage.py` pour régénérer les données.

2. **Rapidité de test** :  
   La base de données `logement.db` fournie est déjà pré-remplie pour faciliter les tests. Libre à vous de la supprimer et de repartir à zéro.


3. **En cas de bug** :
   En cas de bug par exemple, un graphique qui ne s'affiche pas, veuillez essayer de tout simplement passer du mode nuit au mode jour et/ou inversement à partir du bouton situé    au coin supérieur droite.

## Développement et personnalisation
- **Modification du frontend** : Modifiez les fichiers HTML dans `templates/`.
- **CSS et thèmes** : Personnalisez les styles dans `static/css/style.css`.
- **AJAX et interactivité** : JavaScript dans `static/js/`.

## Remarque sur le Plagiat et l'Utilisation de l'IA

Ce projet est personnel, et j'encourage toute personne à s'en inspirer ou à réutiliser le code si nécessaire. Toutefois, je tiens à préciser que certains segments de code ont été générés avec l'aide d'une intelligence artificielle (ChatGPT). Chaque fois que du code a été généré par l'IA, cela a été clairement sourcé sous forme de commentaires avec des prompts appropriés.

Je n'ai utilisé aucun code provenant de plateformes comme Stack Overflow ou d'autres sites similaires. Les prompts fournis dans les commentaires sont susceptibles de générer du code similaire, mais les résultats exacts peuvent varier en fonction :

des fichiers ou du contexte partagé avec l'IA,
des discussions et itérations faites au fil du temps,
des ajustements manuels et personnalisations spécifiques au projet.
Ainsi, il est peu probable que quelqu'un obtienne exactement le même résultat en utilisant uniquement les prompts, sans avoir accès au contexte et aux données associées à ce projet.

Je reste disponible pour toute clarification sur les choix techniques ou l'origine des différentes parties du code.
