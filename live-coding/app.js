// Initialisation de l'éditeur CodeMirror
const editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: "python",
    theme: "monokai",
    lineNumbers: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    tabSize: 4,
    lineWrapping: true
});

// Code Python par défaut
editor.setValue('print("Hello, World!")');

// Gestion de la session
let currentUser = null;

// Vérifier si l'utilisateur est déjà connecté
function checkSession() {
    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
        currentUser = userEmail;
        showUserInfo();
    } else {
        showLoginModal();
    }
}

// Afficher la modale de connexion
function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    document.querySelector('.editor-container').style.display = 'none';
    document.getElementById('output').style.display = 'none';
}

// Cacher la modale de connexion
function hideLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
    document.querySelector('.editor-container').style.display = 'block';
    document.getElementById('output').style.display = 'block';
}

// Afficher les informations de l'utilisateur
function showUserInfo() {
    const userInfo = document.getElementById('userInfo');
    const userEmail = document.querySelector('.user-email');
    userEmail.textContent = currentUser;
    userInfo.style.display = 'flex';
    hideLoginModal();
}

// Gérer la déconnexion
function logout() {
    localStorage.removeItem('userEmail');
    currentUser = null;
    document.getElementById('userInfo').style.display = 'none';
    showLoginModal();
}

// Gérer la soumission du formulaire de connexion
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    if (email) {
        currentUser = email;
        localStorage.setItem('userEmail', email);
        showUserInfo();
    }
});

// Fonction pour formater la date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Fonction pour afficher les logs
async function displayLogs() {
    if (!currentUser) return;

    try {
        const response = await fetch(`/logs/${encodeURIComponent(currentUser)}`);
        const logs = await response.json();
        
        const logsList = document.getElementById('logsList');
        logsList.innerHTML = '';

        logs.forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            
            logEntry.innerHTML = `
                <div class="log-header">
                    <span>${formatDate(log.timestamp)}</span>
                    <span>${log.language}</span>
                </div>
                <div class="log-code">${log.code}</div>
                ${log.error ? 
                    `<div class="log-output log-error">${log.error}</div>` :
                    `<div class="log-output">${log.output}</div>`
                }
            `;
            
            logsList.appendChild(logEntry);
        });
    } catch (error) {
        console.error('Erreur lors de la récupération des logs:', error);
    }
}

// Fonction pour basculer l'affichage des logs
function toggleLogs() {
    const logsContainer = document.getElementById('logsContainer');
    if (logsContainer.style.display === 'none') {
        logsContainer.style.display = 'block';
        displayLogs();
    } else {
        logsContainer.style.display = 'none';
    }
}

// Modifier la fonction runCode pour mettre à jour les logs après l'exécution
async function runCode() {
    if (!currentUser) {
        alert('Veuillez vous connecter pour exécuter du code');
        return;
    }

    const code = editor.getValue();
    const output = document.getElementById("output");
    output.innerHTML = "Exécution en cours...";
    output.className = "";

    try {
        const response = await fetch("/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code, user: currentUser }),
        });

        const data = await response.json();

        if (data.error) {
            output.innerHTML = data.error;
            output.className = "error";
        } else {
            output.innerHTML = data.output;
            output.className = "";
        }

        // Mettre à jour les logs si la section est visible
        if (document.getElementById('logsContainer').style.display === 'block') {
            displayLogs();
        }
    } catch (error) {
        output.innerHTML = "Erreur de connexion au serveur";
        output.className = "error";
    }
}

// Vérifier la session au chargement de la page
checkSession(); 