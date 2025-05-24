#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

# trouvé dans le .env
API_KEY    = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")
ROOM       = os.getenv("LIVEKIT_ROOM", "my-room")
IDENTITY   = os.getenv("IDENTITY", "User-1")
NAME       = os.getenv("NAME", "User-1")

# get the token
token = (
    api.AccessToken(API_KEY, API_SECRET)
       .with_identity(IDENTITY)
       .with_name(NAME)
       .with_grants(
           api.VideoGrants(
               room_join=True,
               room=ROOM,
               can_publish=True,
               can_subscribe=True,
           )
       )
       .to_jwt()
)

print(token)