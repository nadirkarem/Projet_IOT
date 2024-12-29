document.addEventListener('DOMContentLoaded', () => {
    const logementList = document.getElementById('logementList');

    // Charger les logements
    function loadLogements() {
        fetch("http://127.0.0.1:8000/api/logements")
            .then(response => response.json())
            .then(data => {
                logementList.innerHTML = ''; // Effacer les anciens contenus
                data.forEach(logement => {
                    // Créer une carte pour chaque logement
                    const logementCard = document.createElement('div');
                    logementCard.classList.add('col-md-6', 'col-lg-4', 'mb-4');

                    logementCard.innerHTML = `
                        <div class=" card-logement h-100 card">
                            <div class="card-body">
                                <h5 class="card-title">${logement.nom}</h5>
                                <p class="card-text">${logement.adresse}</p>
                                <p class="text-muted">Nombre de pièces : ${logement.nb_pieces}</p>
                                <button class="btn btn-success btn-sm show-details">Afficher les détails</button>
                                <div class="details mt-3" style="display: none;"></div>
                            </div>
                        </div>
                    `;

                    const button = logementCard.querySelector('.show-details');
                    const detailsDiv = logementCard.querySelector('.details');

                    // Gérer l'affichage des détails
                    button.addEventListener('click', () => {
                        if (detailsDiv.style.display === 'none') {
                            loadDetails(logement.id, detailsDiv);
                            detailsDiv.style.display = 'block';
                            button.textContent = "Masquer les détails";
                        } else {
                            detailsDiv.style.display = 'none';
                            button.textContent = "Afficher les détails";
                        }
                    });

                    logementList.appendChild(logementCard);
                });
            })
            .catch(error => console.error("Erreur lors du chargement des logements :", error));
    }

    // Charger les détails d'un logement (pièces et factures)
    function loadDetails(logementId, detailsContainer) {
        fetch(`http://127.0.0.1:8000/api/logements/${logementId}`)
            .then(response => response.json())
            .then(data => {
                let detailsHTML = '<h6>Pièces</h6><ul class="list-group">';
                data.pieces.forEach(piece => {
                    detailsHTML += `<li class="list-group-item dark-list-item">${piece.nom}</li>`;
                });
                detailsHTML += '</ul>';

                let facturesHTML = '<h6 class="mt-3">Factures</h6><ul class="list-group">';
                Object.entries(data.factures).forEach(([mois, factures]) => {
                    facturesHTML += `<li class="list-group-item fw-bold dark-list-item">${mois}</li>`;
                    factures.forEach(facture => {
                        facturesHTML += `<li class="list-group-item dark-list-item">${facture.type}: ${facture.total.toFixed(2)} €</li>`;
                    });
                });
                facturesHTML += '</ul>';

                detailsContainer.innerHTML = detailsHTML + facturesHTML;
            })
            .catch(error => console.error("Erreur lors du chargement des détails :", error));
    }

    // Charger les logements au démarrage
    loadLogements();
});
