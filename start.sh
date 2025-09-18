#!/bin/sh

# Start the Python agent in the background
# The agent will connect to the room specified by the LIVEKIT_ROOM environment variable
echo "Starting Python agent..."
python agent.py connect --room $LIVEKIT_ROOM &

# Start the Next.js application in the foreground
echo "Starting Next.js server..."
pnpm start
