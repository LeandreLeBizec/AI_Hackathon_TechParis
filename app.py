import logging
import os
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


def read_instructions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


async def entrypoint(ctx: JobContext):
    instructions = read_instructions('Instructions.txt')
    json_data = read_json('response_1748098463317 (1) (1).json')
    await ctx.connect()

    # Use json_data as needed, for example:
    candidate_name = json_data['candidate_analysis']['basic_info']['candidate_name']
    logger.info(f"Interviewing candidate: {candidate_name}")

    # Gemini
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

    await session.start(
        agent=Agent(instructions=f"Your instructions are: {instructions}, the candidate informations are: {json_data}"),
        room=ctx.room,
        room_output_options=RoomOutputOptions(audio_enabled=True),
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM)
    )