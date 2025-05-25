const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const app = express();
const port = 3000;

// Configuration de l'API de l'agent
const AGENT_API_URL = 'http://localhost:5000/api/logs';

// Middleware pour parser le JSON
app.use(express.json());

// Middleware pour servir les fichiers statiques
app.use(express.static(__dirname));

// Stockage des sessions (en mémoire pour cet exemple)
const sessions = new Map();

// Fonction pour créer un dossier temporaire pour un utilisateur
function getUserTempDir(user) {
    const userDir = path.join(__dirname, 'temp', user);
    if (!fs.existsSync(userDir)) {
        fs.mkdirSync(userDir, { recursive: true });
    }
    return userDir;
}

// Fonction pour créer un dossier de logs pour un utilisateur
function getUserLogsDir(user) {
    const logsDir = path.join(__dirname, 'logs', user);
    if (!fs.existsSync(logsDir)) {
        fs.mkdirSync(logsDir, { recursive: true });
    }
    return logsDir;
}

// Fonction pour sauvegarder un log
async function saveLog(user, code, output, error) {
    console.log(`[LOG] Sauvegarde du log pour l'utilisateur ${user}`);
    const logsDir = getUserLogsDir(user);
    const timestamp = new Date().toISOString();
    const logEntry = {
        timestamp,
        code,
        output: output || '',
        error: error || '',
        language: 'python',
        user: user
    };
    
    const logFile = path.join(logsDir, `log_${Date.now()}.json`);
    fs.writeFileSync(logFile, JSON.stringify(logEntry, null, 2));
    console.log(`[LOG] Log sauvegardé dans ${logFile}`);

    // Envoyer le log à l'agent
    try {
        await sendLogToAgent(logEntry);
    } catch (error) {
        console.error('[LOG] Erreur lors de l\'envoi du log à l\'agent:', error.message);
    }

    return logEntry;
}

// Fonction pour envoyer le log à l'agent
async function sendLogToAgent(logEntry) {
    console.log('[AGENT] Envoi du log à l\'agent:', JSON.stringify(logEntry, null, 2));
    try {
        const response = await axios.post(AGENT_API_URL, logEntry);
        console.log('[AGENT] Log envoyé avec succès:', response.data);
        return response.data;
    } catch (error) {
        console.error('[AGENT] Erreur lors de l\'envoi du log:', error.message);
        throw error;
    }
}

// Endpoint pour exécuter le code Python
app.post('/execute', async (req, res) => {
    const { code, user } = req.body;
    console.log(`[EXECUTE] Requête reçue de l'utilisateur ${user}`);

    if (!user) {
        console.log('[EXECUTE] Erreur: Utilisateur non authentifié');
        return res.status(401).json({ error: 'Utilisateur non authentifié' });
    }

    // Créer un fichier temporaire unique pour cet utilisateur
    const userDir = getUserTempDir(user);
    const tempFile = path.join(userDir, `script_${Date.now()}.py`);

    // Écrire le code dans le fichier temporaire
    fs.writeFileSync(tempFile, code);
    console.log(`[EXECUTE] Code écrit dans ${tempFile}`);

    // Exécuter le code Python
    exec(`python3 ${tempFile}`, async (error, stdout, stderr) => {
        // Supprimer le fichier temporaire
        fs.unlinkSync(tempFile);
        console.log(`[EXECUTE] Fichier temporaire supprimé: ${tempFile}`);

        // Sauvegarder le log
        const logEntry = await saveLog(user, code, stdout, stderr);

        if (error) {
            console.log(`[EXECUTE] Erreur d'exécution: ${stderr}`);
            res.json({ error: stderr, log: logEntry });
        } else {
            console.log(`[EXECUTE] Exécution réussie: ${stdout}`);
            res.json({ output: stdout, log: logEntry });
        }
    });
});

// Endpoint pour récupérer les logs d'un utilisateur
app.get('/logs/:user', (req, res) => {
    const { user } = req.params;
    console.log(`[LOGS] Récupération des logs pour l'utilisateur ${user}`);
    const logsDir = getUserLogsDir(user);
    
    try {
        const logFiles = fs.readdirSync(logsDir)
            .filter(file => file.endsWith('.json'))
            .map(file => {
                const content = fs.readFileSync(path.join(logsDir, file), 'utf8');
                return JSON.parse(content);
            })
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        console.log(`[LOGS] ${logFiles.length} logs trouvés pour ${user}`);
        res.json(logFiles);
    } catch (error) {
        console.error(`[LOGS] Erreur lors de la récupération des logs: ${error}`);
        res.status(500).json({ error: 'Erreur lors de la récupération des logs' });
    }
});

// Démarrer le serveur
app.listen(port, () => {
    console.log(`[SERVER] Serveur démarré sur http://localhost:${port}`);
    // Créer les dossiers de base
    const baseDirs = ['temp', 'logs'];
    baseDirs.forEach(dir => {
        const dirPath = path.join(__dirname, dir);
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
        }
    });
}); 