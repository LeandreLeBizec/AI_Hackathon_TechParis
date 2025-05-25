import logging
import os
import asyncio
import json

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

async def send_weather_message(ctx):
    await asyncio.sleep(5)  # Attendre 5 secondes
    try:
        # Envoyer le message à l'agent et générer une réponse
        await session.generate_reply(user_input="quelle temps fait-il actuellement?")
        logger.info("Message météo envoyé à l'agent")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message météo: {e}")

async def entrypoint(ctx: JobContext):
    await ctx.connect()

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

    #avatar_id = os.getenv("BEY_AVATAR_ID")
    #bey_avatar = bey.AvatarSession(avatar_id=avatar_id)
    #await bey_avatar.start(session, room=ctx.room)

    await session.start(
        agent=Agent(instructions="Vous êtes un assistant vocal amical qui peut parler de la météo."),
        room=ctx.room,
        room_output_options=RoomOutputOptions(audio_enabled=True),
    )

    # Lancer l'envoi du message météo après 5 secondes
    asyncio.create_task(send_weather_message(ctx))

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM)
    )