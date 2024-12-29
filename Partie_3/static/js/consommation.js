document.addEventListener('DOMContentLoaded', () => {
    const logementSelect = document.getElementById('logementSelect');
    const chartContainer = document.getElementById('chartContainer');
    const lineChartContainer = document.getElementById('lineChartContainer');
    const toggleChartButton = document.getElementById('toggleChart');
    let currentChart = 'pie';  // État du graphique actuel (camembert)
    let currentTheme = localStorage.getItem('theme') || 'dark-mode';

    // Charger les logements dans le sélecteur
    fetch("http://127.0.0.1:8000/api/logements")
        .then(response => response.json())
        .then(logements => {
            logements.forEach(logement => {
                const option = document.createElement('option');
                option.value = logement.id;
                option.textContent = logement.nom;
                logementSelect.appendChild(option);
            });
        });

    // Afficher les graphiques lorsque le logement est sélectionné
    logementSelect.addEventListener('change', () => {
        const logementId = logementSelect.value;
        if (logementId) {
            drawPieChart(logementId);
            drawLineChart(logementId);
            chartContainer.style.display = 'block';
            lineChartContainer.style.display = 'none';
        }
    });

    // Basculer entre les graphiques
    toggleChartButton.addEventListener('click', () => {
        if (currentChart === 'pie') {
            chartContainer.style.display = 'none';
            lineChartContainer.style.display = 'block';
            toggleChartButton.textContent = 'Afficher Répartition des Factures';
            currentChart = 'line';
        } else {
            chartContainer.style.display = 'block';
            lineChartContainer.style.display = 'none';
            toggleChartButton.textContent = 'Afficher Graphique de Progression';
            currentChart = 'pie';
        }
    });

    // Dessiner le graphique en camembert
    function drawPieChart(logementId, theme = currentTheme) {
        fetch(`http://127.0.0.1:8000/api/facture-montants?id_logement=${logementId}`)
            .then(response => response.json())
            .then(data => {
                const chartData = [['Type', 'Montant']];
                data.forEach(item => {
                    chartData.push([item.type, item.montant]);
                });
    
                const dataTable = google.visualization.arrayToDataTable(chartData);
    
                // 🎨 Appliquer les couleurs selon le thème
                const textColor = theme === 'dark-mode' ? '#ffffff' : '#333333';
                const backgroundColor = theme === 'dark-mode' ? '#1e1e1e' : '#ffffff';
    
                const options = {
                    backgroundColor,  // Fond dynamique
                    legend: {
                        textStyle: { color: textColor }  // Légende
                    },
                    titleTextStyle: { color: textColor },  // Titre
                    height: 280,
                    chartArea: { width: '100%', height: '100%' }
                };
    
                const chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(dataTable, options);
            });
    }
    

    function drawLineChart(logementId, theme = currentTheme) {
        fetch(`http://127.0.0.1:8000/api/progression-mensuelle?id_logement=${logementId}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    console.warn("Aucune donnée trouvée pour ce logement.");
                    document.getElementById('linechart').innerHTML = "<p class='text-center text-warning'>Aucune donnée à afficher.</p>";
                    return;
                }
        
                const chartData = [['Mois', 'Montant']];
                data.forEach(item => {
                    chartData.push([item.mois, item.total]);
                });
    
                const dataTable = google.visualization.arrayToDataTable(chartData);
                const options = {
                    curveType: 'function',
                    backgroundColor: theme === 'dark-mode' ? '#1e1e1e' : '#ffffff',  // Fond selon le thème
                    hAxis: { 
                        textStyle: { color: theme === 'dark-mode' ? '#ffffff' : '#888888' },
                        title: 'Mois', // Titre de l'axe horizontal en blanc
                        titleTextStyle: { color: theme === 'dark-mode' ? '#ffffff' : '#888888' },
                        slantedText: true
                    },
                    vAxis: { 
                        textStyle: { color: theme === 'dark-mode' ? '#ffffff' : '#333333' },
                        title: 'Montant (€)' ,
                        titleTextStyle: { color: theme === 'dark-mode' ? '#ffffff' : '#333333' }  ,
                    },
                    // Légende
                    legend: {
                        textStyle: { 
                            color: theme === 'dark-mode' ? '#ffffff' : '#333333' 
                        }
                    },
                    height: 400,
                    chartArea: { width: '80%', height: '70%' }
                };
    
                const container = document.getElementById('linechart');
                const chart = new google.visualization.LineChart(container);
    
                setTimeout(() => {
                    chart.draw(dataTable, options);  // Dessiner avec les nouvelles options
                    console.log("Graphique dessiné !");
                }, 100);
            })
            .catch(error => {
                console.error("Erreur lors du dessin du graphique :", error);
            });
    }
    
    // Mettre à jour le graphique lors du changement de thème
    themeToggle.addEventListener('click', () => {
        const newTheme = document.body.classList.contains('dark-mode') ? 'light-mode' : 'dark-mode';
        currentTheme = newTheme;
        const logementId = document.getElementById('logementSelect').value;
        if (logementId) {
            drawLineChart(logementId, newTheme);  // Redessiner avec le nouveau thème
            drawPieChart(logementId, newTheme);  // Redessiner avec le nouveau thème
        }
    });
    
    
});
