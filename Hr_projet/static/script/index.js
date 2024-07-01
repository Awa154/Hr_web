const sideMenu=document.querySelector("aside");
const menuBtn=document.querySelector("#menu-btn");
const closeBtn=document.querySelector("#close-btn");
const themeToggler=document.querySelector(".theme-toggler");

//ouvrir le sidebar
menuBtn.addEventListener('click', ()=>{
    sideMenu.style.display='block';
})

//fermer le sidebar
closeBtn.addEventListener('click', ()=>{
    sideMenu.style.display='none';
})

//changer le thème de l'écran
themeToggler.addEventListener('click', ()=>{
    document.body.classList.toggle("dark-theme-variables");

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
})

// Fonction pour gérer la navigation du tableau d'affichage de la liste des comptes
function scrollTable(direction) {
    const tableContainer = document.querySelector('.overflow-x-auto');
    const scrollAmount = tableContainer.offsetWidth;
    tableContainer.scrollLeft += direction * scrollAmount;
}

document.addEventListener("DOMContentLoaded", function() {
    // Sélectionne tous les liens de la barre latérale
    const sidebarLinks = document.querySelectorAll('.sidebar-link');

    // Fonction pour gérer l'ajout de la classe 'active'
    function setActiveLink(link) {
        // Supprime la classe 'active' de tous les liens
        sidebarLinks.forEach(link => link.classList.remove('active'));
        // Ajoute la classe 'active' au lien cliqué
        link.classList.add('active');
    }

    // Ajoute un événement de clic à chaque lien
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // Empêche le comportement par défaut pour les liens qui ne naviguent pas
            if (this.getAttribute('href') === '#') {
                event.preventDefault();
            }
            // Gère la mise à jour de la classe 'active'
            setActiveLink(this);
        });
    });

    // Vérifie si un lien doit rester actif après le rechargement
    const currentPath = window.location.pathname;
    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') !== '#' && link.getAttribute('href').includes(currentPath)) {
            setActiveLink(link);
        }
    });
});


// Gestion des champs de rôles
document.addEventListener('DOMContentLoaded', function() {
    const roleInputs = document.querySelectorAll('input[name="role"]');
    const employeFields = document.getElementById('employe-fields');
    const adminFields = document.getElementById('admin-fields');
    const entrepriseFields = document.getElementById('entreprise-fields');
    const addCompetenceButton = document.getElementById('add-competence');
    const competencesContainer = document.getElementById('competences-container');

    roleInputs.forEach(input => {
        input.addEventListener('change', function() {
            employeFields.classList.add('d-none');
            adminFields.classList.add('d-none');
            entrepriseFields.classList.add('d-none');

            if (this.value === 'EM') {
                employeFields.classList.remove('d-none');
            } else if (this.value === 'AD') {
                adminFields.classList.remove('d-none');
            } else if (this.value === 'EN') {
                entrepriseFields.classList.remove('d-none');
            }
        });
    });

    if (addCompetenceButton && competencesContainer) {
        addCompetenceButton.addEventListener('click', function() {
            const newCompetenceField = document.createElement('div');
            newCompetenceField.className = 'form-group';
            newCompetenceField.innerHTML = `
                <input type="text" name="competences" class="form-control mt-2">
                <button type="button" class="btn btn-link text-danger remove-competence">Supprimer</button>
            `;
            competencesContainer.appendChild(newCompetenceField);

            newCompetenceField.querySelector('.remove-competence').addEventListener('click', function() {
                newCompetenceField.remove();
            });
        });
    }
});

