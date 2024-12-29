from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import urllib.parse
import json
import http.server
import socketserver
import threading
import requests
import random
import time

# Exemple de commande pour tester les requêtes HTTP :
# curl -X POST -H "Content-Type: application/json" -d '{"valeur": 25.5, "id_capteur": 1}' http://localhost:8888/mesures
# curl -X POST -H "Content-Type: application/json" -d '{"valeur":
# 25.5, "id_capteur": 1}' http://localhost:8888/mesures
# curl -X GET http://localhost:8888/mesures
# curl -X GET http://localhost:8888/factures
# curl -X POST -H "Content-Type: application/json" -d '{"type": "Eau", "date": "2021-01-01", "montant": 50.5, "valeur_consomme": 100, "id_logement": 1}' http://localhost:8888/factures
# curl -X GET http://localhost:8888/factures/chart
# curl -X GET http://localhost:8888/meteo
# curl -X GET http://localhost:8888/meteo/1

# Sources des codes suivants:
    # Exercice 1 – Gestion des Requêtes HTTP avec SQLite (Mesures et Factures)
        # "Écris moi un code de base de structure d'un serveur HTTP en Python avec http.server qui peut gérer des requêtes GET et POST pour interagir avec une base de données SQLite. 
        # Laisse moi des trous pour que j'implémente des routes pour ajouter et récupérer des mesures de capteurs et des factures mais je veux la ligne nécessaire pour que lorsqu'une mesure est ajoutée, on insère automatiquement la date d'insertion. 
        # Pour les factures, insère des données comme le type, la date, le montant et la consommation associée."
    # Exercice 2 – Générer un Graphique avec Google Charts
        # "Développe une route Python qui affiche une page HTML contenant un graphique Google Charts.
        # Le graphique doit être généré à partir des données d'une table facture dans une base de données SQLite, et représenter la répartition des montants par type de facture (électricité, eau, etc.). 
        # Le serveur doit répondre sur /factures/chart et afficher dynamiquement les données sous forme de camembert."
    # Exercice 3 – Intégration de l'API OpenWeatherMap
        # "Ajoute une route Python qui interroge l'API OpenWeatherMap pour obtenir les prévisions météo de la ville de Paris. 
        # La route doit répondre sur /meteo, et on doit retourner la date, la température et la description de la météo."
    # Exercice 4 – Simulation de Capteur DHT
        # "Implémente une simulation de capteur DHT en Python avec un thread qui met à jour périodiquement la température et l'humidité. 
        # Crée les classes dont j'aurai besoin qui génereront des valeurs aléatoires de température et d'humidité toutes les 5 secondes.

DB_PATH = "logement.db"

class MyHandler(BaseHTTPRequestHandler):
    # Gérer une requête GET
    def do_GET(self):
        try:
            # Parsing de l'URI
            parsed_path = urllib.parse.urlparse(self.path)
            if parsed_path.path == '/mesures':
                self._get_mesures()
            elif parsed_path.path == '/factures':
                self._get_factures()
            elif parsed_path.path == '/factures/chart':
                self._generate_chart()
            elif parsed_path.path == '/meteo':
                self._get_weather()
            else:
                self._send_response(404, {"error": "Ressource non trouvée"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    # Gérer une requête POST
    def do_POST(self):
        try:
            # Parsing de l'URI
            parsed_path = urllib.parse.urlparse(self.path)
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            if parsed_path.path == '/mesures':
                self._add_mesure(data)
            elif parsed_path.path == '/factures':
                self._add_facture(data)
            else:
                self._send_response(404, {"error": "Ressource non trouvée"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    # Méthode pour récupérer les mesures
    def _get_mesures(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        mesures = c.execute("SELECT * FROM mesure").fetchall()
        conn.close()
        self._send_response(200, [dict(row) for row in mesures])

    # Méthode pour récupérer les factures
    def _get_factures(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        factures = c.execute("SELECT * FROM facture").fetchall()
        conn.close()
        self._send_response(200, [dict(row) for row in factures])

    # Méthode pour ajouter une mesure
    def _add_mesure(self, data):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO mesure (valeur, date_insertion, id_capteur) VALUES (?, datetime('now'), ?)",
            (data['valeur'], data['id_capteur'])
        )
        conn.commit()
        conn.close()
        self._send_response(201, {"status": "Mesure ajoutee"})

    # Méthode pour ajouter une facture
    def _add_facture(self, data):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO facture (type, date, montant, valeur_consomme, id_logement) VALUES (?, ?, ?, ?, ?)",
            (data['type'], data['date'], data['montant'], data['valeur_consomme'], data['id_logement'])
        )
        conn.commit()
        conn.close()
        self._send_response(201, {"status": "Facture ajoutee"})

    # Exercice 2

    # Générer une page HTML avec le graphique
    def _generate_chart(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Récupérer les données des factures
        factures = c.execute("SELECT type, SUM(montant) as total FROM facture GROUP BY type").fetchall()
        conn.close()

        # Construire les données pour Google Charts
        chart_data = [["Type", "Montant"]]
        for facture in factures:
            chart_data.append([facture["type"], float(facture["total"])])

        # Générer le HTML avec le graphique
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Graphique des Factures</title>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart']}});
                google.charts.setOnLoadCallback(drawChart);

                function drawChart() {{
                    var data = google.visualization.arrayToDataTable({json.dumps(chart_data)});

                    var options = {{
                        title: 'Repartition des Montants des Factures'
                    }};

                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

                    chart.draw(data, options);
                }}
            </script>
        </head>
        <body>
            <h1>Graphique des Factures</h1>
            <div id="piechart" style="width: 900px; height: 500px;"></div>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    # Exercice 3
    API_KEY = "0880882e775157593161ee2975cb1bfc"  # Clé API OpenWeatherMap
    BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

    # Méthode pour obtenir les prévisions météo
    def _get_weather(self):
        # Paramètres de la requête à l'API météo
        params = {
            'q': 'Paris',  # Ville pour laquelle on veut la météo
            'appid': self.API_KEY,
            'units': 'metric',
            'lang': 'fr'
        }

        # Requête à l'API
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extraire les prévisions pertinentes
            forecasts = []
            for forecast in data['list'][:5]:  # Les 5 prochaines prévisions
                forecasts.append({
                    "datetime": forecast['dt_txt'],
                    "temperature": forecast['main']['temp'],
                    "description": forecast['weather'][0]['description']
                })

            # Répondre avec les données météo
            self._send_response(200, forecasts)
        else:
            self._send_response(500, {"error": "Erreur API meteo"})

    # Méthode générique pour envoyer une réponse
    def _send_response(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

# Exercice 4: Simulation de capteur DHT et multi-Threading comme demandé 
# par le prof de TD plutôt que l'utilisation d'ESP qui n'étaient pas disponibles

# Class pour la simulation DHT dans un thread 
class DHTThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.temperature = 22.8
        self.humidity = 58.0

    def run(self):
        while True:
            self.temperature += random.uniform(-0.5, 0.5)
            self.humidity += random.uniform(-2, 2)
            self.temperature = max(0, min(self.temperature, 40))
            self.humidity = max(0, min(self.humidity, 100))
            time.sleep(5)

# Start les serveurs
def start_servers():
    # Ports pour les serveurs
    HTTP_SERVER_PORT = 8888
    DHT_SERVER_PORT = 1883

    # Serveur HTTP principal
    http_server = HTTPServer(("localhost", HTTP_SERVER_PORT), MyHandler)

    # Serveur HTTP pour les données DHT
    dht_server = HTTPServer(("localhost", DHT_SERVER_PORT), DHTHandler)

    # Simulation du capteur DHT dans un thread
    global dht_thread
    dht_thread = DHTThread()
    dht_thread.start()

    # Threads pour les serveurs HTTP
    http_thread = threading.Thread(target=http_server.serve_forever)
    dht_thread_http = threading.Thread(target=dht_server.serve_forever)

    http_thread.start()
    dht_thread_http.start()

    print(f"Serveur HTTP démarré sur le port {HTTP_SERVER_PORT}")
    print(f"Serveur DHT démarré sur le port {DHT_SERVER_PORT}")

    try:
        http_thread.join()
        dht_thread_http.join()
    except KeyboardInterrupt:
        print("Arrêt des serveurs")
        http_server.shutdown()
        dht_server.shutdown()

# Class pour le serveur DHT
class DHTHandler(BaseHTTPRequestHandler):
    # Méthode GET pour récupérer les données simulées du capteur DHT
    def do_GET(self):
        try:
            # Données simulées de température et d'humidité
            data = {
                "temperature": dht_thread.temperature,
                "humidity": dht_thread.humidity
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


# Start the program
if __name__ == "__main__":
    start_servers()

