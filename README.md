# LiveKit + Next.js AI Voice Agent Interface

A basic example of a Next.js frontend for a LiveKit AI voice agent.
- data passing between frontend and backend voice agent
- agent dispatch to connect both frontend and calling via optional SIP trunk setup (see repo linked at bottom)

## Dev Setup

Clone the repository and install dependencies:

```console
pnpm i
```

Set up the environment by copying `.env.example` to `.env` and filling in the required values:

- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

Run the Next.js application:

```console
pnpm run dev
```

This frontend application requires an agent to communicate with. You can use one this example agent in [livekit-voice-agent-python](https://github.com/kylecampbell/livekit-voice-agent-python)
