
const nextButton= document.querySelector('.btn-next');
const prevButton= document.querySelector('.btn-prev');
const Steps= document.querySelectorAll('.step');
const form_steps= document.querySelectorAll('.form-step');
let active =1;

nextButton.addEventListener('click', () => {
    active++;
    if(active > Steps.length){
        active=Steps.length;
    }
    updateProgress();
})

prevButton.addEventListener('click', () => {
    active--;
    if(active <1){
        active=1;
    }
    updateProgress();
})

const updateProgress = () => {
    console.log('Steps.length => ' + Steps.length);
    console.log('active => ' + active);
    //toogle .active class pour chaque liste d'élément
    Steps.forEach((Step, i) => {
        if(i==(active-1)){
            Step.classList.add('active');
            form_steps[i].classList.add('active');
            console.log('i =>' +i);
        }else{
            Step.classList.remove('active');
            form_steps[i].classList.remove('active');
        }
    });

    //activer ou désactiver les bouttons retour et suivant
    if (active == 1){
        prevButton.disabled = true;
    } else if (active == Steps.length) {
        nextButton.disabled = true;
    }else{
        prevButton.disabled=false;
        nextButton.disabled=false;
    }
};

document.getElementById('employe').addEventListener('change', function() {
    const employeId = this.value;
    if (employeId) {
        fetch(`/get_employe_details/${employeId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('nom_employe').value = data.nom;
                document.getElementById('prenom_employe').value = data.prenom;
                document.getElementById('contact_employe').value = data.contact;
                document.getElementById('email_employe').value = data.email;
                document.getElementById('adresse_employe').value = data.adresse;
            });
    }
});

document.getElementById('entreprise').addEventListener('change', function() {
    const entrepriseId = this.value;
    if (entrepriseId) {
        fetch(`/get_entreprise_details/${entrepriseId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('nom_entreprise_employeur').value = data.nom_entreprise;
                document.getElementById('contact_entreprise').value = data.contact;
                document.getElementById('email_entreprise').value = data.email;
                document.getElementById('adresse_entreprise').value = data.adresse;
            });
    }
});