import logging
import os
import asyncio

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


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(  
        instructions="You are a not friendly voice assistant built by LiveKit.",  
        tools=[],  
    )

    # Gemini
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
        agent=agent,
        room=ctx.room,
        room_output_options=RoomOutputOptions(audio_enabled=True),
    )

    # Envoyer le message texte dans le chat - MÉTHODE CORRIGÉE  
    try:  
        writer = await ctx.room.local_participant.stream_text(  
            topic="lk.chat"  
        )  
        await writer.write("Voici le lien : http://localhost:5173/")  
        await writer.aclose()  
        logger.info("Message texte envoyé avec succès dans le chat")  
    except Exception as e:  
        logger.error(f"Erreur lors de l'envoi du message: {e}")

    logger.info("envoyer le message texte : http://localhost:5173/")



if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM)
    )
