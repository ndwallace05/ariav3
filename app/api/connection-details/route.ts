import { NextResponse } from 'next/server';
// Import AgentServiceClient and JobType
import {
  AccessToken,
  AgentDispatchClient,
  type AccessTokenOptions,
  type VideoGrant,
} from 'livekit-server-sdk';

// NOTE: you are expected to define the following environment variables in `.env.local`:
const API_KEY = process.env.LIVEKIT_API_KEY;
const API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;

// don't cache the results
export const revalidate = 0;

export type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

export async function POST(req: Request) {
  try {
    if (LIVEKIT_URL === undefined) {
      throw new Error('LIVEKIT_URL is not defined');
    }
    if (API_KEY === undefined) {
      throw new Error('LIVEKIT_API_KEY is not defined');
    }
    if (API_SECRET === undefined) {
      throw new Error('LIVEKIT_API_SECRET is not defined');
    }

    // --- NEW: Create an AgentDispatchClient and dispatch an agent to the room ---
    const agentClient = new AgentDispatchClient(LIVEKIT_URL, API_KEY, API_SECRET);

    // Generate a unique room name for this session
    const roomName = `voice_assistant_room_${Math.floor(Math.random() * 10_000)}`;

    // Dispatch a short-lived agent for the room. The SDK exposes `createDispatch(roomName, agentName?, options?)`.
    // We don't need to wait for a long-running job; createDispatch will instruct LiveKit to start an agent for the room.
  console.log(`Attempting to dispatch agent for room: ${roomName}`);
  // Generate an agent identity and pass it to satisfy the SDK's typing.
  const agentName = `aria_agent_${Math.floor(Math.random() * 10_000)}`;
  await agentClient.createDispatch(roomName, agentName, { metadata: JSON.stringify({ purpose: 'voice-assistant' }) });
    console.log(`Successfully dispatched agent dispatch for room: ${roomName}`);
    // --- END NEW SECTION ---

    // Generate participant token
    const participantName = 'user';
    const participantIdentity = `voice_assistant_user_${Math.floor(Math.random() * 10_000)}`;

    const participantToken = await createParticipantToken(
      { identity: participantIdentity, name: participantName },
      roomName
    );

    // Return connection details
    const data: ConnectionDetails = {
      serverUrl: LIVEKIT_URL,
      roomName,
      participantToken: participantToken,
      participantName,
    };
    const headers = new Headers({
      'Cache-Control': 'no-store',
    });
    return NextResponse.json(data, { headers });
  } catch (error) {
    if (error instanceof Error) {
      console.error(error);
      return new NextResponse(error.message, { status: 500 });
    }
  }
}

function createParticipantToken(
  userInfo: AccessTokenOptions,
  roomName: string
): Promise<string> {
  const at = new AccessToken(API_KEY, API_SECRET, {
    ...userInfo,
    ttl: '15m',
  });
  const grant: VideoGrant = {
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canPublishData: true,
    canSubscribe: true,
  };
  at.addGrant(grant);

  // We no longer need the agent configuration on the participant token,
  // as the job dispatch handles it. This can be removed.

  return at.toJwt();
}
