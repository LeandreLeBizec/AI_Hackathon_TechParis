import os
from datetime import datetime

class TranscriptManager:
    def __init__(self, directory="transcripts"):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        self.transcript_lines = []

    def add_line(self, text):
        self.transcript_lines.append(text)

    def save(self, filename=None):
        if filename is None:
            # Utilise la date et l'heure pour un nom unique
            filename = datetime.now().strftime("transcript_%Y%m%d_%H%M%S.txt")
        path = os.path.join(self.directory, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.transcript_lines))
        return path