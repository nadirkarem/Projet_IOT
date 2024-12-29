document.addEventListener('DOMContentLoaded', () => {
    const addLogementForm = document.getElementById('addLogementForm');
    const addPieceForm = document.getElementById('addPieceForm');
    const addCapteurForm = document.getElementById('addCapteurForm');
    const addFactureForm = document.getElementById('addFactureForm');
    const addFactureTypeButton = document.getElementById('addFactureType');
    const addTypeCapteurBtn = document.getElementById('addTypeCapteurBtn');  // <- Bouton pour ajouter un type de capteur
    const capteurTypeSelect = document.getElementById('capteurType');  // <- Sélecteur pour le type de capteur

    const logementPieceSelect = document.getElementById('logementPiece');
    const capteurLogementSelect = document.getElementById('capteurLogement');
    const capteurPieceSelect = document.getElementById('capteurPiece');
    const factureLogementSelect = document.getElementById('factureLogement');
    const factureTypeSelect = document.getElementById('factureType');

    // Charger les logements pour les formulaires
    function loadLogementsForSelects() {
        fetch("http://127.0.0.1:8000/api/logements")
            .then(response => response.json())
            .then(data => {
                logementPieceSelect.innerHTML = '<option value="" disabled selected>Choisir un logement</option>';
                capteurLogementSelect.innerHTML = '<option value="" disabled selected>Choisir un logement</option>';
                factureLogementSelect.innerHTML = '<option value="" disabled selected>Choisir un logement</option>';
                data.forEach(logement => {
                    const option = document.createElement('option');
                    option.value = logement.id;
                    option.textContent = logement.nom;
                    logementPieceSelect.appendChild(option);
                    capteurLogementSelect.appendChild(option.cloneNode(true));
                    factureLogementSelect.appendChild(option.cloneNode(true));
                });
            })
            .catch(error => console.error("Erreur lors du chargement des logements :", error));
    }

    // Charger les pièces pour les capteurs
    function loadPiecesForCapteurs(logementId) {
        fetch(`http://127.0.0.1:8000/api/logements/${logementId}/pieces`)
            .then(response => response.json())
            .then(data => {
                capteurPieceSelect.innerHTML = '<option value="" disabled selected>Choisir une pièce</option>';
                data.forEach(piece => {
                    const option = document.createElement('option');
                    option.value = piece.id;
                    option.textContent = piece.nom;
                    capteurPieceSelect.appendChild(option);
                });
            })
            .catch(error => console.error("Erreur lors du chargement des pièces :", error));
    }

    // Charger les types de factures
    function loadFactureTypes() {
        fetch("http://127.0.0.1:8000/api/types-facture")
            .then(response => response.json())
            .then(data => {
                factureTypeSelect.innerHTML = '<option value="" disabled selected>Choisir un type</option>';
                data.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type.id;
                    option.textContent = type.nom;
                    factureTypeSelect.appendChild(option);
                });
            })
            .catch(error => console.error("Erreur lors du chargement des types de facture :", error));
    }

    // Charger les types de capteurs
    function loadTypesCapteur() {
        fetch("http://127.0.0.1:8000/api/types-capteur")
            .then(response => response.json())
            .then(data => {
                capteurTypeSelect.innerHTML = '<option value="" disabled selected>Choisir un type</option>';
                data.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type.id;
                    option.textContent = type.nom;
                    capteurTypeSelect.appendChild(option);
                });
            })
            .catch(error => console.error("Erreur lors du chargement des types de capteur :", error));
    }

    // Ajouter un logement
    if (addLogementForm) {
        addLogementForm.addEventListener('submit', function (e) {
            e.preventDefault();
            
            const nom = document.getElementById('nomLogement').value;
            const numero = document.getElementById('numero').value;
            const rue = document.getElementById('rue').value;
            const code_postal = document.getElementById('code_postal').value;
            const ville = document.getElementById('ville').value;
        
            fetch("http://127.0.0.1:8000/api/logements", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    nom: nom,
                    numero: numero,
                    rue: rue,
                    code_postal: code_postal,
                    ville: ville
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadLogementsForSelects();  // Rafraîchir les logements après ajout
            })
            .catch(error => console.error("Erreur :", error));
        });
        
    }

    // Ajouter un capteur
    if (addCapteurForm) {
        addCapteurForm.addEventListener('submit', function (e) {
            e.preventDefault();
            console.log("Soumission du formulaire détectée !");
            
            const logementId = capteurLogementSelect.value;
            const pieceId = capteurPieceSelect.value;
            const nom = document.getElementById('capteurNom').value;
            const port = document.getElementById('capteurPort').value;
            const typeId = capteurTypeSelect.value;

            console.log({ logementId, pieceId, nom, port, typeId });

            fetch("http://127.0.0.1:8000/api/capteur", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id_logement: logementId,
                    id_piece: pieceId,
                    nom: nom,
                    port_communication: port,
                    id_type: typeId,
                    reference: "1"
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Réponse de l'API :", data);
                alert(data.message);
            })
            .catch(error => console.error("Erreur :", error));
        });
    }

    // Ajouter un type de capteur via le bouton "+"
    if (addTypeCapteurBtn) {
        addTypeCapteurBtn.addEventListener('click', () => {
            const typeNom = prompt("Nom du nouveau type de capteur :");
            if (typeNom) {
                fetch("http://127.0.0.1:8000/api/type-capteur", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ nom: typeNom })
                })
                .then(() => {
                    // Affiche un message de confirmation
                    alert("Type de capteur ajouté avec succès !");
                    // Met à jour la liste des types de capteur
                    loadTypesCapteur();
                })
                .catch(error => console.error("Erreur lors de l'ajout :", error));
            }
        });
    }

    // Ajouter une pièce
    if (addPieceForm) {
        addPieceForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const logementId = logementPieceSelect.value;
            const nom = document.getElementById('nomPiece').value;

            fetch("http://127.0.0.1:8000/api/piece", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id_logement: logementId, nom })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error("Erreur :", error));
        });
    }
    if (addFactureForm) {
        addFactureForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const logementId = factureLogementSelect.value;
            const typeId = factureTypeSelect.value;
            const montant = document.getElementById('factureMontant').value;
            const mois = document.getElementById('factureMois').value;  // Le mois sous forme de chiffre (1 à 12)
        
            console.log({ logementId, typeId, montant, mois });  // Debugging
        
            fetch("http://127.0.0.1:8000/api/facture", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id_logement: logementId,
                    id_type: typeId,
                    montant: montant,
                    mois: mois
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erreur lors de l'ajout de la facture");
                }
                return response.json();
            })
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error("Erreur :", error);
                alert("Erreur de validation ou problème serveur");
            });
        });
             
    }  
    // Ajouter un type de facture via le bouton "+"
    if (addFactureTypeButton) {
        addFactureTypeButton.addEventListener('click', () => {
            const factureNom = prompt("Nom du nouveau type de facture :");
            if (factureNom) {
                fetch("http://127.0.0.1:8000/api/type-facture", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ nom: factureNom })
                })
                .then(() => {
                    // Affiche un message de confirmation
                    alert("Type de facture ajouté avec succès !");
                    loadTypesFacture();  // Recharge la liste des types après ajout
                })
                .catch(error => console.error("Erreur lors de l'ajout :", error));
            }
        });
    }

    // Fonction pour recharger la liste des types de factures (pour un <select>)
    function loadTypesFacture() {
        fetch("http://127.0.0.1:8000/api/types-facture")
            .then(response => response.json())
            .then(data => {
                const selectElement = document.getElementById('factureType');  // Assure-toi que c'est bien un <select>
                selectElement.innerHTML = '<option value="" disabled selected>Choisir un type</option>';  // Réinitialise le menu déroulant

                data.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type.id;  // L'ID du type de facture
                    option.textContent = type.nom;  // Nom du type de facture
                    selectElement.appendChild(option);
                });
            })
            .catch(error => console.error("Erreur lors du chargement :", error));
    }


    capteurLogementSelect.addEventListener('change', function () {
        const logementId = this.value;
        loadPiecesForCapteurs(logementId);
    });

    loadLogementsForSelects();
    loadFactureTypes();
    loadTypesCapteur();
    loadTypesFacture();
    
});
