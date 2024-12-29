document.addEventListener('DOMContentLoaded', () => {
    const sensorList = document.getElementById('sensorList');

    // Charger les capteurs regroupés par logement et pièce
    function loadSensors() {
        fetch("http://127.0.0.1:8000/api/capteurs-groupes")
            .then(response => response.json())
            .then(data => {
                sensorList.innerHTML = ''; // Effacer les anciennes données
                
                data.forEach(logement => {
                    console.log(logement);  // Vérifier les données reçues

                    const col = document.createElement('div');
                    col.classList.add('col-md-6', 'mb-4');

                    let nbPieces = logement.pieces ? logement.pieces.length : 0;
                    let imgSrc = `/static/images/${nbPieces}_piece.jpg`;
                    if (nbPieces > 7) {
                        imgSrc = `/static/images/6_piece.jpg`;
                    }


                    col.innerHTML = `
                        <div class="card card-capteur h-100">
                            <img src="${imgSrc}" alt="Plan du logement">
                            <div class="card-body">
                                <h5 class="card-title">${logement.nom}</h5>
                                <p class="text-muted">Nombre de pièces : ${nbPieces}</p>
                                <ul class="list-group capteur-list mt-3">
                                    ${logement.pieces.map(piece => `
                                        <li class="list-group-item">
                                            <strong>${piece.nom}</strong>
                                            <ul class="list-group mt-2">
                                                ${piece.capteurs.map(sensor => `
                                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                                        ${sensor.nom}
                                                        <button class="btn toggle-button ${sensor.etat === 'actif' ? 'btn-success' : 'btn-danger'}">
                                                            ${sensor.etat === 'actif' ? 'On' : 'Off'}
                                                        </button>
                                                    </li>
                                                `).join('')}
                                            </ul>
                                        </li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                    `;

                    sensorList.appendChild(col);

                    // Ajouter les événements toggle pour chaque bouton de capteur
                    col.querySelectorAll('.toggle-button').forEach((button, index) => {
                        button.addEventListener('click', () => {
                            const sensorId = logement.pieces
                                .flatMap(piece => piece.capteurs)[index].id;
                            toggleSensorState(sensorId, button);
                        });
                    });
                });
            })
            .catch(error => console.error("Erreur lors du chargement des capteurs :", error));
    }

    // Changer l'état d'un capteur
    function toggleSensorState(sensorId, button) {
        const newState = button.textContent === 'Actif' ? 'inactif' : 'actif';
        
        fetch(`http://127.0.0.1:8000/api/capteurs/${sensorId}/toggle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ etat: newState })
        })
        .then(response => response.json())
        .then(data => {
            if (data.capteur) {
                // Met à jour dynamiquement l'état du capteur avec la réponse de l'API
                button.textContent = data.capteur.etat === 'actif' ? 'Actif' : 'Inactif';
                button.classList.toggle('btn-success', data.capteur.etat === 'actif');
                button.classList.toggle('btn-danger', data.capteur.etat === 'inactif');
                } 
                else {
                console.error("Erreur lors de la mise à jour de l'état du capteur :", data.error);                
            } 
        })
        .catch(error => {
            console.error("Erreur lors de la mise à jour de l'état du capteur :", error);
        });
    }



    // Charger les capteurs au démarrage
    loadSensors();
});
