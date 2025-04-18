document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('rechercheForm').addEventListener('submit', function(e) {
        e.preventDefault();

        var du = document.getElementById('du').value;
        var au = document.getElementById('au').value;

        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/contrevenants?du=' + du + '&au=' + au, true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                var comptage = {};

                data.forEach(function(item) {
                    var nom = item.etablissement;
                    comptage[nom] = (comptage[nom] || 0) + 1;
                });

                var tbody = document.querySelector('#resultatsTable tbody');
                tbody.innerHTML = '';

                for (var etab in comptage) {
                    var tr = document.createElement('tr');
                    var tdNom = document.createElement('td');
                    var tdNb = document.createElement('td');

                    tdNom.textContent = etab;
                    tdNb.textContent = comptage[etab];

                    tr.appendChild(tdNom);
                    tr.appendChild(tdNb);
                    tbody.appendChild(tr);
                }

                // ✅ On affiche maintenant les résultats
                document.getElementById('resultatsSection').style.display = 'block';
                document.getElementById('resultatsTable').style.display = 'table';
            }
        };

        xhr.onerror = function () {
            alert('Erreur réseau');
        };

        xhr.send();
    });
});

// Charger la liste des établissements
function chargerListeRestaurants() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/contrevenants?du=1900-01-01&au=2100-01-01', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var nomsUniques = new Set();
            data.forEach(function(item) {
                nomsUniques.add(item.etablissement);
            });

            var select = document.getElementById('listeRestaurants');
            nomsUniques.forEach(function(nom) {
                var option = document.createElement('option');
                option.value = nom;
                option.textContent = nom;
                select.appendChild(option);
            });
        }
    };
    xhr.send();
}

// Gestion du formulaire de recherche par restaurant
document.getElementById('formulaireRestaurant').addEventListener('submit', function(e) {
    e.preventDefault();
    var nom = document.getElementById('listeRestaurants').value;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/infractions?nom=' + encodeURIComponent(nom), true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var tbody = document.querySelector('#infractionsResultat tbody');
            tbody.innerHTML = '';

            data.forEach(function(item) {
                var tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${item.date}</td>
                    <td>${item.description}</td>
                    <td>${item.montant}$</td>
                    <td>${item.ville}</td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('infractionsResultat').style.display = 'block';
        }
    };
    xhr.send();
});

chargerListeRestaurants();

