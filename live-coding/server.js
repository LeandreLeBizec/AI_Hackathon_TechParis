const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 3000;

// Middleware pour parser le JSON
app.use(express.json());

// Servir les fichiers statiques
app.use(express.static(__dirname));

// Endpoint pour exécuter le code Python
app.post('/execute', (req, res) => {
    const code = req.body.code;
    const tempFile = path.join(__dirname, 'temp.py');

    // Écrire le code dans un fichier temporaire
    fs.writeFileSync(tempFile, code);

    // Exécuter le code Python
    exec(`python3 ${tempFile}`, (error, stdout, stderr) => {
        // Supprimer le fichier temporaire
        fs.unlinkSync(tempFile);

        if (error) {
            res.json({ error: error.message });
            return;
        }

        if (stderr) {
            res.json({ error: stderr });
            return;
        }

        res.json({ output: stdout });
    });
});

app.listen(port, () => {
    console.log(`Serveur démarré sur http://localhost:${port}`);
}); 