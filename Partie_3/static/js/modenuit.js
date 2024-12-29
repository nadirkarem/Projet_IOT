document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'dark-mode';

    // Appliquer le thème au chargement
    document.body.classList.add(currentTheme);
    document.querySelector('.container').classList.add(currentTheme);
    document.querySelector('footer').classList.add(currentTheme);
    document.querySelector('.navbar').classList.add(currentTheme);  // Appliquer à la navbar
    
    // Appliquer le thème aux cartes et aux graphiques
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add(currentTheme);
    });
    document.querySelectorAll('.chart-dark').forEach(chart => {
        chart.classList.add(currentTheme);
    });

    // Icône du bouton en fonction du thème
    themeToggle.textContent = currentTheme === 'dark-mode' ? '🌙' : '☀️';

    themeToggle.addEventListener('click', () => {
        if (document.body.classList.contains('dark-mode')) {
            // Passer en mode jour
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');

            document.querySelector('.container').classList.remove('dark-mode');
            document.querySelector('.container').classList.add('light-mode');

            document.querySelector('footer').classList.remove('dark-mode');
            document.querySelector('footer').classList.add('light-mode');

            document.querySelector('.navbar').classList.remove('dark-mode');  // Mettre à jour la navbar
            document.querySelector('.navbar').classList.add('light-mode');

            // Mise à jour pour les cartes
            document.querySelectorAll('.card').forEach(card => {
                card.classList.remove('dark-mode');
                card.classList.add('light-mode');  
                console.log(card.classList);  // Vérifier si light-mode/dark-mode s'applique
            });

            // Mise à jour pour les graphiques
            document.querySelectorAll('.chart-dark').forEach(chart => {
                chart.classList.remove('dark-mode');
                chart.classList.add('light-mode');
            });

            themeToggle.textContent = '☀️';
            localStorage.setItem('theme', 'light-mode');
        } else {
            // Passer en mode nuit
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');

            document.querySelector('.container').classList.remove('light-mode');
            document.querySelector('.container').classList.add('dark-mode');

            document.querySelector('footer').classList.remove('light-mode');
            document.querySelector('footer').classList.add('dark-mode');

            document.querySelector('.navbar').classList.remove('light-mode');  // Mettre à jour la navbar
            document.querySelector('.navbar').classList.add('dark-mode');

            // Mise à jour pour les cartes
            document.querySelectorAll('.card').forEach(card => {
                card.classList.remove('light-mode');
                card.classList.add('dark-mode'); 
            });
            document.querySelectorAll('.card').forEach(card => {
                console.log(card.classList);  // Vérifier si light-mode/dark-mode s'applique
            });

            // Mise à jour pour les graphiques
            document.querySelectorAll('.chart-dark').forEach(chart => {
                chart.classList.remove('light-mode');
                chart.classList.add('dark-mode');
            });

            themeToggle.textContent = '🌙';
            localStorage.setItem('theme', 'dark-mode');
        }
    });
});
