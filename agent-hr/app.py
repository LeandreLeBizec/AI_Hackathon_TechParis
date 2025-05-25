import logging
import asyncio
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import queue
import subprocess

from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RoomOutputOptions,
    WorkerOptions,
    WorkerType,
    cli,
)
from livekit.plugins import bey, google   # ← switched from openai → google

logger = logging.getLogger("bey-avatar-example")
logger.setLevel(logging.INFO)

load_dotenv()  # GOOGLE_API_KEY is in .env

def read_instructions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#async def send_weather_message(ctx):
#    await asyncio.sleep(5)  # Attendre 5 secondes
#    try:
#        # Envoyer le message à l'agent et générer une réponse
#        await session.generate_reply(user_input="quelle temps fait-il actuellement?")
#        logger.info("Message météo envoyé à l'agent")
#    except Exception as e:
#        logger.error(f"Erreur lors de l'envoi du message météo: {e}")

class LogHandler(FileSystemEventHandler):
    def __init__(self, session):
        self.session = session
        self.last_processed = {}
        self.event_queue = queue.Queue()
        self.processing_files = set()  # Pour suivre les fichiers en cours de traitement
        logger.info("LogHandler initialisé")

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.event_queue.put(('created', event.src_path))

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.event_queue.put(('modified', event.src_path))

    async def process_new_log(self, log_path):
        if log_path in self.processing_files:
            return
            
        self.processing_files.add(log_path)
        try:
            with open(log_path, 'r') as f:
                log_content = json.loads(f.read())
                logger.info("\n=== NOUVEAU LOG DÉTECTÉ ===")
                logger.info(f"Fichier : {log_path}")
                logger.info(f"Timestamp : {log_content.get('timestamp', 'N/A')}")
                # Masquer l'email de l'utilisateur
                user = log_content.get('user', 'N/A')
                if '@' in user:
                    user = user.split('@')[0] + '@***'
                logger.info(f"Utilisateur : {user}")
                logger.info(f"Langage : {log_content.get('language', 'N/A')}")
                logger.info("\nCode exécuté :")
                logger.info(f"```{log_content.get('language', '')}\n{log_content.get('code', '')}\n```")
                
                if log_content.get('output'):
                    logger.info("\nSortie :")
                    logger.info(f"```\n{log_content.get('output', '')}\n```")
                
                if log_content.get('error'):
                    logger.info("\nErreur :")
                    logger.info(f"```\n{log_content.get('error', '')}\n```")
                
                logger.info("========================")
                
                # Envoyer le contenu du log à l'agent sans l'email
                await self.session.generate_reply(
                    user_input=f"This is the solution of the exercise you gave me, can you comment it ? Code en {log_content.get('language')}:\n{log_content.get('code')}\n\nSortie:\n{log_content.get('output')}\n\nErreur:\n{log_content.get('error')}"
                )
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de décodage JSON pour le log {log_path}: {e}")
        except Exception as e:
            logger.error(f"Erreur lors du traitement du log {log_path}: {e}")
        finally:
            self.processing_files.remove(log_path)

async def process_event_queue(handler):
    while True:
        try:
            if not handler.event_queue.empty():
                event_type, log_path = handler.event_queue.get_nowait()
                # Ne traiter que les événements 'created' pour éviter les doublons
                if event_type == 'created':
                    await handler.process_new_log(log_path)
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la queue : {e}")

async def start_log_monitoring(session):
    # Utiliser le chemin absolu
    base_dir = Path(__file__).parent.parent
    log_dir = base_dir / "live-coding" / "logs"
    logger.info(f"Surveillance du dossier : {log_dir}")
    
    if not log_dir.exists():
        logger.error(f"Le dossier de logs n'existe pas : {log_dir}")
        return None
        
    event_handler = LogHandler(session)
    observer = Observer()
    observer.schedule(event_handler, str(log_dir), recursive=True)
    observer.start()
    logger.info("Surveillance des logs démarrée")
    
    # Démarrer le traitement de la queue d'événements
    asyncio.create_task(process_event_queue(event_handler))
    
    return observer

async def entrypoint(ctx: JobContext):
    base_dir = Path(__file__).parent
    instructions = read_instructions(str(base_dir / 'Instructions.txt'))
    json_data = read_json(str(base_dir / 'response_1748098463317.json'))
    
    await ctx.connect()

    candidate_name = json_data['candidate_analysis']['basic_info']['candidate_name']
    logger.info(f"Interviewing candidate: {candidate_name}")

    # Envoyer le message texte dans le chat
    try:  
        writer = await ctx.room.local_participant.stream_text(  
            topic="lk.chat"  
        )  
        await writer.write("here is the link to the live coding website : http://localhost:3000/")  
        await writer.aclose()  
    except Exception as e:  
        logger.error(f"Erreur lors de l'envoi du message dans le chat: {e}")

    # Gemini
    global session
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(  
            model="gemini-2.0-flash-exp",        
            voice="Puck",                        # voix 
            temperature=0.8,
        ),
    )

    avatar_id = os.getenv("BEY_AVATAR_ID")
    bey_avatar = bey.AvatarSession(avatar_id=avatar_id)
    await bey_avatar.start(session, room=ctx.room)

    # Run Airtable_API.py concurrently
    asyncio.create_task(run_airtable_api())

    await session.start(
        agent=Agent(instructions=f"Your instructions are: {instructions}, the candidate informations are: {json_data}"),
        room=ctx.room,
        room_output_options=RoomOutputOptions(audio_enabled=True),
    )


    # Démarrer la surveillance des logs
    observer = await start_log_monitoring(session)
    if observer is None:
        logger.error("Impossible de démarrer la surveillance des logs")
        return

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        if observer:
            observer.stop()
            observer.join()
            logger.info("Surveillance des logs arrêtée")

async def run_airtable_api():
    subprocess.run(["python", "Airtable_API.py"])

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM)
    )