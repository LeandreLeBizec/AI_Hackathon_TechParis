// Initialisation de l'éditeur CodeMirror
const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    mode: "python",
    theme: "monokai",
    lineNumbers: true,
    indentUnit: 4,
    indentWithTabs: false,
    lineWrapping: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    extraKeys: {"Tab": "indentMore", "Shift-Tab": "indentLess"}
});

// Code Python par défaut
editor.setValue("# Écrivez votre code Python ici\nprint('Hello, World!')");

// Fonction pour exécuter le code
async function runCode() {
    const code = editor.getValue();
    const outputDiv = document.getElementById("output");
    
    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (result.error) {
            outputDiv.innerHTML = `<span style="color: red;">${result.error}</span>`;
        } else {
            outputDiv.innerHTML = result.output;
        }
    } catch (error) {
        outputDiv.innerHTML = `<span style="color: red;">Erreur de connexion au serveur</span>`;
    }
} 